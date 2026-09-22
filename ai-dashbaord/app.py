import streamlit as st
import plotly.graph_objects as go
from ui_helpers import display_api_error
from api_client import create_task, login, get_current_user, get_tasks, delete_task, update_task, get_task_suggestion





# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Task Dashboard",
    page_icon="🤖",
    layout="wide",
    )


# --------------------------------------------------
# Session state
# --------------------------------------------------
def initialize_session_state():
    """Initialize application state used across reruns."""
    if "token" not in st.session_state:
        st.session_state.token = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if "ai_suggestion" not in st.session_state:
        st.session_state.ai_suggestion = None

initialize_session_state()

# --------------------------------------------------
# Configuration
# --------------------------------------------------



API_URL = st.secrets["API_URL"]



# --------------------------------------------------
# Helper functions
# --------------------------------------------------




def load_tasks(
        status_filter="All", priority_filter="All"
        ):
    """Load tasks from the API using the selected status filter."""

    completed = None

    if status_filter == "Pending":
        completed = False

    elif status_filter == "Completed":
        completed = True

    priority = None

    if priority_filter != "All":
        priority = priority_filter.lower()

    return get_tasks(
        API_URL,
        st.session_state.token,
        completed=completed,
        priority=priority,
        )




# Login page
# --------------------------------------------------

if st.session_state.token is None:

    st.title("🤖 Task Dashboard")
    st.subheader("Login")

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        )

    password = st.text_input(
        "Password",
        type="password",
        )

    if st.button(
        "Login",
        type="primary",
        use_container_width=True,
        ):

        if not email or not password:
            st.warning(
                "Please enter your email and password."
                )

        else:

            try:
                with st.spinner("Logging in..."):

                    result = login(
                        API_URL,
                        email,
                        password,
                        )

                st.session_state.token = result["access_token"]

                # Get the user profile from the API.
                
                user = get_current_user(
                    API_URL,
                    st.session_state.token,
                    )

                st.session_state.username = (
                    user.get("name")
                    or user.get("username")
                    or email
                    )

                st.rerun()

            except Exception as exc:
                display_api_error(exc)
                st.stop()
    


# --------------------------------------------------
# Logged-in sidebar
# --------------------------------------------------

st.sidebar.title("⚙️ Account")

st.sidebar.write(
    f"Logged in as **{st.session_state.username}**"
    )

if st.sidebar.button(
    "Logout",
    use_container_width=True,
    ):

    st.session_state.token = None
    st.session_state.username = None

    st.rerun()

st.sidebar.divider()

st.sidebar.subheader("Task Filters")

status_filter = st.sidebar.selectbox(
    "Status",
    ["All", "Pending", "Completed"],
    )
priority_filter = st.sidebar.selectbox(
    "Priority",
    ["All", "Low", "Medium", "High"],
    )




# --------------------------------------------------
# Main application
# --------------------------------------------------

st.title("📊 Task Dashboard")

st.success(
    f"Welcome, {st.session_state.username}!"
    )   

try:
    with st.spinner("Loading tasks..."):
        tasks = load_tasks(
            status_filter,
            priority_filter,
            )

except Exception as exc:
    st.error(f"Unable to load tasks: {exc}")
    st.stop()


st.divider()

dashboard_tab, manage_tab = st.tabs(
    [
        "📊dashboard",
        "✅Manage Tasks",
    ]
    )

with dashboard_tab:
    total_tasks = len(tasks)

    completed_tasks = sum(
        task["completed"]
        for task in tasks
        )

    remaining_tasks = total_tasks - completed_tasks

    chart = go.Figure(
        data=[
            go.Pie(
                labels=["Completed", "Pending"],
                values=[completed_tasks, remaining_tasks],
                hole=0.5,
                )
            ]
        )

    chart.update_layout(
        title="Task Completion",
        height=350,
        )

    st.plotly_chart(
        chart,
        use_container_width=True,
        )



    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Tasks",
        total_tasks,
        )

    col2.metric(
        "Completed",
        completed_tasks,
        )

    col3.metric(
        "Remaining",
        remaining_tasks,
        )

    st.subheader("Your Tasks")

    if tasks:

        display_tasks = [
            {
                "ID": task["id"],
                "Title": task["title"],
                "Priority": task["priority"],
                "Completed": task["completed"],
            }

            for task in tasks
            ]

        st.dataframe(
            display_tasks,
            use_container_width=True,
            hide_index=True,
            )

    else:

        st.info(
            "You don't have any tasks yet. "
            "Create your first task in Manage Tasks."
            )




with manage_tab:

    st.subheader("Create a Task")

    with st.form("create_task_form"):

        title = st.text_input(
            "Task title",
            max_chars=200
            )
        description = st.text_area(
            "Description",
            max_chars=2000,
            )
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"]
            )
        submitted = st.form_submit_button(
            "Create Task",
            type="primary"
            )
        if submitted:

            if not title.strip():
                st.warning("Task title is required.")

            else:

                try:
                    with st.spinner("Creating task..."):

                        create_task(
                            API_URL,
                            st.session_state.token,
                            title=title.strip(),
                            description=description.strip(),
                            priority=priority,
                            )
                    st.success("Task created successfully!")

                    st.rerun()
                except Exception as exc:
                    st.error(
                        f"Unable to create task: {exc}"
                        )
        st.subheader("Existing Tasks")




    if not tasks:
        st.info("No tasks available.")

    else:
        for task in tasks:
            col1, col2, col3, col4 = st.columns(
                [5, 1, 1,2]
                )

            with col1:
                status = "✅ Completed" if task["completed"] else "⏳ Pending"

                st.write(
                    f"**{task['title']}** — "
                    f"{task['priority']} — {status}"
                    )
            with col2:
                if st.button(
                    "Complete",
                    key=f"complete_{task['id']}",
                    disabled=task["completed"],
                    ):
                    try:
                        with st.spinner("Completing task..."):
                            update_task(
                                API_URL,
                                st.session_state.token,
                                task["id"],
                                completed=True,
                            )

                        st.success("Task completed!")

                        st.rerun()

                    except Exception as exc:
                        st.error(f"Unable to complete task: {exc}"
                        )
            with col3:
                if st.button(
                    "Delete",
                    key=f"delete_{task['id']}",
                    ):
                    try:
                        with st.spinner("Deleting task..."):
                            delete_task(
                            API_URL,
                            st.session_state.token,
                            task["id"],
                            )

                        st.success("Task deleted!")

                        st.rerun()

                    except Exception as exc:
                        st.error(f"Unable to delete task: {exc}"
                    )
            with col4:
                if st.button(
                    "✨ AI Suggestion",
                    key=f"suggest_{task['id']}",
                    ):
                    try:
                        with st.spinner("Generating suggestion..."):
                            result = get_task_suggestion(
                                API_URL,
                                st.session_state.token,
                                task["id"],
                                )
                        st.info(result["suggestion"]
                        )
                    except Exception as exc:

                        st.error(
                            f"Unable to generate suggestion: {exc}"
                            )



                        

               