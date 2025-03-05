import glob

python_files = glob.glob("*.py")
markdown_files = glob.glob("*.md")


def task_isort():
    """Run isort on all Python files."""
    return {
        "actions": ["isort --profile black ."],
        "file_dep": python_files,
        "verbosity": 2,
    }


def task_black():
    """Run black on all Python files."""
    return {
        "actions": ["black ."],
        "file_dep": python_files,
        "verbosity": 2,
    }


def task_mdformat():
    """Run mdformat on all Markdown files."""
    return {
        "actions": ["mdformat README.md --wrap 120"],
        "file_dep": markdown_files,
        "verbosity": 2,
    }


def task_pylint():
    """Run pylint on all Python files."""
    return {
        "actions": ["pylint -E *.py"],
        "file_dep": python_files,
        "verbosity": 2,
    }
