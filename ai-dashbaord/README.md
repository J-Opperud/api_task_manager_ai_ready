 AI Task Dashboard

## overview

A Streamlit frontend for the AI-Ready Task Manager API.

The dashboard connects to a FastAPI backend and provides authentication, task management, filtering, dashboard metrics, data visualization, and an AI-powered task suggestion feature using Ollama and Llama 3.2.

## Architecture

Project Structure
ai-dashboard/
├── app.py
├── api_client.py
├── ui_helpers.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml

┌─────────────────────────────┐
│       Streamlit UI          │
│          app.py             │
└──────────────┬──────────────┘
               │
               │ HTTP / JWT
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│       Task Manager API      │
└──────────────┬──────────────┘
               │
               │ AI request
               ▼
┌─────────────────────────────┐
│           Ollama            │
│      localhost:11434        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Llama 3.2            │
│       Local AI Model        │
└─────────────────────────────┘



## Features
- Authentication

- Login using email and password

- JWT authentication

- JWT token stored in Streamlit session state

- Logged-in user displayed in the sidebar

- Logout functionality

- Authentication errors displayed to the user

## Dashboard

The dashboard provides:

- Total task count

- Completed task count

- Remaining task count

- Task data displayed in a table

- Task completion visualization using Plotly

- Status and priority filtering

## Task Management

Users can:

- Create new tasks

- Set task descriptions

- Set task priority

- Mark tasks as completed

- Delete tasks

- Filter tasks by status

- Filter tasks by priority

## AI Task Suggestions

The dashboard includes an AI-powered suggestion feature.

When the user selects AI Suggestion, the frontend sends the task ID to the FastAPI backend:

POST /tasks/{task_id}/suggest


The backend sends the task information to a locally running Ollama model.

The current model is:

llama3.2


The generated suggestion is then returned to Streamlit and displayed to the user.


## Requirements

Python 3.11+

Streamlit

Requests

Plotly

A running instance of the FastAPI Task Manager API

Ollama for the AI suggestion feature

Llama 3.2 model

## Installation

Create and activate a virtual environment:

python -m venv venv


Windows:

venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

Configuration

Create:

.streamlit/secrets.toml


Add the FastAPI backend URL:

API_URL = <"inscert">


.streamlit/secrets.toml

Running the Application
1. Start the FastAPI backend

From the backend project:

uvicorn app.main:app --reload


The API should be available at:



2. Start Ollama

Make sure Ollama is installed and running.

Verify that the model is available:

ollama list


If necessary, download Llama 3.2:

ollama pull llama3.2


Test the model:

ollama run llama3.2

3. Start Streamlit



## Testing

The backend API tests can be run with:

python -m pytest tests -v


The AI integration is mocked during automated testing so that the test suite does not require Ollama to be running.

The real Ollama connection is tested when running the application.

## Security 

JWT tokens are kept in Streamlit session state.

API authentication uses the Authorization: Bearer <token> header.

API secrets should not be committed to source control.

Ollama runs locally and does not require an external AI API key for this application.



