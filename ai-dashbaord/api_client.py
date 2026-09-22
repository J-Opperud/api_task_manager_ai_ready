import requests


DEFAULT_TIMEOUT = 10
AI_TIMEOUT = 30


def auth_headers(token):
    """Return authorization headers for a JWT token."""
    return {
        "Authorization": f"Bearer {token}",
        }


def login(base_url, email, password):
    """Authenticate a user and return the JWT response."""
    response = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=DEFAULT_TIMEOUT,
        )

    response.raise_for_status()
    return response.json()


def get_current_user(base_url, token):
    """Return the authenticated user's profile."""
    response = requests.get(
        f"{base_url}/users/me",
        headers=auth_headers(token),
        timeout=DEFAULT_TIMEOUT,
        )

    response.raise_for_status()
    return response.json()


def get_tasks(
    base_url,
    token,
    completed=None,
    priority=None,
    skip=0,
    limit=100,
    ):
    """Return tasks belonging to the authenticated user."""

    params = {
        "skip": skip,
        "limit": limit,
        }

    if completed is not None:
        params["completed"] = completed

    if priority:
        params["priority"] = priority

    response = requests.get(
        f"{base_url}/tasks",
        headers=auth_headers(token),
        params=params,
        timeout=DEFAULT_TIMEOUT,
        )

    response.raise_for_status()
    return response.json()


def create_task(
    base_url,
    token,
    title,
    description="",
    priority="medium",
    ):
    """Create a new task."""

    response = requests.post(
        f"{base_url}/tasks",
        headers=auth_headers(token),
        json={
            "title": title,
            "description": description,
            "priority": priority,
        },
        timeout=DEFAULT_TIMEOUT,
        )

    response.raise_for_status()
    return response.json()


def update_task(
    base_url,
    token,
    task_id,
    **updates,
    ):
    """Partially update an existing task."""

    response = requests.patch(
        f"{base_url}/tasks/{task_id}",
        headers=auth_headers(token),
        json=updates,
        timeout=DEFAULT_TIMEOUT,
        )

    response.raise_for_status()
    return response.json()


def delete_task(base_url, token, task_id):
    """Delete a task."""

    response = requests.delete(
        f"{base_url}/tasks/{task_id}",
        headers=auth_headers(token),
        timeout=DEFAULT_TIMEOUT,
        )

    response.raise_for_status()

    return response.json() if response.content else None


def get_task_suggestion(base_url, token, task_id):
    """Request an AI suggestion for a task."""

    response = requests.post(
        f"{base_url}/tasks/{task_id}/suggest",
        headers=auth_headers(token),
        timeout=AI_TIMEOUT,
        )

    response.raise_for_status()
    return response.json()

