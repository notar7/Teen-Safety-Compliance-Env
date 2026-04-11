"""FastAPI server exposing the Teen Safety environment endpoints."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from env.environment import TeenSafetyEnvironment, get_task_catalog, get_task_ids
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


def _clamp_open_unit_interval(value: float) -> float:
    """Clamp numeric values to strict open interval (0, 1)."""
    return round(min(max(float(value), 0.01), 0.99), 4)

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
    return {"tasks": get_task_catalog()}


@app.post("/reset", response_model=dict, tags=["environment"])
def reset(
    task_id: str = Query(
        default="task1_easy",
        description="Task to run (see /tasks)",
    )
):
    """
    Reset the environment and get the initial observation.

    Args:
        task_id: Which task to run (query param)

    Returns:
        TeenSafetyObservation as dict
    """
    valid_tasks = set(get_task_ids())
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

    reward_payload = reward.model_dump()
    reward_payload["score"] = _clamp_open_unit_interval(reward_payload.get("score", 0.5))

    info_payload = dict(info)
    if "episode_reward" in info_payload:
        info_payload["episode_reward"] = _clamp_open_unit_interval(info_payload["episode_reward"])

    return StepResponse(
        observation=observation.model_dump(),
        reward=reward_payload,
        done=done,
        info=info_payload,
    )


@app.get("/state", tags=["environment"])
def state():
    """
    Return the current episode state.

    Returns:
        dict with task_id, case_id, step_number, previous_actions, episode_scores
    """
    st = env.state()
    if "episode_scores" in st and isinstance(st["episode_scores"], list):
        st["episode_scores"] = [_clamp_open_unit_interval(s) for s in st["episode_scores"]]
    return st


def main() -> None:
    """Run the FastAPI app on the required Hugging Face Spaces port."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
