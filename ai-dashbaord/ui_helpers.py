import requests
import streamlit as st


def display_api_error(exc):
    """Display a user-friendly message for common API errors."""

    if isinstance(exc, requests.ConnectionError):
        st.error(
            "Unable to connect to the API. "
            "Make sure the FastAPI server is running."
            )
    elif isinstance(exc, requests.Timeout):
        st.error(
            "The API request timed out. "
            "Please try again."
            )
    elif isinstance(exc, requests.HTTPError):
        status_code = exc.response.status_code

        if status_code == 401:
            st.error(
                "Your session is invalid or has expired. "
                "Please log in again."
                )

        elif status_code == 404:
            st.error("The requested resource was not found."
            )

        elif status_code == 422:
            st.error(
                "The submitted data is invalid. "
                "Please check your input."
                )
        elif status_code == 403:
            st.error(
                "You do not have permission to perform this action."
                )
            

        else:
            st.error(
                f"The API returned an error ({status_code})."
                )

    else:
        st.error(f"Unexpected error: {exc}")