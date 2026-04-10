def grade(output, info=None):
    text = str(output).lower()
    if "dispatch" in text or "send vehicle" in text:
        return 1
    return 0
