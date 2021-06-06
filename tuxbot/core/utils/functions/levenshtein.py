from Levenshtein import ratio


def levenshtein(test, strings, weight=0.7) -> dict:
    hits = {}

    for string in strings:
        if (hit := ratio(string, test)) >= weight:
            hits[string] = hit

    return hits
