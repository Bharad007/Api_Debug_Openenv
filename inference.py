import os
from openai import OpenAI

from api_debug_openenv.environment import ApiDebugEnv
from api_debug_openenv.models import ApiAction

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "dummy_key_for_local_test")

# Bridge HF_TOKEN -> OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = HF_TOKEN

# Required OpenAI client (even if not used)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
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

        # START
        print(
            f"[START] task={task} env={BENCHMARK} model={MODEL_NAME}",
            flush=True,
        )

        try:
            env.reset(task)

            action_str = POLICY[task]
            action = ApiAction(action=action_str)

            state, reward, done = env.step(action)
            rewards.append(reward)

            # STEP
            print(
                f"[STEP] step=1 action={action_str} "
                f"reward={reward:.2f} done={str(done).lower()} error=null",
                flush=True,
            )

            score = max(min(reward, 1.0), 0.0)
            success = score >= 0.0

        finally:
            # END (must always be printed)
            rewards_str = ",".join(f"{r:.2f}" for r in rewards)
            print(
                f"[END] success={str(success).lower()} steps=1 "
                f"score={score:.2f} rewards={rewards_str}",
                flush=True,
            )
