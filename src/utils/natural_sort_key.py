import re


def natural_sort_key(s):
    """Helper function to perform natural sort order."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", str(s))]
