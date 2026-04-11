def grade(output, info=None):
    """
    Grades based on whether the agent chose 'dispatch'
    """
    if not output:
        return 0.0

    output = str(output).lower()

    if "dispatch" in output:
        return 1.0

    return 0.0
