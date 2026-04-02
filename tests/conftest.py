import os


def pytest_sessionstart(session):
    """Ensure required env vars exist before importing modules with import-time checks."""
    os.environ.setdefault("OPENAI_API_KEY", "test-api-key")
    os.environ.setdefault("API_BASE_URL", "https://api.groq.com/openai/v1")
    os.environ.setdefault("MODEL_NAME", "llama-3.3-70b-versatile")
