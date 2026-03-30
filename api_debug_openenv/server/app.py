from typing import Optional
import uvicorn
from fastapi import FastAPI

from api_debug_openenv.environment import ApiDebugEnv
from api_debug_openenv.models import ApiAction

app = FastAPI()
env = ApiDebugEnv()

DEFAULT_TASK_ID = "easy_auth"


@app.post("/reset")
def reset(task_id: Optional[str] = None):
    task = task_id or DEFAULT_TASK_ID
    return env.reset(task)


@app.post("/step")
def step(action: ApiAction):
    state, reward, done = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
    }


@app.get("/state")
def state():
    return env.state()


def main():
    """
    OpenEnv multi-mode entrypoint.
    Required for openenv validate and CLI execution.
    """
    uvicorn.run(
        "api_debug_openenv.server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=False,
    )


if __name__ == "__main__":
    main()