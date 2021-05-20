from pathlib import Path


def safe_mkdirs(path):
    """Creates a directory for the given path

    Args:
        path (string): directory path
    """
    Path(path).mkdir(parents=True, exist_ok=True)


