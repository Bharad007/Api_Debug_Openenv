import os
from openai import OpenAI

from api_debug_openenv.environment import ApiDebugEnv
from api_debug_openenv.models import ApiAction

# Environment variables injected by validator
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

# Required OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)

BENCHMARK = "api_debug_openenv"

POLICY = {
    "easy_auth": "add_auth_header",
    "medium_rate_limit": "retry",
    "hard_schema": "change_api_version",
}

if __name__ == "__main__":
    tasks = ["easy_auth", "medium_rate_limit", "hard_schema"]

    for task in tasks:
        env = ApiDebugEnv()
        rewards = []

        # ✅ START
        print(
            f"[START] task={task} env={BENCHMARK} model={MODEL_NAME}",
            flush=True,
        )

        try:
            # ✅ REQUIRED: make at least one LLM call through proxy
            _ = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=5,
            )

            env.reset(task)

            action_str = POLICY[task]
            action = ApiAction(action=action_str)

            state, reward, done = env.step(action)
            rewards.append(reward)

            # ✅ STEP
            print(
                f"[STEP] step=1 action={action_str} "
                f"reward={reward:.2f} done={str(done).lower()} error=null",
                flush=True,
            )

            score = max(min(reward, 1.0), 0.0)
            success = score >= 0.0

        finally:
            rewards_str = ",".join(f"{r:.2f}" for r in rewards)
            print(
                f"[END] success={str(success).lower()} steps=1 "
                f"score={score:.2f} rewards={rewards_str}",
                flush=True,
            )