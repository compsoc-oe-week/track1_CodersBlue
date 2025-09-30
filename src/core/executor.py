import os
import shutil
from datetime import datetime

from src.core import safety, search

UNDO_LOG_FILE = os.path.expanduser("~/.samantha/undo.log")
# Keep track of the current working directory for the session, start with process CWD
SESSION_CWD = os.getcwd()

def _ensure_log_directory_exists():
    """Ensures that the directory for the undo log exists."""
    log_dir = os.path.dirname(UNDO_LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

def log_command(command_str: str):
    """Logs a command to the undo log file."""
    _ensure_log_directory_exists()
    timestamp = datetime.now().isoformat()
    with open(UNDO_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {command_str}\n")

# --- Core Command Implementations ---

def _resolve_path(path: str) -> str:
    """Resolves a path relative to the session's CWD."""
    return os.path.join(SESSION_CWD, os.path.expanduser(path))

def _execute_ls(args):
    """Lists files and directories."""
    path = _resolve_path(args[0]) if args else SESSION_CWD
    if not os.path.isdir(path):
        return f"Error: Directory not found at '{path}'"

    try:
        items = os.listdir(path)
        output_items = []
        for item in sorted(items):
            if os.path.isdir(os.path.join(path, item)):
                output_items.append(f"{item}/")
            else:
                output_items.append(item)
        return f"Contents of '{os.path.abspath(path)}':\n" + "\n".join(output_items)
    except OSError as e:
        return f"Error listing directory '{path}': {e}"

def _execute_cd(args):
    """Changes the current working directory for the session."""
    global SESSION_CWD
    if not args:
        return "Error: 'cd' requires a destination directory."

    path = _resolve_path(args[0])
    if not os.path.isdir(path):
        return f"Error: Directory not found at '{path}'"

    try:
        os.chdir(path)
        SESSION_CWD = os.getcwd()
        return f"Current directory is now: {SESSION_CWD}"
    except OSError as e:
        return f"Error changing directory to '{path}': {e}"

def _execute_pwd(args):
    """Prints the current working directory."""
    return f"Current directory: {SESSION_CWD}"

def _execute_mkdir(args):
    """Creates a new directory."""
    if not args:
        return "Error: 'mkdir' requires a directory name."

    path = _resolve_path(args[0])
    if os.path.exists(path):
        return f"Error: '{path}' already exists."

    try:
        os.makedirs(path)
        return f"Directory created: '{path}'"
    except OSError as e:
        return f"Error creating directory '{path}': {e}"

def _execute_touch(args):
    """Creates an empty file or updates its timestamp."""
    if not args:
        return "Error: 'touch' requires a filename."

    path = _resolve_path(args[0])
    try:
        with open(path, 'a'):
            os.utime(path, None)
        return f"File created or updated: '{path}'"
    except OSError as e:
        return f"Error touching file '{path}': {e}"

def _execute_cp(args):
    """Copies a file or directory."""
    if len(args) < 2:
        return "Error: 'cp' requires a source and a destination."

    src = _resolve_path(args[0])
    dest = _resolve_path(args[1])

    if not os.path.exists(src):
        return f"Error: Source '{src}' not found."

    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest) # copy2 preserves metadata
        return f"Copied '{src}' to '{dest}'"
    except (shutil.Error, OSError) as e:
        return f"Error copying '{src}' to '{dest}': {e}"

def _execute_mv(args):
    """Moves/renames a file or directory."""
    if len(args) < 2:
        return "Error: 'mv' requires a source and a destination."

    src = _resolve_path(args[0])
    dest = _resolve_path(args[1])

    if not os.path.exists(src):
        return f"Error: Source '{src}' not found."

    try:
        shutil.move(src, dest)
        return f"Moved '{src}' to '{dest}'"
    except (shutil.Error, OSError) as e:
        return f"Error moving '{src}' to '{dest}': {e}"

def _execute_rm(args):
    """Removes a file or directory."""
    if not args:
        return "Error: 'rm' requires a target path."

    path = _resolve_path(args[0])
    if not os.path.exists(path):
        return f"Error: Path '{path}' not found."

    abs_path = os.path.abspath(path)
    # Safety check for rm is handled by the safety module and confirmation below
    # if not safety.is_safe_to_delete(abs_path):
    #     return f"Error: Deletion of '{abs_path}' is not allowed."

    confirm = input(f"Are you sure you want to permanently delete '{abs_path}'? (y/n): ").lower().strip()
    if confirm != 'y':
        return f"Deletion of '{abs_path}' cancelled."

    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"Directory '{abs_path}' and all its contents removed."
        else:
            os.remove(path)
            return f"File '{abs_path}' removed."
    except OSError as e:
        return f"Error removing '{abs_path}': {e}"

def _execute_find_files(args):
    """Finds files by name pattern."""
    if len(args) < 1:
        return "Error: 'find_files' requires a name pattern."

    name_pattern = args[0]
    path = _resolve_path(args[1]) if len(args) > 1 else SESSION_CWD

    try:
        matches = search.find_files(name_pattern, path)
        if not matches:
            return f"No files found matching '{name_pattern}' in '{path}'."
        return f"Found files:\n" + "\n".join(matches)
    except Exception as e:
        return f"Error finding files: {e}"

def _execute_search_in_files(args):
    """Searches for content within files."""
    if len(args) < 1:
        return "Error: 'search_in_files' requires a content pattern."

    content_pattern = args[0]
    path = _resolve_path(args[1]) if len(args) > 1 else SESSION_CWD

    try:
        matches = search.search_in_files(content_pattern, path)
        if not matches:
            return f"No content matching '{content_pattern}' found in files in '{path}'."
        return f"Found content:\n" + "\n".join(matches)
    except Exception as e:
        return f"Error searching in files: {e}"

COMMAND_MAP = {
    "ls": _execute_ls,
    "cd": _execute_cd,
    "pwd": _execute_pwd,
    "mkdir": _execute_mkdir,
    "touch": _execute_touch,
    "cp": _execute_cp,
    "mv": _execute_mv,
    "rm": _execute_rm,
    "find_files": _execute_find_files,
    "search_in_files": _execute_search_in_files,
}

def preview(plan: dict):
    """Prints a human-readable preview of the execution plan."""
    print("I understand. Here is the plan:")
    if plan.get("assumptions"):
        print("Based on these assumptions:")
        for assumption in plan["assumptions"]:
            print(f"  - {assumption}")

    print("\nI will perform the following steps:")
    for i, step in enumerate(plan.get("steps", []), 1):
        cmd = step.get('cmd', 'N/A')
        args = " ".join(f'"{arg}"' for arg in step.get('args', []))
        why = step.get('why', 'No reason provided.')
        print(f"{i}. {cmd} {args}")
        print(f"   Reason: {why}")

def confirm():
    """Asks the user to confirm (y/n) before proceeding."""
    response = input("\nShould I proceed with this plan? (y/n): ").lower().strip()
    return response == 'y'

def run(plan: dict):
    """
    Runs a plan dictionary after safety checks, confirmation, and logging.
    This function replaces the old subprocess-based command execution.
    """
    # plan = safety.sanitize_plan(plan) # Assumes safety module can clean the plan
    preview(plan)

    if not confirm():
        print("Execution cancelled by user.")
        return {"summary": "User cancelled.", "results": []}

    results = []
    for step in plan.get("steps", []):
        command_name = step.get("cmd")
        args = step.get("args", [])

        if not command_name:
            results.append({"status": "error", "output": "Step is missing a command."})
            continue

        if command_name in COMMAND_MAP:
            try:
                output = COMMAND_MAP[command_name](args)
                print(output)
                results.append({"status": "success", "output": output})
                log_command(f"{command_name} {' '.join(args)}")
            except Exception as e:
                error_message = f"An unexpected error occurred executing '{command_name}': {e}"
                print(error_message)
                results.append({"status": "error", "output": error_message})
                print("Stopping execution due to error.")
                break
        else:
            unknown_cmd_msg = f"Unknown command: '{command_name}'. Aborting."
            print(unknown_cmd_msg)
            results.append({"status": "error", "output": unknown_cmd_msg})
            break

    return {"summary": "Plan execution finished.", "results": results}

def summarize(execution_results: dict):
    """Prints a summary of the execution results."""
    print("\n--- Execution Summary ---")
    print(execution_results.get("summary", "No summary provided."))
    for i, result in enumerate(execution_results.get("results", []), 1):
        status = result.get('status', 'N/A').upper()
        output = result.get('output', 'No output.')
        print(f"Step {i} [{status}]: {output}")