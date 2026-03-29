from fastapi import FastAPI
from environment import ApiDebugEnv
from models import ApiAction
from typing import Optional

app = FastAPI()
env = ApiDebugEnv()

DEFAULT_TASK_ID = "easy_auth"  # Default task if none provided

@app.post("/reset")
def reset(task_id: Optional[str] = None):
    """
    OpenEnv-compatible reset endpoint.
    If task_id is not provided, fall back to default task.
    """
    task = task_id or DEFAULT_TASK_ID
    return env.reset(task)


@app.post("/step")
def step(action: ApiAction):
    state, reward, done = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def state():
    return env.state()