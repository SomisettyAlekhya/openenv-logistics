def grade(output, info=None):
    """
    Accepts reroute or alternative routing decisions
    """
    if not output:
        return 0

    output = str(output).lower()

    valid_actions = ["reroute", "alternate_route", "redirect"]

    for action in valid_actions:
        if action in output:
            return 1

    return 0
