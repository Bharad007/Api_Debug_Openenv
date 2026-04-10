---
title: API Debug OpenEnv
emoji: 🧪
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---


# API Debug OpenEnv

API Debug OpenEnv is an OpenEnv-compatible environment that simulates common real-world API integration failures and evaluates how an agent fixes them through discrete debugging actions.

The environment is deterministic, lightweight, and fully machine-evaluable.

---

## What This Environment Does

Each task represents a broken API interaction.  
An agent must take the **correct debugging action** to resolve the failure.

The environment exposes a standard OpenEnv loop:
- `reset(task_id)`
- `step(action)`
- `state()`

All interactions return HTTP 200.  
Failures are represented **in the environment state**, not as HTTP errors.

---

## Implemented Tasks

| Task ID | Failure Scenario | Correct Action |
|-------|------------------|----------------|
| `easy_auth` | Missing authorization header | `add_auth_header` |
| `medium_rate_limit` | API rate limit exceeded | `retry` |
| `hard_schema` | API schema / version mismatch | `change_api_version` |

Each task terminates immediately upon success.

---

## Reward and Scoring

- Correct action → positive reward  
- Incorrect action → zero reward  
- Episodes end on success  

For evaluation:
- Each task produces a **normalized score strictly in (0, 1)**
- Scores are deterministic and reproducible
- A simple baseline agent achieves near-optimal scores

---

## HTTP API (FastAPI)

### Reset
```http
POST /reset?task_id=easy_auth
```

### Step
```json
{
  "action": "add_auth_header"
}
```

### State
```http
GET /state
```

---

## Inference and Evaluation

A deterministic baseline agent is provided in `inference.py`.

The inference script:
- Uses injected environment variables (`API_BASE_URL`, `API_KEY`)
- Makes at least one LLM call via the provided proxy
- Executes each task once
- Emits **structured stdout logs** in the required format:

```
[START] task=<task> env=<benchmark> model=<model>
[STEP]  step=<n> action=<action> reward=<r> done=<true|false> error=<null|msg>
[END]   success=<true|false> steps=<n> score=<s> rewards=<r1,r2,...>
```

No additional output is printed to stdout.

---

## Repository Structure

```
api_debug_openenv/
├── api_debug_openenv/
│   ├── environment.py   # Core OpenEnv logic
│   ├── tasks.py         # Task definitions
│   ├── rewards.py       # Reward computation
│   ├── models.py        # Typed actions and observations
│   └── server/
│       └── app.py       # FastAPI server
│
├── server/app.py        # Root entrypoint (validator requirement)
├── inference.py         # Baseline agent + evaluation
├── openenv.yaml         # Task metadata
├── pyproject.toml       # Packaging and entrypoints
├── uv.lock
└── Dockerfile
```

---

## OpenEnv Compliance

- Implements `reset`, `step`, and `state`
- Robust to out-of-order calls (e.g. `step` before `reset`)
- Deterministic rewards and transitions
- Machine-parseable inference output
- Compatible with OpenEnv validators and Hugging Face Spaces

---

## How to Run Locally

Run the baseline inference:

```bash
python inference.py
```

Run the server locally:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

---

## Why This Environment Is Useful

- Models real debugging behavior instead of synthetic puzzles  
- Easy to extend with additional API failure modes  
- Suitable for agent benchmarking and teaching  
- Clean separation of environment logic, rewards, and interface  

---

## Possible Extensions

- Multi-step debugging chains  
- Partial rewards for intermediate fixes  
- Stateful rate-limit windows  
- Noisy or ambiguous failure signals  

---

## Author

Subrahmanya  
Meta PyTorch Hackathon × Scaler School of Technology
