def grade(output, info=None):
    text = str(output).lower()
    if "reroute" in text or "alternate route" in text:
        return 1
    return 0
