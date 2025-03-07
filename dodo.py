import glob

python_files = glob.glob("src/*.py") + glob.glob("tests/*.py") + glob.glob("*.py")
markdown_files = glob.glob("*.md")


def task_isort():
    """Run isort on all Python files."""
    return {
        "actions": ["isort --profile black " + " ".join(python_files)],
        "file_dep": python_files,
        "verbosity": 2,
    }


def task_black():
    """Run black on all Python files."""
    return {
        "actions": ["black " + " ".join(python_files)],
        "file_dep": python_files,
        "verbosity": 2,
    }


def task_mdformat():
    """Run mdformat on all Markdown files."""
    return {
        "actions": ["mdformat --wrap 80 " + " ".join(markdown_files)],
        "file_dep": markdown_files,
        "verbosity": 2,
    }


def task_pylint():
    """Run pylint on all Python files."""
    return {
        "actions": ["pylint -E " + " ".join(python_files)],
        "file_dep": python_files,
        "verbosity": 2,
    }
