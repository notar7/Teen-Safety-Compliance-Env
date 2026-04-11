---
title: Teen Safety Compliance Env
emoji: 🛡️
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

<!-- Hugging Face Spaces metadata above is required for Space configuration. -->

<!-- markdownlint-disable-next-line MD025 -->

## Teen Safety Compliance Environment

OpenEnv-compliant reinforcement learning environment for teen-safety moderation decisions on social platforms.

Built for Scaler OpenEnv Hackathon 2026 by Team MindMesH.

## Creators

- Ashish Ransing (Lead) — GitHub: [@notar7](https://github.com/notar7)
- Riyanshi Verma — GitHub: [@Codigoaprendiza02](https://github.com/Codigoaprendiza02)

---

## What this environment is

This environment simulates a production-style teen safety compliance pipeline where an agent must decide whether to allow, restrict, block, escalate, or request age verification for risky content and account behaviors.

It is designed to evaluate:

- obvious policy violations,
- subtle psychological harm,
- age fraud and misrepresentation,
- adversarial/obfuscated harmful intent,
- recommendation-surface safety and privacy risk.

The environment is deterministic and benchmark-friendly: same inputs produce same grades.

---

## OpenEnv interaction model

The agent uses the standard loop:

- `reset(task_id)` → initial observation
- `step(action)` → observation, reward, done, info
- `state()` → current episode state

Core objects:

- `TeenSafetyObservation`
- `TeenSafetyAction`
- `TeenSafetyReward`

Reward scores are strictly clamped to the open interval `(0, 1)` for validator compatibility.

---

## Round 2 implemented improvements

All major engineering improvements from the internal plan are implemented:

1. Expanded benchmark from 3 tasks to 10 tasks.
2. Dynamic task registry and API task catalog (no hardcoded 3-task paths).
3. Risk-tiered decision logic in inference calibration.
4. Uncertainty-aware handling for ambiguous/conflicting cases.
5. Recommendation gating behavior integrated in policy logic.
6. Adversarial/coded-harm cue handling (e.g., obfuscated terms).
7. Counterfactual note support in decision reasoning.
8. Internal policy trace (`signals -> rule -> action`) in step info/state.
9. Strict validator-safe stdout format retained (`[START]`, `[STEP]`, `[END]`).
10. Optional summary line retained but sanitized to print only `overall_avg`.

---

## Task matrix (10 tasks)

### Easy

- `task1_easy`: obvious content restriction for minors
- `task4_easy`: self-harm/violent challenge suppression
- `task5_easy`: grooming/exploitation/adult solicitation blocking

### Medium

- `task2_medium`: subtle psychological harm assessment
- `task6_medium`: recommendation risk gating
- `task7_medium`: conflicting metadata resolution
- `task8_medium`: teen privacy/location exposure control

### Hard

- `task3_hard`: age misrepresentation detection from behavior
- `task9_hard`: adversarial mixed-signal moderation
- `task10_hard`: obfuscated harmful intent detection

---

## Evaluation summary (integrated evaluation packet)

### Current benchmark snapshot

Latest local deterministic run (`baseline_results.json`) shows:

| Scope | ID / Group | Avg Score |
| --- | --- | ---: |
| Overall | all tasks | `0.98` |
| Difficulty average | easy | `0.99` |
| Difficulty average | medium | `0.99` |
| Difficulty average | hard | `0.97` |
| Task | `task1_easy` | `0.99` |
| Task | `task2_medium` | `0.99` |
| Task | `task3_hard` | `0.93` |
| Task | `task4_easy` | `0.99` |
| Task | `task5_easy` | `0.99` |
| Task | `task6_medium` | `0.99` |
| Task | `task7_medium` | `0.99` |
| Task | `task8_medium` | `0.99` |
| Task | `task9_hard` | `0.99` |
| Task | `task10_hard` | `0.99` |

### Failure modes addressed

- Obfuscated harmful terms bypassing simple keyword filters.
- “Educational” framing with hidden risky promotion signals.
- Teen privacy/location data extraction patterns.
- Mixed-signal content that requires calibrated escalation vs restriction.
- Age-fraud patterns without direct identity proof.

---

## Fairness and bias guardrails (integrated fairness audit)

The decision logic is designed to use policy-relevant risk signals only.

### Signals used

- content risk cues (harmful themes, metadata contradictions, obfuscation),
- teen-safety context (age-related safety constraints),
- behavior patterns directly tied to policy objectives.

### Signals not used for punitive decisions

- irrelevant personal traits not tied to safety policy,
- demographic attributes as standalone risk predictors.

### Guardrails in practice

- deterministic grading and transparent rule criteria,
- internal policy trace for auditability,
- cross-step consistency controls to reduce contradictory actions,
- explicit escalation pathways for uncertainty.

---

## Technical stack

- Python 3.11
- openenv-core
- FastAPI + Uvicorn
- Pydantic v2
- OpenAI Python client (OpenAI-compatible endpoints)
- pytest
- Docker

---

## Environment structure

- `env/` — environment core, models, reward, state manager
- `tasks/` — all scenario sets + deterministic graders
- `server/` — FastAPI API service
- `inference.py` — benchmark inference runner and policy calibration
- `openenv.yaml` — OpenEnv metadata
- `Dockerfile` — container runtime
- `tests/` — regression and contract tests

---

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.

```bash
pip install -r requirements.txt
```

1. Configure environment variables.

```env
API_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
OPENAI_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
```

Environment variable reference:

| Variable | Required | Used in | Example | Purpose |
| --- | --- | --- | --- | --- |
| `API_BASE_URL` | Yes | `inference.py` | `https://api.groq.com/openai/v1` | OpenAI-compatible endpoint base URL |
| `MODEL_NAME` | Yes | `inference.py` | `llama-3.3-70b-versatile` | Model ID for decision calls |
| `OPENAI_API_KEY` | Yes | `inference.py` | `gsk_xxx` or `sk-xxx` | API authentication |
| `HF_TOKEN` | Optional (deploy) | HF workflow | `hf_xxx` | Hugging Face auth |
| `PRINT_OVERALL_SUMMARY` | Optional | `inference.py` | `1` | Print `[SUMMARY] overall_avg=...` line |

Security notes:

- Keep secrets in local `.env` or Hugging Face Space secrets.
- Never commit live API keys.
- Rotate keys immediately if exposed.

---

## Run locally

Start API server:

```bash
python -m server.app
```

Server: `http://0.0.0.0:7860`

API endpoints:

- `GET /` — metadata
- `GET /health` — health status
- `GET /tasks` — dynamic task catalog
- `POST /reset?task_id=...` — reset episode
- `POST /step` — submit action
- `GET /state` — current state snapshot

---

## Run benchmark inference

```bash
python inference.py
```

This runs all registered tasks (currently 10), prints validator-safe progress logs, and writes `baseline_results.json`.

---

## Test status

Run tests:

```bash
pytest -q
```

Current status: `106 passed`.

---

## Docker

Build:

```bash
docker build -t teen-safety-compliance-env .
```

Run:

```bash
docker run --rm -p 7860:7860 --env-file .env teen-safety-compliance-env
```

---

## Hugging Face Spaces deployment notes

- Use Docker Space.
- Expose port `7860`.
- Configure required secrets/env vars in Space settings.
- Smoke test: `/health`, `/reset`, `/step`, `/state`.

---

## Roadmap (next iterations)

- Add multilingual scenarios and region-specific safety patterns.
- Add richer long-horizon reward shaping for repeat-offense behavior.
- Add policy-version benchmarking and drift analysis dashboard.
- Add multi-agent audit workflows for governance evaluation.

---
