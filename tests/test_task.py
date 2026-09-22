from app.ai_service import generate_task_suggestion




def test_create_task(client):
    # Register a test user.
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201

    token = response.json()["access_token"]

    # Create a task for that user.
    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Test task",
            "description": "A task created during testing.",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test task"
    assert data["description"] == "A task created during testing."
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert data["user_id"] == 1


#-----------------------------------------------

def test_get_tasks(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "list@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "First task",
            "description": "First test task.",
            "priority": "high",
        },
    )

    client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Second task",
            "description": "Second test task.",
            "priority": "low",
        },
    )

    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 2
    assert tasks[0]["title"] == "First task"
    assert tasks[1]["title"] == "Second task"

#------------------------------------------------
def test_get_tasks_priority_filter(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Priority User",
            "email": "priority@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "High priority task",
            "description": "Important task.",
            "priority": "high",
        },
    )

    client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Low priority task",
            "description": "Less urgent task.",
            "priority": "low",
        },
    )

    response = client.get(
        "/tasks?priority=high",
        headers=headers,
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "High priority task"
    assert tasks[0]["priority"] == "high"

#------------------------------------------------

def test_get_tasks_pagination(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Pagination User",
            "email": "pagination@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    for title in ["Task One", "Task Two", "Task Three"]:
        response = client.post(
            "/tasks",
            headers=headers,
            json={
                "title": title,
                "description": "Pagination test task.",
                "priority": "medium",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/tasks?skip=1&limit=1",
        headers=headers,
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task Two"

#------------------------------------------------

def test_get_tasks_invalid_pagination(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Validation User",
            "email": "validation@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = client.get(
        "/tasks?skip=-1",
        headers=headers,
    )

    assert response.status_code == 422

    response = client.get(
        "/tasks?limit=0",
        headers=headers,
    )

    assert response.status_code == 422

    response = client.get(
        "/tasks?limit=101",
        headers=headers,
    )

    assert response.status_code == 422
#------------------------------------------------

def test_get_task(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Get Task User",
            "email": "gettask@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    create = client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Task to retrieve",
            "description": "Testing the GET by ID endpoint.",
            "priority": "high",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task to retrieve"
    assert data["priority"] == "high"

#-----------------------------------------------


def test_get_task_not_found(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Not Found User",
            "email": "notfound@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    response = client.get(
        "/tasks/9999",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["type"] == "NotFoundException"
    assert data["error"]["detail"] == "Task with id 9999 not found"
    assert data["error"]["status_code"] == 404
#------------------------------------------------

def test_get_task_forbidden_for_other_user(client):
    # Register User A.
    user_a = client.post(
        "/auth/register",
        json={
            "name": "User A",
            "email": "usera@example.com",
            "password": "TestPassword123",
        },
    )

    assert user_a.status_code == 201

    token_a = user_a.json()["access_token"]

    # User A creates a task.
    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
        json={
            "title": "Private task",
            "description": "This belongs to User A.",
            "priority": "high",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    # Register User B.
    user_b = client.post(
        "/auth/register",
        json={
            "name": "User B",
            "email": "userb@example.com",
            "password": "TestPassword123",
        },
    )

    assert user_b.status_code == 201

    token_b = user_b.json()["access_token"]

    # User B tries to access User A's task.
    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token_b}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["error"]["type"] == "ForbiddenException"
    assert data["error"]["detail"] == (
        "You don't have permission to access this task"
    )
    assert data["error"]["status_code"] == 403
#----------------------------------------------



    def test_get_tasks_requires_authentication(client):
        response = client.get("/tasks")

        assert response.status_code == 401


def test_get_task_requires_authentication(client):
    response = client.get("/tasks/1")

    assert response.status_code == 401

def test_get_tasks_requires_authentication(client):
    response = client.get("/tasks")

    assert response.status_code == 401

#-----------------------------------------------

def test_update_task(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Update User",
            "email": "update@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Original task",
            "description": "Original description.",
            "priority": "low",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Updated task",
            "priority": "high",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Updated task"
    assert data["description"] == "Original description."
    assert data["priority"] == "high"
    assert data["completed"] is False


#----------------------------------------------

def test_update_task_not_found(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Missing Task User",
            "email": "missing-update@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    response = client.patch(
        "/tasks/9999",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Updated task",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["type"] == "NotFoundException"
    assert data["error"]["status_code"] == 404

#------------------------------------------------

def test_update_task_forbidden_for_other_user(client):
    first_user = client.post(
        "/auth/register",
        json={
            "name": "First User",
            "email": "first-update@example.com",
            "password": "TestPassword123",
        },
    )

    assert first_user.status_code == 201

    first_token = first_user.json()["access_token"]

    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {first_token}",
        },
        json={
            "title": "Private task",
            "description": "This belongs to the first user.",
            "priority": "low",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    second_user = client.post(
        "/auth/register",
        json={
            "name": "Second User",
            "email": "second-update@example.com",
            "password": "TestPassword123",
        },
    )

    assert second_user.status_code == 201

    second_token = second_user.json()["access_token"]

    response = client.patch(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {second_token}",
        },
        json={
            "title": "Unauthorized update",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["error"]["type"] == "ForbiddenException"
    assert data["error"]["status_code"] == 403


def test_update_task_requires_authentication(client):
    response = client.patch(
        "/tasks/1",
        json={
            "title": "Unauthorized update",
        },
    )

    assert response.status_code == 401

#------------------------------------------------

def test_delete_task(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Delete User",
            "email": "delete@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Task to delete",
            "description": "This task should be deleted.",
            "priority": "medium",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

def test_delete_task(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Delete User",
            "email": "delete@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Task to delete",
            "description": "This task should be deleted.",
            "priority": "medium",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

#-----------------------------------------------

def test_delete_task_forbidden_for_other_user(client):
    first_user = client.post(
        "/auth/register",
        json={
            "name": "First Delete User",
            "email": "first-delete@example.com",
            "password": "TestPassword123",
        },
    )

    assert first_user.status_code == 201

    first_token = first_user.json()["access_token"]

    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {first_token}",
        },
        json={
            "title": "Protected task",
            "description": "Belongs to the first user.",
            "priority": "high",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    second_user = client.post(
        "/auth/register",
        json={
            "name": "Second Delete User",
            "email": "second-delete@example.com",
            "password": "TestPassword123",
        },
    )

    assert second_user.status_code == 201

    second_token = second_user.json()["access_token"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {second_token}",
        },
    )

    assert response.status_code == 403

def test_delete_task_not_found(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Missing Delete User",
            "email": "missing-delete@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    response = client.delete(
        "/tasks/9999",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["type"] == "NotFoundException"
    assert data["error"]["status_code"] == 404

def test_delete_task_requires_authentication(client):
    response = client.delete("/tasks/1")

    assert response.status_code == 401

def test_get_current_user_profile(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Profile User",
            "email": "profile@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
#-----------------------------------------------
    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Profile User"
    assert data["email"] == "profile@example.com"
    assert "id" in data
    assert "is_active" in data
    assert "created_at" in data

    assert "password" not in data
    assert "hashed_password" not in data

def test_get_current_user_requires_authentication(client):
    response = client.get("/users/me")

    assert response.status_code == 401

def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "does-not-exist@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["error"]["type"] == "UnauthorizedException"
    assert data["error"]["detail"] == "Invalid email or password"
    assert data["error"]["status_code"] == 401

def test_generate_task_suggestion(requests_mock):

    requests_mock.post(
        "http://localhost:11434/api/generate",
        json={
            "response": (
                "Break the task into smaller actionable steps."
            )
        },
    )

    result = generate_task_suggestion(
        "Finish database migration"
    )

    assert result == (
        "Break the task into smaller actionable steps."
    )











def test_suggest_task_forbidden_for_other_user(client):
    first_user = client.post(
        "/auth/register",
        json={
            "name": "First AI User",
            "email": "first-ai@example.com",
            "password": "TestPassword123",
        },
    )

    assert first_user.status_code == 201

    first_token = first_user.json()["access_token"]

    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {first_token}",
        },
        json={
            "title": "Private AI task",
            "description": "This task belongs to another user.",
            "priority": "high",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    second_user = client.post(
        "/auth/register",
        json={
            "name": "Second AI User",
            "email": "second-ai@example.com",
            "password": "TestPassword123",
        },
    )

    assert second_user.status_code == 201

    second_token = second_user.json()["access_token"]

    response = client.post(
        f"/tasks/{task_id}/suggest",
        headers={
            "Authorization": f"Bearer {second_token}",
        },
    )

    assert response.status_code == 403

def test_suggest_task_not_found(client):
    register = client.post(
        "/auth/register",
        json={
            "name": "Missing AI User",
            "email": "missing-ai@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    response = client.post(
        "/tasks/9999/suggest",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["type"] == "NotFoundException"
    assert data["error"]["status_code"] == 404






def test_suggest_task(client, monkeypatch):
    def fake_generate_task_suggestion(task_text):
        return "Break this task into smaller actionable steps."

    monkeypatch.setattr(
        "app.routers.tasks.generate_task_suggestion",
        fake_generate_task_suggestion,
    )

    register = client.post(
        "/auth/register",
        json={
            "name": "AI User",
            "email": "ai@example.com",
            "password": "TestPassword123",
        },
    )

    assert register.status_code == 201

    token = register.json()["access_token"]

    create = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "title": "Learn FastAPI",
            "description": (
                "Study dependency injection and authentication."
            ),
            "priority": "high",
        },
    )

    assert create.status_code == 201

    task_id = create.json()["id"]

    response = client.post(
        f"/tasks/{task_id}/suggest",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["suggestion"] == (
        "Break this task into smaller actionable steps."
    )

