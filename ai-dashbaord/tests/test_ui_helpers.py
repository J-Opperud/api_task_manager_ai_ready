import requests
from unittest.mock import patch

from ui_helpers import display_api_error


def test_display_api_error_connection_error():
    """Connection failures should show a useful message."""

    error = requests.ConnectionError(
        "API unavailable"
        )

    with patch("ui_helpers.st.error") as mock_error:
        display_api_error(error)

    mock_error.assert_called_once_with(
        "Unable to connect to the API. "
        "Make sure the FastAPI server is running."
        )
import requests
import streamlit as st

from ui_helpers import display_api_error


def test_display_api_error_connection_error(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
    )

    display_api_error(
        requests.ConnectionError()
    )

    assert len(messages) == 1
    assert "Unable to connect to the API" in messages[0]


def test_display_api_error_timeout(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
        )

    display_api_error(
        requests.Timeout()
        )

    assert len(messages) == 1
    assert "timed out" in messages[0]


def test_display_api_error_401(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
        )

    response = requests.Response()
    response.status_code = 401

    error = requests.HTTPError(
        "Unauthorized",
        response=response,
        )

    display_api_error(error)

    assert len(messages) == 1
    assert "session is invalid" in messages[0]


def test_display_api_error_403(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
        )

    response = requests.Response()
    response.status_code = 403

    error = requests.HTTPError(
        "Forbidden",
        response=response,
        )

    display_api_error(error)

    assert len(messages) == 1
    assert "permission" in messages[0]


def test_display_api_error_404(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
        )

    response = requests.Response()
    response.status_code = 404

    error = requests.HTTPError(
        "Not Found",
        response=response,
        )

    display_api_error(error)

    assert len(messages) == 1
    assert "not found" in messages[0]


def test_display_api_error_422(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
        )

    response = requests.Response()
    response.status_code = 422

    error = requests.HTTPError(
        "Validation Error",
        response=response,
        )

    display_api_error(error)

    assert len(messages) == 1
    assert "submitted data is invalid" in messages[0]


def test_display_api_error_500(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
        )

    response = requests.Response()
    response.status_code = 500

    error = requests.HTTPError(
        "Server Error",
        response=response,
        )

    display_api_error(error)

    assert len(messages) == 1
    assert "API returned an error (500)" in messages[0]


def test_display_api_error_unexpected_error(monkeypatch):
    messages = []

    monkeypatch.setattr(
        st,
        "error",
        lambda message: messages.append(message),
        )

    display_api_error(
        ValueError("Something unexpected happened")
        )

    assert len(messages) == 1
    assert "Unexpected error" in messages[0]
