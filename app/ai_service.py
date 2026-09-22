import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"


def generate_task_suggestion(task_title: str) -> str:
    """Generate an actionable suggestion for a task."""

    prompt = f"""
You are a helpful task management assistant.

Given the following task:

{task_title}

Provide a concise, practical suggestion for completing it.
Break the task into a few actionable steps when appropriate.
Do not include unnecessary explanation.
""".strip()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]
