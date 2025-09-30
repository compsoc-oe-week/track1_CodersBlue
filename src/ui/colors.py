import colorama

# Define constants for easy use.
# Using colorama makes this cross-platform.
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN
BOLD = colorama.Style.BRIGHT
RESET = colorama.Style.RESET_ALL

# Functions to wrap text in colors
def green(text):
    """Returns green text for success messages."""
    return f"{GREEN}{text}{RESET}"

def yellow(text):
    """Returns yellow text for warnings."""
    return f"{YELLOW}{text}{RESET}"

def red(text):
    """Returns red text for dangerous operations."""
    return f"{RED}{text}{RESET}"

def cyan(text):
    """Returns cyan text for persona highlights."""
    return f"{CYAN}{text}{RESET}"

def bold(text):
    """Returns bold text for commands."""
    return f"{BOLD}{text}{RESET}"