
def classify_intent(message):
    text = message.lower()

    if any(word in text for word in [
        "phone", "contact", "number", "call"
    ]):
        return "contact"

    if any(word in text for word in [
        "where", "location", "address", "located"
    ]):
        return "location"

    if any(word in text for word in [
        "open", "close", "hours", "timing", "when"
    ]):
        return "operating_hours"

    if any(word in text for word in [
        "membership", "member", "join", "register"
    ]):
        return "membership"

    if any(word in text for word in [
        "service", "services", "provide", "offer"
    ]):
        return "services"

    if any(word in text for word in [
        "admission", "apply", "application", "college"
    ]):
        return "education"

    return "general"
