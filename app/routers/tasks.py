from fastapi import APIRouter, BackgroundTasks, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.task import Task, Priority
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskSuggestionResponse
from app.utils.exceptions import ForbiddenException, NotFoundException
from app.utils.notifications import log_activity, update_calendar
from app.utils.security import get_current_user



router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    )


def get_task_or_403(
    task_id: int,
    current_user: User,
    db: Session,
    ) -> Task:

    """Return a task when it exists and belongs to the current user."""

    task = db.get(Task, task_id)

    if task is None:
        raise NotFoundException(
            "Task",
            task_id,
            )

    if task.user_id != current_user.id:
        raise ForbiddenException(
            "You don't have permission to access this task"
            )

    return task

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    responses={
        401: {
            "description": "Authentication credentials are missing or invalid."
            },
        422: {
            "description": "Validation error for the task data."},
        },
    )

def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):

    """
    Create a new task for the authenticated user.

    - Requires an authenticated user.
    - Validates the task data.
    - Assigns the task to the authenticated user.
    - Returns the newly created task.
    
    """

    task = Task(
        **task_data.model_dump(),
        user_id=current_user.id,
        )

    db.add(task)
    db.commit()
    db.refresh(task)

    background_tasks.add_task(
        log_activity,
        current_user.id,
        f"Created task {task.title} {task.id}",
        )

    background_tasks.add_task(
        update_calendar,
        current_user.id,
        f"Task scheduled: {task.title}",
        )

    return task

@router.get(
    "",
    response_model=list[TaskResponse],
    summary="List the authenticated user's tasks",
    responses={
        401: {
            "description": "Authentication credentials are missing or invalid."
            },
        422: {
            "description": "Validation error for the query parameters."},
            },  
        )
def get_tasks(
    completed: bool | None = Query(
        default=None,
        description="Filter tasks by completion status.",
        ),
    priority: Priority | None = Query(
        default=None,
        description="Filter tasks by priority.",
        ),
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of tasks to skip.",
        ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of tasks to return.",
        ),

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):

    """
    
    Retrieve tasks belonging to the authenticated user.

    - Requires authentication.
    - Returns only the current user's tasks.
    - Supports filtering by completion status.
    - Supports filtering by priority.
    - Supports pagination with skip and limit.
    """

    statement = select(Task).where(
        Task.user_id == current_user.id
        )

    if completed is not None:
        statement = statement.where(
            Task.completed == completed
            )

    if priority is not None:
        statement = statement.where(
            Task.priority == priority
            )

    statement = statement.offset(skip).limit(limit)

    tasks = db.scalars(statement).all()

    return tasks

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    responses={
        401: {
            "description": "Authentication credentials are missing or invalid."
            },
        403: {
            "description": "The authenticated user does not own this task."
            },
        404: {
            "description": "Task with the specified ID was not found."
            },
        422: {
            "description": "Validation error for the task ID."},
        },
    )
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):

    """
    
    Retrieve a task by ID.

    - Requires authentication.
    - Returns the task when it belongs to the authenticated user.
    - Returns 403 when the task belongs to another user.
    - Returns 404 when the task does not exist.
    - Returns 422 when the task ID is invalid.
    
    """

    return get_task_or_403(
        task_id,
        current_user,
        db,
        )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    responses={
        401: {
            "description": "Authentication credentials are missing or invalid."
            },
        403: {
            "description": "The task belongs to another user."
            },
        404: {
            "description": "The task does not exist."
            },
        422: {
            "description": "Validation error for the task data."},
        },
    )
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):

    """
    Update a task belonging to the authenticated user.

    Supports partial updates.
    
    """

    task = get_task_or_403(
        task_id,
        current_user,
        db,
        )

    updates = task_data.model_dump(
        exclude_unset=True
        )

    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    background_tasks.add_task(
        log_activity,
        current_user.id,
        f"Updated task {task.title} {task.id}",
        )

    return task

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        401: {
            "description": "Authentication credentials are missing or invalid."
            },
        403: {
            "description": "The task belongs to another user."
            },
        404: {
            "description": "The task does not exist."},
        },
    )

def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):

    """
    Delete a task belonging to the authenticated user.
    
    """

    task = get_task_or_403(
        task_id,
        current_user,
        db,
        )

    task_title = task.title

    db.delete(task)
    db.commit()

    background_tasks.add_task(
        log_activity,
        current_user.id,
        f"Deleted task {task_title} {task_id}",
        )

    return None

@router.post(
    "/{task_id}/suggest",
    summary="Generate an AI-ready task suggestion",
    responses={
        200: {
            "description": "Placeholder AI suggestion generated successfully."
            },
        401: {
            "description": "Authentication credentials are missing or invalid."
            },
        403: {
            "description": "The task belongs to another user."
            },
        404: {
            "description": "The task does not exist."},
        },
    )

def suggest_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):

    """
    Return a placeholder AI suggestion for a user's task.

    The task description is used as the input for the future
    AI integration.
    
    """

    task = get_task_or_403(
        task_id,
        current_user,
        db,
        )

    suggestion = (
        f"AI suggestion for '{task.title}': "
        f"Break this task into smaller actionable steps."
        )

    return {
        "suggestion": suggestion,
        }


