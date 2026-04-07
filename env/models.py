from pydantic import BaseModel, Field
from typing import Optional


class TeenSafetyObservation(BaseModel):
    """
    What the agent sees — the current case to review.
    """
    case_id: str = Field(..., description="Unique case identifier")
    case_type: str = Field(
        ...,
        description="Type of case: 'content_review' | 'age_verification' | 'harm_assessment'"
    )
    content: dict = Field(..., description="The actual content/account/feature to review")
    user_profile: dict = Field(..., description="Information about the user involved")
    platform_context: str = Field(
        ...,
        description="Which platform: 'instagram' | 'facebook' | 'threads'"
    )
    previous_actions: list[str] = Field(
        default_factory=list,
        description="History of actions taken this episode"
    )
    step_number: int = Field(..., description="Current step in episode")
    task_id: str = Field(
        ...,
        description="Which task: 'task1_easy' | 'task2_medium' | 'task3_hard'"
    )
    instructions: str = Field(..., description="Clear instructions for what agent must do")


class TeenSafetyAction(BaseModel):
    """
    What the agent can do — a compliance decision.
    """
    decision: str = Field(
        ...,
        description="Decision: 'allow' | 'restrict' | 'block' | 'escalate' | 'request_verification'"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How confident the agent is (0.0 to 1.0)"
    )
    reason: str = Field(..., description="Explanation for the decision")
    additional_action: Optional[str] = Field(
        default=None,
        description="Optional: 'add_warning_label' | 'notify_parent' | 'age_gate'"
    )


class TeenSafetyReward(BaseModel):
    """
    Reward signal returned after each step.
    """
    score: float = Field(..., gt=0.0, lt=1.0, description="Reward score strictly between 0.0 and 1.0")
    breakdown: dict = Field(..., description="Detailed scoring breakdown")
    feedback: str = Field(..., description="Human-readable feedback for the agent")
