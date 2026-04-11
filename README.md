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

OpenEnv-Compliant Reinforcement Learning Environment For Teen-Safety Moderation Decisions On Social Platforms.

Built For Scaler OpenEnv Hackathon 2026 By Team MindMesH.

## Creators

- Ashish Ransing (Lead) — GitHub: [@notar7](https://github.com/notar7)
- Riyanshi Verma — GitHub: [@Codigoaprendiza02](https://github.com/Codigoaprendiza02)

---

## What This Environment Is

This Environment Simulates A Production-Style Teen Safety Compliance Pipeline Where An Agent Must Decide Whether To Allow, Restrict, Block, Escalate, Or Request Age Verification For Risky Content And Account Behaviors.

It Is Designed To Evaluate:

- Obvious Policy Violations,
- Subtle Psychological Harm,
- Age Fraud And Misrepresentation,
- Adversarial/Obfuscated Harmful Intent,
- Recommendation-Surface Safety And Privacy Risk.

The Environment Is Deterministic And Benchmark-Friendly: Same Inputs Produce Same Grades.

---

## OpenEnv Interaction Model

The Agent Uses The Standard Loop:

- `reset(task_id)` → initial observation
- `step(action)` → observation, reward, done, info
- `state()` → current episode state

Core Objects:

- `TeenSafetyObservation`
- `TeenSafetyAction`
- `TeenSafetyReward`

Reward Scores Are Strictly Clamped To The Open Interval `(0, 1)` For Validator Compatibility.

---

## Round 2 Implemented Improvements

All Major Engineering Improvements From The Internal Plan Are Implemented:

1. Expanded Benchmark From 3 Tasks To 10 Tasks.
2. Dynamic Task Registry And API Task Catalog (No Hardcoded 3-Task Paths).
3. Risk-Tiered Decision Logic In Inference Calibration.
4. Uncertainty-Aware Handling For Ambiguous/Conflicting Cases.
5. Recommendation Gating Behavior Integrated In Policy Logic.
6. Adversarial/Coded-Harm Cue Handling (E.G., Obfuscated Terms).
7. Counterfactual Note Support In Decision Reasoning.
8. Internal Policy Trace (`Signals -> Rule -> Action`) In Step Info/State.
9. Strict Validator-Safe Stdout Format Retained (`[START]`, `[STEP]`, `[END]`).
10. Optional Summary Line Retained But Sanitized To Print Only `overall_avg`.

---

## Task Matrix (10 Tasks)

### Easy

- `task1_easy`: Obvious Content Restriction For Minors
- `task4_easy`: Self-Harm/Violent Challenge Suppression
- `task5_easy`: Grooming/Exploitation/Adult Solicitation Blocking

### Medium

- `task2_medium`: Subtle Psychological Harm Assessment
- `task6_medium`: Recommendation Risk Gating
- `task7_medium`: Conflicting Metadata Resolution
- `task8_medium`: Teen Privacy/Location Exposure Control

### Hard

- `task3_hard`: Age Misrepresentation Detection From Behavior
- `task9_hard`: Adversarial Mixed-Signal Moderation
- `task10_hard`: Obfuscated Harmful Intent Detection

---

## Evaluation Summary (Integrated Evaluation Packet)

### Current Benchmark Snapshot

Latest Local Deterministic Run (`baseline_results.json`) Shows:

| Scope | ID / Group | Avg Score |
| --- | --- | ---: |
| Overall | All Tasks | `0.98` |
| Difficulty Average | Easy | `0.99` |
| Difficulty Average | Medium | `0.99` |
| Difficulty Average | Hard | `0.97` |
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

### Failure Modes Addressed

- Obfuscated Harmful Terms Bypassing Simple Keyword Filters.
- “Educational” Framing With Hidden Risky Promotion Signals.
- Teen Privacy/Location Data Extraction Patterns.
- Mixed-Signal Content That Requires Calibrated Escalation Vs Restriction.
- Age-Fraud Patterns Without Direct Identity Proof.

---

## Fairness And Bias Guardrails (Integrated Fairness Audit)

The Decision Logic Is Designed To Use Policy-Relevant Risk Signals Only.

### Signals Used

- Content Risk Cues (Harmful Themes, Metadata Contradictions, Obfuscation),
- Teen-Safety Context (Age-Related Safety Constraints),
- Behavior Patterns Directly Tied To Policy Objectives.

### Signals Not Used For Punitive Decisions

- Irrelevant Personal Traits Not Tied To Safety Policy,
- Demographic Attributes As Standalone Risk Predictors.

### Guardrails In Practice

- Deterministic Grading And Transparent Rule Criteria,
- Internal Policy Trace For Auditability,
- Cross-Step Consistency Controls To Reduce Contradictory Actions,
- Explicit Escalation Pathways For Uncertainty.

---

## Technical Stack

- Python 3.11
- OpenEnv-Core
- FastAPI + Uvicorn
- Pydantic v2
- OpenAI Python client (OpenAI-compatible endpoints)
- Pytest
- Docker

---

## Environment Structure

- `env/` — Environment Core, Models, Reward, State Manager
- `tasks/` — All Scenario Sets + Deterministic Graders
- `server/` — FastAPI API Service
- `inference.py` — Benchmark Inference Runner And Policy Calibration
- `openenv.yaml` — OpenEnv Metadata
- `Dockerfile` — Container Runtime
- `tests/` — Regression And Contract Tests

---

## Setup

1. Create And Activate A Virtual Environment.
2. Install Dependencies.

```bash
pip install -r requirements.txt
```

1. Configure Environment Variables.

```env
API_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
OPENAI_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
```

Environment Variable Reference:

| Variable | Required | Used in | Example | Purpose |
| --- | --- | --- | --- | --- |
| `API_BASE_URL` | Yes | `inference.py` | `https://api.groq.com/openai/v1` | OpenAI-compatible endpoint base URL |
| `MODEL_NAME` | Yes | `inference.py` | `llama-3.3-70b-versatile` | Model ID for decision calls |
| `OPENAI_API_KEY` | Yes | `inference.py` | `gsk_xxx` or `sk-xxx` | API authentication |
| `HF_TOKEN` | Optional (deploy) | HF workflow | `hf_xxx` | Hugging Face auth |
| `PRINT_OVERALL_SUMMARY` | Optional | `inference.py` | `1` | Print `[SUMMARY] overall_avg=...` line |

Security Notes:

- Keep Secrets In Local `.env` Or Hugging Face Space Secrets.
- Never Commit Live API Keys.
- Rotate Keys Immediately If Exposed.

---

## Run Locally

Start API Server:

```bash
python -m server.app
```

Server: `http://0.0.0.0:7860`

API Endpoints:

- `GET /` — Metadata
- `GET /health` — Health Status
- `GET /tasks` — Dynamic Task Catalog
- `POST /reset?task_id=...` — Reset Episode
- `POST /step` — Submit Action
- `GET /state` — Current State Snapshot

---

## Run Benchmark Inference

```bash
python inference.py
```

This Runs All Registered Tasks (Currently 10), Prints Validator-Safe Progress Logs, And Writes `baseline_results.json`.

---

## Test Status

Run Tests:

```bash
pytest -q
```

Current Status: `106 Passed`.

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

## Hugging Face Spaces Deployment Notes

- Use Docker Space.
- Expose Port `7860`.
- Configure Required Secrets/Env Vars In Space Settings.
- Smoke Test: `/health`, `/reset`, `/step`, `/state`.

---
