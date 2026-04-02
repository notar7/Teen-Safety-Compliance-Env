"""FastAPI server exposing the Teen Safety environment endpoints."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from env.environment import TeenSafetyEnvironment
from env.models import TeenSafetyAction, TeenSafetyObservation, TeenSafetyReward

app = FastAPI(
    title="Teen Safety Compliance Environment",
    description=(
        "OpenEnv-compliant RL environment simulating Meta's Teen Safety Compliance system. "
        "An AI agent reviews content, accounts, and features to protect teenage users "
        "from harmful content, psychological harm, and age fraud on social media platforms."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow CORS so the app is easy to test from browser-based clients.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single shared environment instance.
env = TeenSafetyEnvironment(rng_seed=42)

class StepResponse(BaseModel):
    observation: dict
    reward: dict
    done: bool
    info: dict


class TaskInfo(BaseModel):
    id: str
    name: str
    difficulty: str
    description: str
    expected_score_range: str


@app.get("/", tags=["info"])
def root():
    """Environment info — confirms service is running."""
    return {
        "name": "teen-safety-compliance-env",
        "status": "running",
        "version": "1.0.0",
        "team": "MindMesH",
        "hackathon": "Scaler OpenEnv Hackathon 2026",
        "docs": "/docs",
    }


@app.get("/health", tags=["info"])
def health():
    """Health check endpoint — required for HuggingFace Spaces."""
    return {"status": "healthy"}


@app.get("/tasks", tags=["info"])
def list_tasks():
    """List all available tasks with metadata."""
    return {
        "tasks": [
            {
                "id": "task1_easy",
                "name": "Obvious Content Restriction",
                "difficulty": "easy",
                "description": "Detect and block obviously inappropriate content for teen users",
                "expected_score_range": "0.70 - 1.00",
                "num_scenarios": 10,
            },
            {
                "id": "task2_medium",
                "name": "Subtle Harm Assessment",
                "difficulty": "medium",
                "description": "Assess subtle psychological harm in content targeting teenagers",
                "expected_score_range": "0.40 - 0.80",
                "num_scenarios": 8,
            },
            {
                "id": "task3_hard",
                "name": "Age Misrepresentation Detection",
                "difficulty": "hard",
                "description": "Detect age fraud from behavioral signals alone",
                "expected_score_range": "0.20 - 0.60",
                "num_scenarios": 6,
            },
        ]
    }


@app.post("/reset", response_model=dict, tags=["environment"])
def reset(
    task_id: str = Query(
        default="task1_easy",
        description="Task to run: task1_easy | task2_medium | task3_hard",
    )
):
    """
    Reset the environment and get the initial observation.

    Args:
        task_id: Which task to run (query param)

    Returns:
        TeenSafetyObservation as dict
    """
    valid_tasks = {"task1_easy", "task2_medium", "task3_hard"}
    if task_id not in valid_tasks:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid task_id '{task_id}'. Valid: {sorted(valid_tasks)}",
        )
    observation = env.reset(task_id=task_id)
    return observation.model_dump()


@app.post("/step", response_model=StepResponse, tags=["environment"])
def step(action: TeenSafetyAction):
    """
    Submit an agent action and advance the episode.

    Args:
        action: TeenSafetyAction with decision, confidence, reason, additional_action

    Returns:
        StepResponse with observation, reward, done flag, and info dict
    """
    try:
        observation, reward, done, info = env.step(action)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return StepResponse(
        observation=observation.model_dump(),
        reward=reward.model_dump(),
        done=done,
        info=info,
    )


@app.get("/state", tags=["environment"])
def state():
    """
    Return the current episode state.

    Returns:
        dict with task_id, case_id, step_number, previous_actions, episode_scores
    """
    return env.state()


def main() -> None:
    """Run the FastAPI app on the required Hugging Face Spaces port."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
