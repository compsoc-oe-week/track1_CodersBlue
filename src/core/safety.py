import os
import re

DANGEROUS_PATHS = ['/', '/etc', '/boot', '/usr']
DESTRUCTIVE_COMMANDS = ['rm', 'mv', 'chmod', 'chown']

def is_dangerous_path(path):
    """Checks if a path is in the list of dangerous paths."""
    return os.path.abspath(path) in DANGEROUS_PATHS

def resolve_path(path):
    """Resolves symbolic links and returns the absolute path."""
    return os.path.abspath(os.path.realpath(path))

def get_command_paths(command):
    """Extracts all file paths from a command string."""
    # This regex is a simple approach and might not cover all edge cases.
    # It looks for sequences of characters that are likely to be file paths.
    # It avoids matching options (like -r) by not starting with a hyphen.
    path_pattern = re.compile(r'(?:\s|/|^)([a-zA-Z0-9_./-]+)')
    potential_paths = path_pattern.findall(command)

    # Filter out things that are probably not paths
    paths = []
    for p in potential_paths:
        # A very basic filter: if it contains a slash or a dot, it's probably a path.
        # This is to avoid matching simple arguments or parts of commands.
        if '/' in p or '.' in p or os.path.exists(p):
            paths.append(p.strip())

    return paths

def confirm_destructive_command(command):
    """Asks for user confirmation for destructive commands."""
    command_parts = command.strip().split()
    if not command_parts:
        return True

    cmd = command_parts[0]
    if cmd in DESTRUCTIVE_COMMANDS:
        print(f"You are about to run a potentially destructive command: '{command}'")
        response = input("Are you sure you want to continue? (y/n): ").lower().strip()
        return response == 'y'
    return True

def validate_command(command):
    """Validates a command against all safety checks."""
    paths = get_command_paths(command)
    for path in paths:
        resolved_path = resolve_path(path)
        if is_dangerous_path(resolved_path):
            print(f"Error: Operation on dangerous path '{resolved_path}' is not allowed.")
            return False

    if not confirm_destructive_command(command):
        print("Operation cancelled by user.")
        return False

    return True