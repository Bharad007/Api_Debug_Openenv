def compute_reward(result, action):
    if result["success"]:
        return 1.0
    
    if result["status_code"] == 401 and action.action == "add_auth_header":
        return 0.4
    
    if result["status_code"] == 429 and action.action == "retry":
        return 0.3
    
    if result["status_code"] == 400 and action.action == "change_api_version":
        return 0.5
    
    return 0.0