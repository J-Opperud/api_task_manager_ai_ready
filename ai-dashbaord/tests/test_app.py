from pathlib import Path

from streamlit.testing.v1 import AppTest

import api_client


def get_app():
    """Return a Streamlit AppTest instance."""

    app_path = Path(__file__).parent.parent / "app.py"

    return AppTest.from_file(app_path)


def test_login_page():
    app = get_app()

    app.run()

    # The app should start on the login page.
    assert app.title[0].value == "🤖 Task Dashboard"

    assert len(app.text_input) == 2

    assert app.text_input[0].label == "Email"
    assert app.text_input[1].label == "Password"

    assert any(
        button.label == "Login"
        for button in app.button
    )


def test_successful_login(monkeypatch):
    def fake_login(base_url, email, password):
        assert email == "test@example.com"
        assert password == "password123"

        return {
            "access_token": "fake-jwt-token",
        }

    def fake_get_current_user(base_url, token):
        assert token == "fake-jwt-token"

        return {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
        }

    monkeypatch.setattr(
        api_client,
        "login",
        fake_login,
    )

    monkeypatch.setattr(
        api_client,
        "get_current_user",
        fake_get_current_user,
    )

    app = get_app()

    app.run()

    app.text_input[0].input(
        "test@example.com"
    )

    app.text_input[1].input(
        "password123"
    )

    login_button = next(
        button
        for button in app.button
        if button.label == "Login"
    )

    login_button.click()

    app.run()

    assert app.session_state["token"] == (
        "fake-jwt-token"
    )

    assert app.session_state["username"] == (
        "Test User"
    )

    assert any(
        "Welcome, Test User!" in message.value
        for message in app.success
    )


def test_logout_clears_session(monkeypatch):
    def fake_login(base_url, email, password):
        return {
            "access_token": "fake-jwt-token",
        }

    def fake_get_current_user(base_url, token):
        return {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
        }

    def fake_get_tasks(
        base_url,
        token,
        completed=None,
        priority=None,
        skip=0,
        limit=100,
    ):
        return []

    monkeypatch.setattr(
        api_client,
        "login",
        fake_login,
    )

    monkeypatch.setattr(
        api_client,
        "get_current_user",
        fake_get_current_user,
    )

    monkeypatch.setattr(
        api_client,
        "get_tasks",
        fake_get_tasks,
    )

    app = get_app()

    # Start on the login page.
    app.run()

    app.text_input[0].input(
        "test@example.com"
    )

    app.text_input[1].input(
        "password123"
    )

    login_button = next(
        button
        for button in app.button
        if button.label == "Login"
    )

    login_button.click()

    app.run()

    # Confirm authenticated state.
    assert app.session_state["token"] == (
        "fake-jwt-token"
    )

    assert app.session_state["username"] == (
        "Test User"
    )

    # Logout.
    logout_button = next(
        button
        for button in app.button
        if button.label == "Logout"
    )

    logout_button.click()

    app.run()

    # Authentication should be cleared.
    assert app.session_state["token"] is None
    assert app.session_state["username"] is None

    # Login page should be visible again.
    assert any(
        button.label == "Login"
        for button in app.button
    )
