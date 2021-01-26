from collections import Counter


def sort_by(_events: Counter) -> dict[str, dict]:
    majors = [
        "guild",
        "channel",
        "message",
        "invite",
        "integration",
        "presence",
        "voice",
        "other",
    ]
    sorted_events = {m: {} for m in majors}

    for event, count in _events:
        done = False
        for m in majors:
            if event.lower().startswith(m):
                sorted_events[m][event] = count
                done = True
        if not done:
            sorted_events["other"][event] = count

    return sorted_events
