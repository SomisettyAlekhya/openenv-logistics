def grade(output, info=None):
    """
    Grades based on delay decision
    """
    if not output:
        return 0.0

    output = str(output).lower()

    if "delay" in output:
        return 1.0
    elif "wait" in output:
        return 0.5

    return 0.0
