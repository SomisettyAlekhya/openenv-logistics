def grade(output, info=None):
    text = str(output).lower()
    if "priority" in text or "urgent" in text:
        return 1
    return 0
