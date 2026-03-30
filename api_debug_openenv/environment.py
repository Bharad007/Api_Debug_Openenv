from api_debug_openenv.models import ApiObservation, ApiAction
from api_debug_openenv.tasks import TASKS
from api_debug_openenv.rewards import compute_reward


class ApiDebugEnv:
    def __init__(self):
        self._state = None

    def reset(self, task_id: str):
        self.task_id = task_id
        self.task_fn = TASKS[task_id]

        self._state = ApiObservation(
            task_id=task_id,
            message="environment reset",
            last_action=None,
        )
        return self._state

    def step(self, action: ApiAction):
        # ✅ Defensive: auto-reset if step is called first
        if not hasattr(self, "task_fn") or self._state is None:
            self.reset("easy_auth")

        result = self.task_fn(self._state, action)

        reward = compute_reward(result, action)
        done = result["success"]

        if result["success"]:
            message = "API call successful"
        else:
            message = f"Error: {result['error']}"

        self._state = ApiObservation(
            task_id=self.task_id,
            message=message,
            last_action=action.action,
        )

        return self._state, reward, done

    def state(self):
        return self._state