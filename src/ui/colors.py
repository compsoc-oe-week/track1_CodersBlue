# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

def green(text):
    """Returns green text for success messages."""
    return f"{GREEN}{text}{ENDC}"

def yellow(text):
    """Returns yellow text for warnings."""
    return f"{YELLOW}{text}{ENDC}"

def red(text):
    """Returns red text for dangerous operations."""
    return f"{RED}{text}{ENDC}"

def bold(text):
    """Returns bold text for commands."""
    return f"{BOLD}{text}{ENDC}"