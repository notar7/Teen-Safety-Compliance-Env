---
title: Teen Safety Compliance Env
emoji: 🛡️
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

<!-- Hugging Face Spaces metadata above is required for Space configuration. -->

# Teen Safety Compliance Environment

OpenEnv-compliant reinforcement learning environment that simulates teen safety compliance decisions for social media platforms.

Built for Scaler OpenEnv Hackathon 2026 by Team MindMesH.

## Creators

- Ashish Ransing (Lead) — GitHub: [@notar7](https://github.com/notar7)
- Riyanshi Verma — GitHub: [@Codigoaprendiza02](https://github.com/Codigoaprendiza02)

---

## 🚀 Project Overview

This environment evaluates an agent’s ability to:
- Restrict clearly unsafe content for minors
- Detect subtle psychological harm patterns
- Identify age misrepresentation from behavioral signals

The agent interacts with a standard OpenEnv loop:
- `reset(task_id)` → initial observation
- `step(action)` → observation, reward, done, info
- `state()` → current episode state

---

## 🌍 Why this project matters

Teen online safety is a high-impact, real-world compliance domain. This environment models policy-style moderation tradeoffs with deterministic grading and reproducible evaluation runs.

---

## 🧩 Tasks and difficulty

### Task 1: `task1_easy` (Easy)
Obvious policy violations for under-18 users.
Examples: alcohol ads, gambling promos, firearms sales, adult content promotions.

Expected good-agent range: `0.70 – 1.00`.

### Task 2: `task2_medium` (Medium)
Subtle harm assessment for teens.
Examples: dangerous dieting, predatory parasocial content, scam patterns, cyberbullying-adjacent posts.

Expected good-agent range: `0.40 – 0.80`.

### Task 3: `task3_hard` (Hard)
Age-misrepresentation detection using behavioral evidence only.
Examples: school-timing activity patterns, teen-interest clusters, suspicious group memberships.

Expected good-agent range: `0.20 – 0.60`.

---

## 🧠 Observation, action, reward

### Observation (`TeenSafetyObservation`)
- `case_id`: unique case id
- `case_type`: `content_review` | `harm_assessment` | `age_verification`
- `content`: case payload
- `user_profile`: user metadata
- `platform_context`: platform context
- `previous_actions`: action history in episode
- `step_number`: current step
- `task_id`: active task
- `instructions`: task-specific instruction text

### Action (`TeenSafetyAction`)
- `decision`: `allow` | `restrict` | `block` | `escalate` | `request_verification`
- `confidence`: float in `[0.0, 1.0]`
- `reason`: natural language rationale
- `additional_action`: optional action (`add_warning_label` | `notify_parent` | `age_gate`)

### Reward (`TeenSafetyReward`)
- `score`: float in `[0.0, 1.0]`
- `breakdown`: structured details
- `feedback`: grader feedback text

---

## 🛠️ Tech stack

- Python 3.11
- openenv-core
- FastAPI + Uvicorn
- Pydantic v2
- OpenAI Python client (used with OpenAI-compatible endpoints, e.g., Groq)
- pytest
- Docker

---

## 🗂️ Project structure

- `env/` — environment core, models, reward, state manager
- `tasks/` — scenario sets + deterministic graders
- `server/` — FastAPI API server
- `inference.py` — baseline inference/evaluation script
- `openenv.yaml` — OpenEnv metadata
- `Dockerfile` — containerization
- `tests/` — test suite

---

## ⚙️ Setup

1. Create/activate virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables (example):

```env
API_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
OPENAI_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
```

### Environment variables details

| Variable | Required | Used in | Example | Purpose |
| --- | --- | --- | --- | --- |
| `API_BASE_URL` | Yes | `inference.py` | `https://api.groq.com/openai/v1` | OpenAI-compatible endpoint base URL |
| `MODEL_NAME` | Yes | `inference.py` | `llama-3.3-70b-versatile` | Model ID used for agent decisions |
| `OPENAI_API_KEY` | Yes | `inference.py` | `gsk_xxx` or `sk-xxx` | Auth token for model API access |
| `HF_TOKEN` | Recommended for deploy | HF deployment workflow | `hf_xxx` | Hugging Face authentication for pushing/deploying Space |

Notes:

- Keep secrets only in local `.env` or HF Space Secrets.
- Never commit real API keys to Git.
- If a key is exposed, rotate it immediately and replace it everywhere.

---

## 💻 Run locally

### Start server

```bash
python -m server.app
```

Server runs at `http://0.0.0.0:7860`.

### API endpoints
- `GET /` — metadata
- `GET /health` — health status
- `GET /tasks` — task metadata
- `POST /reset?task_id=...` — reset episode
- `POST /step` — submit action
- `GET /state` — current state snapshot

---

## 📈 Run baseline inference

```bash
python inference.py
```

This runs all 3 tasks (3 episodes each), prints scores, and writes `baseline_results.json`.

---

## 🏁 Baseline results (latest run)

Latest baseline run produced:

| Task | Avg Score |
|---|---:|
| `task1_easy` | `1.0000` |
| `task2_medium` | `1.0000` |
| `task3_hard` | `0.8667` |
| **Overall** | **`0.9556`** |

Runtime: ~`11.1s`.

---

## ✅ Tests

Run full test suite:

```bash
pytest -q
```

Current status: `100 passed`.

---

## 🔍 OpenEnv validation

Validate project readiness:

```bash
openenv validate
```

Current status: passes (`Ready for multi-mode deployment`).

---

## 🐳 Docker

Build image:

```bash
docker build -t teen-safety-compliance-env .
```

Run container:

```bash
docker run --rm -p 7860:7860 --env-file .env teen-safety-compliance-env
```

> `.dockerignore` excludes local artifacts, tests, and secret files from build context.

---

## ☁️ Deployment notes (Hugging Face Spaces)

- Use Docker Space
- Expose port `7860`
- Ensure env vars are configured in Space secrets
- Verify `/health`, `/reset`, `/step` after deploy

---

## 🔮 Future scope

- Add multilingual safety scenarios (Hindi, Hinglish, and regional languages) for broader moderation coverage.
- Introduce adversarial prompt/content variants to stress-test policy robustness.
- Expand task coverage with cross-platform escalation workflows and appeal-handling loops.
- Add richer reward shaping using long-term safety outcomes (repeat-offense penalties, recovery signals).
- Support multi-agent evaluation (moderation agent + auditor agent) for governance-style benchmarks.
- Build a lightweight dashboard for per-task drift tracking, score trends, and failure analysis.
- Add a policy-versioning layer so agents can be tested against evolving safety rules over time.

---
