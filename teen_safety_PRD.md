# 🛡️ Teen Safety Compliance Environment — Full PRD
### Scaler OpenEnv Hackathon 2026
**Team:** MindMesH
**Members:** Ashish Ransing (Lead) + Riyanshi Verma
**Deadline:** 8 April 2026, 11:59 PM IST
**Framework:** OpenEnv

---

## 📌 TABLE OF CONTENTS
1. [Project Overview](#1-project-overview)
2. [Why This Problem](#2-why-this-problem)
3. [Hackathon Rules & Guidelines](#3-hackathon-rules--guidelines)
4. [Evaluation Criteria](#4-evaluation-criteria)
5. [Tech Stack](#5-tech-stack)
6. [Environment Design](#6-environment-design)
7. [Project Structure](#7-project-structure)
8. [Phase-by-Phase Build Plan](#8-phase-by-phase-build-plan)
9. [Member 1 — Ashish Ransing](#9-member-1--ashish-ransing-team-lead)
10. [Member 2 — Riyanshi Verma](#10-member-2--riyanshi-verma)
11. [Submission Checklist](#11-submission-checklist)
12. [Vibe Coder Prompts](#12-vibe-coder-prompts)

---

## 1. PROJECT OVERVIEW

### What Are We Building?
A complete **OpenEnv-compliant reinforcement learning environment** that simulates Meta's Teen Safety Compliance system.

An AI agent interacts with this environment to learn how to:
- Review content shown to teenage users (under 18)
- Detect age misrepresentation on social media platforms
- Assess subtle psychological harm in content targeting teens
- Make correct compliance decisions based on platform safety policies

### One Line Description
> "An RL environment where an AI agent learns to protect teenage users on social media platforms by detecting harmful content, age fraud, and policy violations — simulating the real compliance challenges Meta faces today."

### Real World Context
- Meta paid **$1.4 billion settlement** for teen privacy violations (2024)
- US Congress passed the **Kids Online Safety Act** targeting platforms like Instagram
- Instagram is under **active Senate investigation** for teen mental health harm
- Meta has an entire internal team dedicated to Teen Safety Compliance
- This environment simulates their exact decision-making pipeline

---

## 2. WHY THIS PROBLEM

| Factor | Details |
|--------|---------|
| **Real-world utility** | Meta faces this EXACT problem daily — protecting 400M+ teen users |
| **Legal urgency** | Laws being passed RIGHT NOW in USA & EU about teen online safety |
| **Novelty** | No existing OpenEnv environment for teen safety compliance |
| **Clear grading** | Decisions are binary + graduated — easy to build deterministic graders |
| **Meta relevance** | Meta judges will immediately recognize this as a real internal problem |
| **Difficulty range** | Natural easy → hard progression built into the problem domain |

---

## 3. HACKATHON RULES & GUIDELINES

### Must Follow — Or Get Disqualified
- [ ] Environment must simulate a **real-world task** (NOT a game or toy)
- [ ] Must implement **full OpenEnv spec** with typed Pydantic models
- [ ] `step(action)` → returns observation, reward, done, info
- [ ] `reset()` → returns initial observation
- [ ] `state()` → returns current state
- [ ] `openenv.yaml` file with metadata must exist
- [ ] Must pass `openenv validate` command
- [ ] **Minimum 3 tasks** with agent graders (easy → medium → hard)
- [ ] Each grader scores **0.0 to 1.0**
- [ ] Graders must be **deterministic and reproducible**
- [ ] Reward function must provide **partial progress signals** (NOT binary)
- [ ] Baseline inference script named exactly **`inference.py`** in root directory
- [ ] Uses **OpenAI client** format for LLM calls
- [ ] Must deploy to **HuggingFace Spaces** tagged with `openenv`
- [ ] Must include working **Dockerfile**
- [ ] Inference runtime **< 20 minutes**
- [ ] Must run on **vCPU=2, memory=8GB** machine

### Environment Variables Required
```bash
API_BASE_URL=https://api.groq.com/openai/v1   # or any OpenAI-compatible endpoint
MODEL_NAME=llama-3.3-70b-versatile             # model to use
HF_TOKEN=your_huggingface_token                # for deployment
OPENAI_API_KEY=your_groq_or_openai_key         # API key
```

### Confirmed by Organizers
> Using OpenAI-compatible APIs like **Groq or Gemini** is allowed as long as:
> - Runs reliably without errors
> - Produces reproducible results
> - Works smoothly during evaluation

### Submission Steps
1. Push code to GitHub
2. Deploy to HuggingFace Spaces
3. Run `openenv validate` — must pass
4. Submit HF Spaces URL on platform before **8 April 11:59 PM IST**

---

## 4. EVALUATION CRITERIA

### Scoring Breakdown

| Parameter | Weight | What Judges Look For |
|-----------|--------|----------------------|
| **Real-world utility** | 30% | Does it model a genuine task? Would someone use this to train agents? |
| **Task & grader quality** | 25% | Well-defined objectives? Fair graders? Meaningful difficulty progression? |
| **Environment design** | 20% | Clean state, good action/observation spaces, useful reward shaping |
| **Code quality & spec** | 15% | OpenEnv spec followed, clean structure, typed models, Docker works |
| **Creativity & novelty** | 10% | Domain not seen before in OpenEnv, clever reward design |

### Real-world Utility Scoring Scale
- **0–5**: Toy/artificial problem — no practical application
- **6–15**: Valid domain but shallow modeling
- **16–25**: Good domain modeling, useful for agent evaluation
- **26–30**: Excellent — fills real gap, immediate value for RL community

### How Judging Works (3 Stages)
1. **Pass/Fail Gate** — HF Space deploys, OpenEnv spec, Docker builds, baseline reproduces, 3+ tasks
2. **Scored** — Baseline agent re-run, Nemotron 3 Super LLM run against environment
3. **Top Submissions** — Reviewed by **Meta and HuggingFace engineers** personally

### Disqualification Criteria
- Environment does not deploy or respond
- Plagiarized or trivially modified existing environments
- Graders that always return the same score
- No baseline inference script

---

## 5. TECH STACK

### Core Framework
```
openenv-core          # The OpenEnv framework — MUST USE
pydantic              # For typed models (Observation, Action, Reward)
fastapi               # To serve the environment as an API
uvicorn               # ASGI server
```

### AI / LLM
```
openai                # OpenAI client library (used for Groq/OpenAI calls)
# API: Groq (free) or OpenAI
# Model: llama-3.3-70b-versatile (Groq) or gpt-4o-mini (OpenAI)
```

### Infrastructure
```
docker                # Containerization
huggingface_hub       # HuggingFace deployment
python-dotenv         # Environment variable management
```

### Development
```
Python 3.11           # Recommended version
uv                    # Fast Python package manager (used by OpenEnv)
pytest                # Testing
```

### Installation Commands
```bash
# Install uv first
pip install uv

# Install OpenEnv
pip install openenv-core

# Install other dependencies
pip install openai pydantic fastapi uvicorn python-dotenv huggingface_hub pytest
```

---

## 6. ENVIRONMENT DESIGN

### Environment Name
`teen-safety-compliance-env`

### What The Environment Simulates
The agent plays the role of Meta's automated Teen Safety Compliance system. It receives cases — content, accounts, or features — and must make safety decisions to protect teenage users.

### Observation Space (What Agent Sees)
```python
class TeenSafetyObservation(BaseModel):
    case_id: str                    # Unique case identifier
    case_type: str                  # "content_review" | "age_verification" | "harm_assessment"
    content: dict                   # The actual content/account/feature to review
    user_profile: dict              # Information about the user involved
    platform_context: str           # Which platform: "instagram" | "facebook" | "threads"
    previous_actions: list[str]     # History of actions taken this episode
    step_number: int                # Current step in episode
    task_id: str                    # Which task: "task1_easy" | "task2_medium" | "task3_hard"
    instructions: str               # Clear instructions for what agent must do
```

### Action Space (What Agent Can Do)
```python
class TeenSafetyAction(BaseModel):
    decision: str                   # "allow" | "restrict" | "block" | "escalate" | "request_verification"
    confidence: float               # 0.0 to 1.0 — how confident agent is
    reason: str                     # Explanation for the decision
    additional_action: str | None   # Optional: "add_warning_label" | "notify_parent" | "age_gate"
```

### Reward Model
```python
class TeenSafetyReward(BaseModel):
    score: float                    # 0.0 to 1.0
    breakdown: dict                 # Detailed scoring breakdown
    feedback: str                   # Human-readable feedback
```

### Reward Function Logic
```
CORRECT DECISION:
+1.0  → Perfect decision + correct reason + right additional action
+0.8  → Correct decision + correct reason
+0.6  → Correct decision but wrong/missing reason
+0.3  → Partially correct (right category, wrong severity)

WRONG DECISION:
-0.3  → Over-restriction (blocked safe content — false positive)
-0.5  → Under-restriction (allowed mildly harmful content)
-0.8  → Missed clearly harmful content shown to teen
-1.0  → Gave teen access to adult content / missed age fraud

PARTIAL PROGRESS SIGNALS:
+0.1  → Correctly identified the content category
+0.1  → Correctly identified the user is a teen
+0.1  → Correctly identified the platform context
```

---

## 7. THE 3 TASKS

### TASK 1 — Easy: Obvious Content Restriction
**Difficulty:** 🟢 Easy
**Description:** Agent reviews content that is obviously inappropriate for teen users and must make a clear restriction decision.

**Scenario Examples:**
```python
# Scenario A — Alcohol Advertisement
{
    "content_type": "advertisement",
    "text": "Get 20% off your first order of premium whiskey! Limited time offer.",
    "image_tags": ["alcohol", "bottle", "adults"],
    "advertiser_category": "alcohol_brand",
    "target_audience_set_by_advertiser": "18+"
}
# Correct Decision: block + add_warning_label
# User Profile: age=15, platform=instagram

# Scenario B — Gambling Promotion
{
    "content_type": "sponsored_post",
    "text": "Win big tonight! Join our online casino — $500 welcome bonus!",
    "image_tags": ["casino", "money", "gambling"],
    "link_domain": "onlinecasino.com"
}
# Correct Decision: block
# User Profile: age=16, platform=facebook
```

**Grader Logic:**
```python
def grade_task1(action: TeenSafetyAction, ground_truth: dict) -> float:
    score = 0.0
    if action.decision == ground_truth["correct_decision"]:
        score += 0.7
    if action.confidence >= 0.8:  # Should be highly confident on easy cases
        score += 0.15
    if action.reason and len(action.reason) > 10:
        score += 0.15
    return min(score, 1.0)
```

**Expected Score Range:** 0.7 — 1.0 for a good agent

---

### TASK 2 — Medium: Subtle Psychological Harm Assessment
**Difficulty:** 🟡 Medium
**Description:** Agent reviews content that isn't explicitly adult but poses subtle psychological harm risks to teenagers — like extreme diet culture, dangerous fitness trends, or manipulative content.

**Scenario Examples:**
```python
# Scenario A — Extreme Diet Content
{
    "content_type": "reel",
    "caption": "How I lost 20kg in 6 weeks eating only 500 calories a day! DM me for my plan 🔥",
    "hashtags": ["weightloss", "diet", "transformation", "thinspiration"],
    "creator_follower_count": 250000,
    "engagement_rate": 0.08,
    "comments_sample": ["goals!", "I want to try this", "you look amazing"]
}
# Correct Decision: restrict + add_warning_label
# NOT block — content needs warning, not full removal
# User Profile: age=14, gender=female, platform=instagram

# Scenario B — Dangerous Challenge
{
    "content_type": "video",
    "description": "The 72-hour fast challenge — day 3 update. Feeling dizzy but pushing through!",
    "video_length_seconds": 180,
    "view_count": 1200000,
    "trending_hashtag": "#fastingchallenge"
}
# Correct Decision: restrict + add_warning_label + escalate
# User Profile: age=15, platform=instagram
```

**Grader Logic:**
```python
def grade_task2(action: TeenSafetyAction, ground_truth: dict) -> float:
    score = 0.0
    if action.decision == ground_truth["correct_decision"]:
        score += 0.5
    elif action.decision in ground_truth["acceptable_decisions"]:
        score += 0.3  # Partial credit for acceptable alternatives
    if ground_truth["requires_label"] and action.additional_action == "add_warning_label":
        score += 0.2
    if action.reason and any(keyword in action.reason.lower() 
                             for keyword in ground_truth["expected_keywords"]):
        score += 0.2
    if action.confidence >= 0.6 and action.confidence <= 0.85:  # Should not be overconfident
        score += 0.1
    return min(score, 1.0)
```

**Expected Score Range:** 0.4 — 0.8 for a good agent

---

### TASK 3 — Hard: Age Misrepresentation Detection
**Difficulty:** 🔴 Hard
**Description:** Agent must detect when a user has lied about their age to access adult features on the platform. The agent only has behavioral signals — no direct age proof. Must make decision purely from patterns.

**Scenario Examples:**
```python
# Scenario A — Behavioral Age Signals
{
    "account_info": {
        "declared_age": 22,
        "account_created": "2023-01-15",
        "profile_bio": "just vibing 😊"
    },
    "behavioral_signals": {
        "posting_times": ["3pm", "4pm", "8pm", "weekends_heavy"],
        "content_interests": ["minecraft", "roblox", "school_memes", "teen_drama_shows"],
        "language_patterns": ["no cap", "bussin", "slay", "periodt", "its giving"],
        "engagement_patterns": "high engagement with teen content creators",
        "reported_by_peers": 3,
        "follows_teen_influencers": True,
        "parent_account_linked": False
    },
    "requested_feature": "access_to_adult_dating_features"
}
# Correct Decision: request_verification + restrict (deny adult features)
# Agent must infer user is likely underage despite claiming 22

# Scenario B — Subtle Signals
{
    "account_info": {
        "declared_age": 19,
        "account_created": "2024-08-20",  # August — typical school year start
    },
    "behavioral_signals": {
        "posting_times": ["7am", "8am", "3pm", "10pm"],  # School schedule
        "mentions": ["school", "exams", "homework", "teacher"],
        "group_memberships": ["Class of 2026", "High School Memes"],
        "location_tags": ["high school name"],
    },
    "requested_feature": "disable_parental_supervision_mode"
}
# Correct Decision: request_verification + block feature access
```

**Grader Logic:**
```python
def grade_task3(action: TeenSafetyAction, ground_truth: dict) -> float:
    score = 0.0
    # Core decision
    if action.decision == ground_truth["correct_decision"]:
        score += 0.4
    # Must request verification — not just block outright
    if "request_verification" in action.decision or action.additional_action == "request_verification":
        score += 0.2
    # Evidence-based reasoning
    signals_mentioned = sum(1 for signal in ground_truth["key_signals"] 
                           if signal in action.reason.lower())
    score += min(signals_mentioned * 0.1, 0.3)  # Up to 0.3 for citing evidence
    # Appropriate confidence — should NOT be overconfident on hard cases
    if action.confidence <= 0.75:
        score += 0.1
    return min(score, 1.0)
```

**Expected Score Range:** 0.2 — 0.6 for a good agent (hard task should challenge frontier models)

---

## 8. PROJECT STRUCTURE

```
teen-safety-compliance-env/
│
├── 📄 inference.py              ← MUST be in root, named exactly this
├── 📄 openenv.yaml              ← Environment metadata
├── 📄 Dockerfile                ← Container config
├── 📄 requirements.txt          ← Python dependencies
├── 📄 README.md                 ← Documentation
├── 📄 .env.example              ← Example environment variables
│
├── 📁 env/
│   ├── __init__.py
│   ├── environment.py           ← Main environment class
│   ├── models.py                ← Pydantic models (Observation, Action, Reward)
│   ├── state_manager.py         ← State management
│   └── reward.py                ← Reward function logic
│
├── 📁 tasks/
│   ├── __init__.py
│   ├── task1_easy.py            ← Easy task scenarios + grader
│   ├── task2_medium.py          ← Medium task scenarios + grader
│   ├── task3_hard.py            ← Hard task scenarios + grader
│   └── scenario_generator.py   ← Generates synthetic scenarios
│
├── 📁 server/
│   ├── __init__.py
│   └── app.py                   ← FastAPI server
│
└── 📁 tests/
    ├── test_environment.py
    ├── test_graders.py
    └── test_inference.py
```

---

## 9. PHASE-BY-PHASE BUILD PLAN

### 8 Phases Total — Divided Between 2 Members

---

## MEMBER 1 — ASHISH RANSING (Team Lead)
### Phases 1, 2, 3, 4

---

### PHASE 1 — Project Setup & Core Models
**Owner:** Ashish
**Timeline:** Day 1 (3-4 hours)
**Goal:** Get the project skeleton running

#### What to Build:
1. Initialize OpenEnv project
2. Create all Pydantic models
3. Set up folder structure
4. Create `openenv.yaml`

#### Step by Step:
```bash
# 1. Install dependencies
pip install openenv-core pydantic fastapi uvicorn python-dotenv openai

# 2. Initialize project
openenv init teen-safety-compliance-env
cd teen-safety-compliance-env

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
```

#### Code to Write — `env/models.py`:
```python
from pydantic import BaseModel
from typing import Optional

class TeenSafetyObservation(BaseModel):
    case_id: str
    case_type: str  # "content_review" | "age_verification" | "harm_assessment"
    content: dict
    user_profile: dict
    platform_context: str  # "instagram" | "facebook" | "threads"
    previous_actions: list[str]
    step_number: int
    task_id: str
    instructions: str

class TeenSafetyAction(BaseModel):
    decision: str  # "allow" | "restrict" | "block" | "escalate" | "request_verification"
    confidence: float  # 0.0 to 1.0
    reason: str
    additional_action: Optional[str] = None  # "add_warning_label" | "notify_parent" | "age_gate"

class TeenSafetyReward(BaseModel):
    score: float  # 0.0 to 1.0
    breakdown: dict
    feedback: str
```

#### Code to Write — `openenv.yaml`:
```yaml
name: teen-safety-compliance-env
version: "1.0.0"
description: >
  An RL environment simulating Meta's Teen Safety Compliance system.
  An AI agent reviews content, accounts, and features to protect teenage
  users on social media platforms from harmful content and policy violations.
author: Team MindMesH
tags:
  - openenv
  - content-moderation
  - teen-safety
  - social-media
  - compliance
tasks:
  - id: task1_easy
    name: Obvious Content Restriction
    difficulty: easy
    description: Detect and restrict obviously inappropriate content for teen users
  - id: task2_medium
    name: Subtle Harm Assessment
    difficulty: medium
    description: Assess subtle psychological harm in content targeting teenagers
  - id: task3_hard
    name: Age Misrepresentation Detection
    difficulty: hard
    description: Detect age fraud from behavioral signals alone
observation_space: TeenSafetyObservation
action_space: TeenSafetyAction
reward_range: [0.0, 1.0]
```

#### Vibe Coder Prompt for Phase 1:
```
Build a Python OpenEnv project called "teen-safety-compliance-env".

Create this exact folder structure:
teen-safety-compliance-env/
├── inference.py (empty for now)
├── openenv.yaml
├── Dockerfile (empty for now)
├── requirements.txt
├── env/__init__.py
├── env/models.py
├── tasks/__init__.py
├── server/__init__.py
└── tests/__init__.py

In env/models.py create these exact Pydantic v2 models:
1. TeenSafetyObservation with fields: case_id(str), case_type(str), content(dict), 
   user_profile(dict), platform_context(str), previous_actions(list[str]), 
   step_number(int), task_id(str), instructions(str)

2. TeenSafetyAction with fields: decision(str), confidence(float), reason(str), 
   additional_action(Optional[str])

3. TeenSafetyReward with fields: score(float), breakdown(dict), feedback(str)

In openenv.yaml add the metadata as described.
In requirements.txt add: openenv-core, pydantic, fastapi, uvicorn, openai, python-dotenv
```

---

### PHASE 2 — Task 1 (Easy) + Grader
**Owner:** Ashish
**Timeline:** Day 2 (3-4 hours)
**Goal:** Build first task with working grader

#### What to Build:
- 10+ synthetic scenarios for Task 1
- Grader function that scores 0.0-1.0
- Deterministic and reproducible results

#### Code to Write — `tasks/task1_easy.py`:
```python
TASK1_SCENARIOS = [
    {
        "case_id": "T1_001",
        "case_type": "content_review",
        "content": {
            "content_type": "advertisement",
            "text": "Get 20% off premium whiskey! Limited time offer.",
            "tags": ["alcohol", "adults_only"],
            "advertiser_category": "alcohol_brand"
        },
        "user_profile": {"declared_age": 15, "account_verified": False},
        "platform_context": "instagram",
        "ground_truth": {
            "correct_decision": "block",
            "acceptable_decisions": ["block", "restrict"],
            "correct_additional_action": "add_warning_label",
            "minimum_confidence": 0.8,
            "explanation": "Alcohol advertising must not be shown to users under 18"
        }
    },
    # Add 9 more scenarios covering: gambling, adult content, weapons sales,
    # tobacco, explicit violence, adult dating apps, adult movies
]

def grade_task1(action, ground_truth) -> float:
    score = 0.0
    if action["decision"] == ground_truth["correct_decision"]:
        score += 0.7
    elif action["decision"] in ground_truth["acceptable_decisions"]:
        score += 0.4
    if action["confidence"] >= ground_truth["minimum_confidence"]:
        score += 0.15
    if action["reason"] and len(action["reason"]) > 20:
        score += 0.15
    return round(min(score, 1.0), 2)
```

#### Vibe Coder Prompt for Phase 2:
```
In tasks/task1_easy.py, create a TASK1_SCENARIOS list with 10 realistic scenarios 
where content is OBVIOUSLY inappropriate for teenage users (under 18).

Scenarios must cover these categories (one each minimum):
- Alcohol advertisement
- Gambling promotion  
- Tobacco/vaping product
- Adult dating app promotion
- Explicit violence in game ad
- Adult movie trailer
- Online casino
- Weapons/firearms sale
- Adult entertainment subscription
- Extreme sports with no safety warnings

Each scenario must be a dict with:
- case_id: "T1_001" through "T1_010"
- case_type: "content_review"
- content: dict with content_type, text, tags, advertiser_category
- user_profile: dict with declared_age (13-17), platform
- platform_context: one of "instagram", "facebook", "threads"
- ground_truth: dict with correct_decision, acceptable_decisions, 
  correct_additional_action, minimum_confidence, explanation

Then write a grade_task1(action: dict, ground_truth: dict) -> float function
that scores 0.0-1.0 based on:
- 0.7 for correct decision
- 0.4 for acceptable alternative decision
- 0.15 for appropriate confidence level
- 0.15 for non-empty reason

Make it fully deterministic — same input always gives same output.
```

---

### PHASE 3 — Task 2 (Medium) + Grader
**Owner:** Ashish
**Timeline:** Day 3 (4 hours)
**Goal:** Build medium difficulty task

#### What to Build:
- 8+ synthetic scenarios for Task 2
- More nuanced grader with partial credit
- Scenarios involving subtle harm

#### Vibe Coder Prompt for Phase 3:
```
In tasks/task2_medium.py create TASK2_SCENARIOS with 8 scenarios of SUBTLE 
psychological harm content targeting teen users.

Scenarios must cover:
- Extreme diet/weight loss content (not explicit but harmful)
- Dangerous fitness challenge trending on platform
- Influencer promoting unhealthy body image
- Financial scam targeting teens (crypto, MLM)
- Cyberbullying adjacent content
- Predatory parasocial relationship content
- Mental health misinformation (fake depression cures)
- Dangerous viral challenge (fasting, skipping sleep)

Each scenario dict needs:
- case_id, case_type: "harm_assessment", content (detailed dict), 
  user_profile (age 13-17, gender, interests), platform_context
- ground_truth with: correct_decision, acceptable_decisions list, 
  requires_label(bool), expected_keywords list (words that should appear 
  in agent's reason), explanation

Write grade_task2(action, ground_truth) -> float:
- 0.5 for correct decision
- 0.3 for acceptable alternative
- 0.2 if requires_label and agent added warning label
- 0.2 if agent's reason contains any expected_keywords
- 0.1 if confidence is between 0.5-0.85 (not overconfident on subtle cases)
- Cap at 1.0
```

---

### PHASE 4 — Main Environment Class
**Owner:** Ashish
**Timeline:** Day 4 (4-5 hours)
**Goal:** Build the core environment that ties everything together

#### Code to Write — `env/environment.py`:
```python
from openenv import BaseEnvironment
from env.models import TeenSafetyObservation, TeenSafetyAction, TeenSafetyReward
from env.state_manager import StateManager
from env.reward import RewardCalculator
from tasks.task1_easy import TASK1_SCENARIOS, grade_task1
from tasks.task2_medium import TASK2_SCENARIOS, grade_task2
from tasks.task3_hard import TASK3_SCENARIOS, grade_task3
import random

class TeenSafetyEnvironment(BaseEnvironment):
    def __init__(self):
        self.state_manager = StateManager()
        self.reward_calculator = RewardCalculator()
        self.current_task = None
        self.current_scenario = None
        self.step_count = 0
        self.max_steps = 5
        self.episode_reward = 0.0

    def reset(self, task_id: str = "task1_easy") -> TeenSafetyObservation:
        """Reset environment and return initial observation"""
        self.step_count = 0
        self.episode_reward = 0.0
        self.current_task = task_id
        
        # Select scenario based on task
        scenarios = {
            "task1_easy": TASK1_SCENARIOS,
            "task2_medium": TASK2_SCENARIOS,
            "task3_hard": TASK3_SCENARIOS
        }
        
        scenario_list = scenarios[task_id]
        self.current_scenario = random.choice(scenario_list)
        self.state_manager.set_state(self.current_scenario, task_id)
        
        return TeenSafetyObservation(
            case_id=self.current_scenario["case_id"],
            case_type=self.current_scenario["case_type"],
            content=self.current_scenario["content"],
            user_profile=self.current_scenario["user_profile"],
            platform_context=self.current_scenario["platform_context"],
            previous_actions=[],
            step_number=0,
            task_id=task_id,
            instructions=self._get_instructions(task_id)
        )

    def step(self, action: TeenSafetyAction):
        """Process agent action and return next observation, reward, done, info"""
        self.step_count += 1
        
        # Grade the action
        graders = {
            "task1_easy": grade_task1,
            "task2_medium": grade_task2,
            "task3_hard": grade_task3
        }
        
        grader = graders[self.current_task]
        ground_truth = self.current_scenario["ground_truth"]
        score = grader(action.dict(), ground_truth)
        
        reward = TeenSafetyReward(
            score=score,
            breakdown={"decision_score": score},
            feedback=self._generate_feedback(action, ground_truth, score)
        )
        
        self.episode_reward += score
        done = self.step_count >= self.max_steps or score >= 0.8
        
        observation = TeenSafetyObservation(
            case_id=self.current_scenario["case_id"],
            case_type=self.current_scenario["case_type"],
            content=self.current_scenario["content"],
            user_profile=self.current_scenario["user_profile"],
            platform_context=self.current_scenario["platform_context"],
            previous_actions=[str(action.decision)],
            step_number=self.step_count,
            task_id=self.current_task,
            instructions=self._get_instructions(self.current_task)
        )
        
        return observation, reward, done, {"episode_reward": self.episode_reward}

    def state(self):
        """Return current environment state"""
        return self.state_manager.get_state()

    def _get_instructions(self, task_id: str) -> str:
        instructions = {
            "task1_easy": "Review this content and decide if it is appropriate for a teenage user. Choose from: allow, restrict, block, escalate. Also specify if a warning label should be added.",
            "task2_medium": "Assess if this content poses psychological harm risk to a teenage user. Consider subtle harms like unhealthy body image, dangerous trends, or manipulative content.",
            "task3_hard": "Analyze the behavioral signals and determine if this user has misrepresented their age. You do not have direct proof — use patterns to make your decision."
        }
        return instructions[task_id]

    def _generate_feedback(self, action, ground_truth, score) -> str:
        if score >= 0.8:
            return "Excellent decision. Well reasoned and appropriate action taken."
        elif score >= 0.5:
            return f"Partially correct. Correct decision would be: {ground_truth['correct_decision']}"
        else:
            return f"Incorrect. This content required: {ground_truth['correct_decision']}. Reason: {ground_truth['explanation']}"
```

#### Vibe Coder Prompt for Phase 4:
```
Build env/environment.py with a TeenSafetyEnvironment class that extends BaseEnvironment 
from openenv-core.

It must implement exactly these methods:
1. reset(task_id: str = "task1_easy") -> TeenSafetyObservation
   - Resets episode state
   - Picks a random scenario from the correct task's scenario list
   - Returns initial TeenSafetyObservation

2. step(action: TeenSafetyAction) -> tuple[TeenSafetyObservation, TeenSafetyReward, bool, dict]
   - Processes the action using the correct task's grader
   - Returns (observation, reward, done, info)
   - done=True if step_count >= 5 OR score >= 0.8

3. state() -> dict
   - Returns current state as dict

Also build env/state_manager.py with StateManager class that stores and returns current state.
Build env/reward.py with RewardCalculator class.

Import and use models from env/models.py.
Import graders and scenarios from tasks/task1_easy.py, task2_medium.py, task3_hard.py.
```

---

## MEMBER 2 — RIYANSHI VERMA
### Phases 5, 6, 7, 8

---

### PHASE 5 — Task 3 (Hard) + Grader
**Owner:** Riyanshi
**Timeline:** Day 3 (4-5 hours)
**Goal:** Build the hardest and most impressive task

#### What to Build:
- 6+ synthetic scenarios for Task 3
- Grader that rewards evidence-based reasoning
- Must genuinely challenge frontier models

#### Vibe Coder Prompt for Phase 5:
```
In tasks/task3_hard.py create TASK3_SCENARIOS with 6 scenarios where an agent 
must detect AGE MISREPRESENTATION purely from behavioral signals.

Each scenario: a user has declared they are 18+ but behavioral patterns suggest 
they are actually a minor (under 18). Agent has NO direct age proof.

Scenarios must vary in difficulty:
- 2 scenarios: strong behavioral signals (school schedule, teen slang, teen content)
- 2 scenarios: medium signals (some teen indicators, some adult indicators mixed)  
- 2 scenarios: subtle signals (only 2-3 weak behavioral hints)

Each scenario dict needs:
- case_id: "T3_001" through "T3_006"
- case_type: "age_verification"
- content: dict with account_info (declared_age 18-25, account_created date, bio)
- behavioral_signals: dict with posting_times(list), content_interests(list), 
  language_patterns(list), group_memberships(list), location_tags(list),
  reported_by_peers(int), requested_feature(str)
- user_profile: dict
- platform_context
- ground_truth: dict with correct_decision, key_signals(list of strings that 
  are important evidence), explanation, max_expected_confidence(float 0.5-0.75)

Write grade_task3(action, ground_truth) -> float:
- 0.4 for correct decision (request_verification or restrict)
- 0.2 if action mentions requesting verification
- up to 0.3 based on how many key_signals agent cited in their reason 
  (0.1 per signal mentioned, max 3)
- 0.1 if confidence <= ground_truth["max_expected_confidence"]
- Cap at 1.0

This task should be hard — a random agent should score 0.1-0.3 on average.
```

---

### PHASE 6 — Baseline Inference Script
**Owner:** Riyanshi
**Timeline:** Day 4 (4-5 hours)
**Goal:** Build the inference.py that judges will run

#### CRITICAL RULES:
- File MUST be named exactly `inference.py`
- MUST be in root directory of project
- MUST use OpenAI client format
- MUST read credentials from environment variables
- MUST produce reproducible scores on all 3 tasks
- MUST complete in under 20 minutes

#### Code to Write — `inference.py`:
```python
"""
Teen Safety Compliance Environment — Baseline Inference Script
Team MindMesH | Scaler OpenEnv Hackathon 2026

USAGE:
    Set environment variables:
        API_BASE_URL=https://api.groq.com/openai/v1
        MODEL_NAME=llama-3.3-70b-versatile
        OPENAI_API_KEY=your_api_key
    
    Run:
        python inference.py
"""

import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Read credentials from environment variables — REQUIRED by hackathon
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "llama-3.3-70b-versatile")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Initialize OpenAI client — REQUIRED by hackathon (OpenAI client format)
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=API_BASE_URL
)

# Set seed for reproducibility
random.seed(42)

from env.environment import TeenSafetyEnvironment

SYSTEM_PROMPT = """You are a Teen Safety Compliance Agent for a social media platform.
Your job is to review content and make safety decisions to protect teenage users.

You must respond with a JSON object in this exact format:
{
    "decision": "allow" | "restrict" | "block" | "escalate" | "request_verification",
    "confidence": 0.0 to 1.0,
    "reason": "Your detailed reasoning here",
    "additional_action": "add_warning_label" | "notify_parent" | "age_gate" | null
}

Be thorough in your reasoning. Consider:
- Is this content appropriate for users under 18?
- What are the potential harms?
- What is the most proportionate response?
"""

def get_agent_action(observation: dict) -> dict:
    """Get action from LLM agent"""
    user_message = f"""
Case ID: {observation['case_id']}
Task: {observation['task_id']}
Instructions: {observation['instructions']}

Content to Review:
{json.dumps(observation['content'], indent=2)}

User Profile:
{json.dumps(observation['user_profile'], indent=2)}

Platform: {observation['platform_context']}

Previous Actions: {observation['previous_actions']}

What is your compliance decision?
"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,  # Low temperature for reproducibility
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content
        
        # Parse JSON response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # Fallback action
            return {
                "decision": "escalate",
                "confidence": 0.5,
                "reason": "Unable to parse response, defaulting to escalation",
                "additional_action": None
            }
    except Exception as e:
        print(f"API Error: {e}")
        return {
            "decision": "escalate",
            "confidence": 0.5,
            "reason": f"API error: {str(e)}",
            "additional_action": None
        }

def run_task(env: TeenSafetyEnvironment, task_id: str, num_episodes: int = 3) -> float:
    """Run agent on a task and return average score"""
    total_score = 0.0
    
    print(f"\n{'='*50}")
    print(f"Running Task: {task_id}")
    print(f"{'='*50}")
    
    for episode in range(num_episodes):
        print(f"\nEpisode {episode + 1}/{num_episodes}")
        observation = env.reset(task_id=task_id)
        obs_dict = observation.dict()
        episode_score = 0.0
        done = False
        step = 0
        
        while not done and step < 5:
            action_dict = get_agent_action(obs_dict)
            print(f"  Step {step+1}: Decision={action_dict.get('decision')}, "
                  f"Confidence={action_dict.get('confidence', 0):.2f}")
            
            from env.models import TeenSafetyAction
            try:
                action = TeenSafetyAction(**action_dict)
            except Exception:
                action = TeenSafetyAction(
                    decision="escalate",
                    confidence=0.5,
                    reason="Invalid action format",
                    additional_action=None
                )
            
            observation, reward, done, info = env.step(action)
            obs_dict = observation.dict()
            episode_score = reward.score
            print(f"  Reward: {reward.score:.2f} | Feedback: {reward.feedback[:60]}...")
            step += 1
        
        total_score += episode_score
        print(f"  Episode Score: {episode_score:.2f}")
    
    avg_score = total_score / num_episodes
    print(f"\nAverage Score for {task_id}: {avg_score:.2f}")
    return avg_score

def main():
    print("Teen Safety Compliance Environment — Baseline Inference")
    print("Team MindMesH | Scaler OpenEnv Hackathon 2026")
    print(f"Model: {MODEL_NAME}")
    print(f"API Base: {API_BASE_URL}")
    
    env = TeenSafetyEnvironment()
    results = {}
    
    # Run all 3 tasks
    results["task1_easy"] = run_task(env, "task1_easy", num_episodes=3)
    results["task2_medium"] = run_task(env, "task2_medium", num_episodes=3)
    results["task3_hard"] = run_task(env, "task3_hard", num_episodes=3)
    
    # Print final results
    print(f"\n{'='*50}")
    print("BASELINE RESULTS")
    print(f"{'='*50}")
    for task_id, score in results.items():
        print(f"{task_id}: {score:.4f}")
    
    overall = sum(results.values()) / len(results)
    print(f"\nOverall Average Score: {overall:.4f}")
    
    # Save results for reproducibility
    with open("baseline_results.json", "w") as f:
        json.dump({
            "model": MODEL_NAME,
            "api_base": API_BASE_URL,
            "results": results,
            "overall": overall
        }, f, indent=2)
    
    print("\nResults saved to baseline_results.json")
    return results

if __name__ == "__main__":
    main()
```

#### Vibe Coder Prompt for Phase 6:
```
Build inference.py in the root directory of the project.

STRICT REQUIREMENTS:
- File must be named exactly "inference.py" 
- Must use OpenAI Python client (from openai import OpenAI)
- Must read these env vars: API_BASE_URL, MODEL_NAME, OPENAI_API_KEY
- Must run all 3 tasks: task1_easy, task2_medium, task3_hard
- Must run 3 episodes per task (9 total)
- Must complete in under 20 minutes total
- Must save results to baseline_results.json
- Must be deterministic (use random.seed(42))

The script should:
1. Initialize OpenAI client with API_BASE_URL and OPENAI_API_KEY
2. Create TeenSafetyEnvironment instance
3. For each task run 3 episodes
4. In each episode: call reset(), get LLM action, call step(), record reward
5. Print scores and save to JSON

LLM prompt must ask agent to respond in JSON format with: 
decision, confidence, reason, additional_action

Handle API errors gracefully with fallback action (escalate, 0.5 confidence).
```

---

### PHASE 7 — FastAPI Server + Dockerfile
**Owner:** Riyanshi
**Timeline:** Day 5 (4 hours)
**Goal:** Containerize and make environment serveable

#### Code to Write — `server/app.py`:
```python
from fastapi import FastAPI
from env.environment import TeenSafetyEnvironment
from env.models import TeenSafetyAction

app = FastAPI(
    title="Teen Safety Compliance Environment",
    description="OpenEnv environment for teen safety compliance on social media",
    version="1.0.0"
)

env = TeenSafetyEnvironment()

@app.get("/")
def root():
    return {"name": "teen-safety-compliance-env", "status": "running", "version": "1.0.0"}

@app.post("/reset")
def reset(task_id: str = "task1_easy"):
    observation = env.reset(task_id=task_id)
    return observation.dict()

@app.post("/step")
def step(action: TeenSafetyAction):
    observation, reward, done, info = env.step(action)
    return {
        "observation": observation.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()

@app.get("/health")
def health():
    return {"status": "healthy"}
```

#### Code to Write — `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
```

#### Vibe Coder Prompt for Phase 7:
```
Build server/app.py as a FastAPI application that serves the TeenSafetyEnvironment.

It needs these exact endpoints:
GET  /          → returns {name, status, version}
POST /reset     → accepts task_id query param, calls env.reset(), returns observation dict
POST /step      → accepts TeenSafetyAction body, calls env.step(), returns {observation, reward, done, info}
GET  /state     → calls env.state(), returns current state
GET  /health    → returns {"status": "healthy"}

Then build Dockerfile:
- Base image: python:3.11-slim
- Working dir: /app
- Install requirements.txt
- Copy all files
- Expose port 7860 (required for HuggingFace Spaces)
- CMD: uvicorn server.app:app --host 0.0.0.0 --port 7860

Also create .env.example with:
API_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
OPENAI_API_KEY=your_key_here
HF_TOKEN=your_hf_token_here
```

---

### PHASE 8 — README + HuggingFace Deployment + Final Testing
**Owner:** Riyanshi
**Timeline:** Day 6-7 (4-5 hours)
**Goal:** Deploy and submit

#### README.md Must Include (Hackathon Requirement):
```markdown
# Teen Safety Compliance Environment

## Description & Motivation
## Action Space
## Observation Space  
## Tasks (with expected difficulty)
## Setup & Installation
## Usage Instructions
## Baseline Scores
## Environment Variables
```

#### Deployment Steps:
```bash
# 1. Login to HuggingFace
huggingface-cli login

# 2. Create new Space on huggingface.co
# Go to huggingface.co → New Space → Docker → name: teen-safety-compliance-env

# 3. Push to HuggingFace
git init
git add .
git commit -m "Initial commit"
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/teen-safety-compliance-env
git push origin main

# 4. Validate
openenv validate

# 5. Test deployment
curl https://YOUR_USERNAME-teen-safety-compliance-env.hf.space/health
curl -X POST https://YOUR_USERNAME-teen-safety-compliance-env.hf.space/reset
```

#### Vibe Coder Prompt for Phase 8:
```
Write a comprehensive README.md for the teen-safety-compliance-env OpenEnv project.

Must include these sections:
1. Project Title & One-line description
2. Motivation (why teen safety on social media matters — mention Meta, legal context)
3. Environment Description (what the agent does)
4. Observation Space (list all fields with types and descriptions)
5. Action Space (list all fields with types and valid values)
6. Tasks:
   - Task 1: Obvious Content Restriction (Easy) — description + expected score range
   - Task 2: Subtle Harm Assessment (Medium) — description + expected score range  
   - Task 3: Age Misrepresentation Detection (Hard) — description + expected score range
7. Reward Function (explain partial credit system)
8. Setup Instructions (pip install, env vars)
9. Running Locally (uv run server or uvicorn command)
10. Running Inference (python inference.py)
11. Docker Instructions (docker build + docker run)
12. Baseline Scores table (fill after running inference.py)
13. Environment Variables table

Make it professional and detailed. Judges will read this.
```

---

## 10. SUBMISSION CHECKLIST

### Pre-Submission (Must All Pass or DISQUALIFIED)

| Check | How to Verify | Status |
|-------|--------------|--------|
| HF Space deploys | `curl YOUR_HF_URL/health` returns 200 | ⬜ |
| `reset()` works | `curl -X POST YOUR_HF_URL/reset` returns observation | ⬜ |
| `step()` works | POST to `/step` with action returns reward | ⬜ |
| `openenv validate` passes | Run `openenv validate` locally | ⬜ |
| Docker builds | `docker build -t teen-safety .` succeeds | ⬜ |
| Docker runs | `docker run -p 7860:7860 teen-safety` works | ⬜ |
| inference.py runs | `python inference.py` completes without error | ⬜ |
| inference.py < 20 min | Time the run | ⬜ |
| 3+ tasks with graders | task1, task2, task3 all work | ⬜ |
| Scores in 0.0-1.0 range | Check grader outputs | ⬜ |
| Scores are NOT all same | Run multiple times, check variance | ⬜ |
| README complete | All required sections present | ⬜ |
| inference.py in root | Check file location | ⬜ |
| openenv.yaml exists | Check file exists | ⬜ |

### Submission Steps
1. Push final code to GitHub
2. Deploy to HuggingFace Spaces
3. Copy HF Space URL
4. Go to hackathon platform
5. Paste URL and submit before **8 April 11:59 PM IST**

---

## 11. VIBE CODER TIPS

### How to Use This PRD With Your Vibe Coder

1. **Give context first** — paste the "Project Overview" section to your vibe coder
2. **One phase at a time** — don't dump everything at once
3. **Use the exact prompts** from each phase — they are written to be vibe coder friendly
4. **Always test after each phase** before moving to next
5. **When stuck** — paste the error + relevant code section here for debugging help

### Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `openenv validate` fails | Check openenv.yaml format matches spec exactly |
| Docker build fails | Check all imports in requirements.txt |
| HF Space not responding | Check port is 7860 in Dockerfile |
| inference.py timeout | Reduce num_episodes from 3 to 2 |
| Pydantic validation error | Check model field types match exactly |
| API key error | Check .env file has correct variable names |

---

## 12. IMPORTANT LINKS

| Resource | URL |
|----------|-----|
| OpenEnv Docs | https://openenv.dev |
| HuggingFace Spaces | https://huggingface.co/spaces |
| Groq Free API | https://groq.com |
| Hackathon Support | help_openenvhackathon@scaler.com |
| Discord | Join via dashboard |
| Submit | Platform submission page |

---

*PRD prepared by Claude for Team MindMesH — Scaler OpenEnv Hackathon 2026*
*Good luck Ashish & Riyanshi! 🚀*
