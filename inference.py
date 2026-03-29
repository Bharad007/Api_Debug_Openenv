
import os
from openai import OpenAI

from environment import ApiDebugEnv
from models import ApiAction

# # Required environment variables
# API_BASE_URL = os.environ.get("API_BASE_URL")
# MODEL_NAME = os.environ.get("MODEL_NAME")   
# HF_TOKEN = os.environ.get("HF_TOKEN")

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "dummy_key_for_local_test")

# 🔑 IMPORTANT: bridge HF_TOKEN → OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = HF_TOKEN

# OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_task(task_id: str):

    env = ApiDebugEnv()
    env.reset(task_id)

    # Simple deterministic baseline policy
    policy = {
        "easy_auth": "add_auth_header",
        "medium_rate_limit": "retry",
        "hard_schema": "change_api_version",
    }

    action = ApiAction(action=policy[task_id])
    state, reward, done = env.step(action)

    return reward

if __name__ == "__main__":
    tasks = ["easy_auth", "medium_rate_limit", "hard_schema"]

    print("Running baseline inference:\n")

    for task in tasks:  
        score = run_task(task)
        print(f"{task}: score = {score}")
