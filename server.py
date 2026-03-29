from fastapi import FastAPI
from environment import ApiDebugEnv
from models import ApiAction

app = FastAPI()
env = ApiDebugEnv()

@app.post("/reset")
def reset(task_id: str):
    return env.reset(task_id)

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