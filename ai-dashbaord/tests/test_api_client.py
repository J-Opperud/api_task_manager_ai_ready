import requests_mock

from api_client import (
    create_task,
    delete_task,
    get_current_user,
    get_task_suggestion,
    get_tasks,
    login,
    update_task,
)


BASE_URL = "http://test-api"
TOKEN = "fake-token"


def test_login():
    with requests_mock.Mocker() as mock:
        mock.post(
            f"{BASE_URL}/auth/login",
            json={
                "access_token": TOKEN,
                "token_type": "bearer",
            },
        )

        result = login(
            BASE_URL,
            "test@example.com",
            "password123",
        )

        assert result["access_token"] == TOKEN
        assert result["token_type"] == "bearer"

        request = mock.last_request

        assert request.json() == {
            "email": "test@example.com",
            "password": "password123",
        }


def test_get_current_user():
    with requests_mock.Mocker() as mock:
        mock.get(
            f"{BASE_URL}/users/me",
            json={
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
            },
        )

        result = get_current_user(
            BASE_URL,
            TOKEN,
        )

        assert result["name"] == "Test User"
        assert result["email"] == "test@example.com"

        request = mock.last_request

        assert request.headers["Authorization"] == (
            f"Bearer {TOKEN}"
        )


def test_get_tasks():
    with requests_mock.Mocker() as mock:
        mock.get(
            f"{BASE_URL}/tasks",
            json=[
                {
                    "id": 1,
                    "title": "Test task",
                    "description": "Test description",
                    "priority": "high",
                    "completed": False,
                }
            ],
        )

        result = get_tasks(
            BASE_URL,
            TOKEN,
        )

        assert len(result) == 1
        assert result[0]["title"] == "Test task"
        assert result[0]["priority"] == "high"

        request = mock.last_request

        assert request.headers["Authorization"] == (
            f"Bearer {TOKEN}"
        )


def test_get_tasks_with_filters():
    with requests_mock.Mocker() as mock:
        mock.get(
            f"{BASE_URL}/tasks",
            json=[],
        )

        result = get_tasks(
            BASE_URL,
            TOKEN,
            completed=False,
            priority="high",
        )

        assert result == []

        request = mock.last_request

        assert request.qs["completed"] == ["false"]
        assert request.qs["priority"] == ["high"]
        assert request.qs["skip"] == ["0"]
        assert request.qs["limit"] == ["100"]


def test_create_task():
    with requests_mock.Mocker() as mock:
        mock.post(
            f"{BASE_URL}/tasks",
            json={
                "id": 1,
                "title": "New task",
                "description": "Test description",
                "priority": "medium",
                "completed": False,
            },
        )

        result = create_task(
            BASE_URL,
            TOKEN,
            title="New task",
            description="Test description",
            priority="medium",
        )

        assert result["id"] == 1
        assert result["title"] == "New task"
        assert result["priority"] == "medium"

        request = mock.last_request

        assert request.headers["Authorization"] == (
            f"Bearer {TOKEN}"
        )

        assert request.json() == {
            "title": "New task",
            "description": "Test description",
            "priority": "medium",
        }


def test_update_task():
    with requests_mock.Mocker() as mock:
        mock.patch(
            f"{BASE_URL}/tasks/1",
            json={
                "id": 1,
                "title": "Updated task",
                "completed": True,
            },
        )

        result = update_task(
            BASE_URL,
            TOKEN,
            1,
            completed=True,
        )

        assert result["completed"] is True

        request = mock.last_request

        assert request.headers["Authorization"] == (
            f"Bearer {TOKEN}"
        )

        assert request.json() == {
            "completed": True,
        }


def test_delete_task():
    with requests_mock.Mocker() as mock:
        mock.delete(
            f"{BASE_URL}/tasks/1",
            status_code=204,
        )

        result = delete_task(
            BASE_URL,
            TOKEN,
            1,
        )

        assert result is None

        request = mock.last_request

        assert request.headers["Authorization"] == (
            f"Bearer {TOKEN}"
        )


def test_get_task_suggestion():
    with requests_mock.Mocker() as mock:
        mock.post(
            f"{BASE_URL}/tasks/1/suggest",
            json={
                "suggestion": (
                    "Break this task into smaller steps."
                )
            },
        )

        result = get_task_suggestion(
            BASE_URL,
            TOKEN,
            1,
        )

        assert "suggestion" in result
        assert result["suggestion"]

        request = mock.last_request

        assert request.headers["Authorization"] == (
            f"Bearer {TOKEN}"
        )
