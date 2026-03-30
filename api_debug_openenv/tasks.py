def easy_auth_task(state, action):
    """
    Simulates an API that requires an Authorization header.
    """

    if action.action == "add_auth_header":
        return {
            "success": True,
            "status_code": 200,
            "error": None
        }
    
    return {
        "success": False,
        "status_code": 401,
        "error": "Unauthorized: Missing Authorization header"
    }

def medium_rate_limit_task(state, action):
    """
    Simulates an API that has a rate limit of 5 requests per minute.
    """

    # This is a placeholder implementation. In a real implementation, you would track the number of requests and the time of the last request.
    if action.action == "retry":
        return {
            "success": True,
            "status_code": 200,
            "error": None
        }
    
    return {
        "success": False,
        "status_code": 429,
        "error": "Too Many Requests: Rate limit exceeded"
    }

def hard_schema_task(state, action):
    """
    Simulates an API that requires a specific JSON schema in the request body.
    """

    if action.action == "change_api_version":
        return {
            "success": True,
            "status_code": 200,
            "error": None
        }
    
    return {
        "success": False,
        "status_code": 400,
        "error": "Bad Request: Invalid JSON schema"
    }

# Task registry for easy lookup
TASKS = {
    "easy_auth": easy_auth_task,
    "medium_rate_limit": medium_rate_limit_task,
    "hard_schema": hard_schema_task
}
# Required for grading
TASK_METADATA = {
    "easy_auth": {"max_attempts": 3},
    "medium_rate_limit": {"max_attempts": 4},
    "hard_schema": {"max_attempts": 5}
}