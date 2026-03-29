def grade_task(success: bool, attempts: int, max_attempts: int):
    """
    Returns a score between 0.0 and 1.0
    """
    if success:
        return 1.0

    if attempts < max_attempts:
        return 0.5

    return 0.0