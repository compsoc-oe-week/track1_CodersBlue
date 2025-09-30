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

def _suggest_best_match(path_not_found: str, match_type: str = 'any') -> str:
    """Suggests a best match for a path that was not found."""
    parent_dir = os.path.dirname(path_not_found)
    target_name = os.path.basename(path_not_found)
    if not os.path.isdir(parent_dir):
        return ""
    try:
        all_items = os.listdir(parent_dir)
        candidates = []
        if match_type == 'dir':
            candidates = [item for item in all_items if os.path.isdir(os.path.join(parent_dir, item))]
        else: # 'any' (files or dirs)
            candidates = all_items
        best_match = search.find_best_match(target_name, candidates)
        if best_match:
            return f" Did you mean '{best_match[0]}'?"
        return ""
    except OSError:
        return ""

def _execute_ls(args, kwargs=None):
    """Lists files and directories."""
    path = _resolve_path(args[0]) if args else SESSION_CWD
    if not os.path.isdir(path):
        suggestion = _suggest_best_match(path, match_type='dir')
        return f"Error: Directory not found at '{path}'.{suggestion}"

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

def _execute_cd(args, kwargs=None):
    """Changes the current working directory for the session."""
    global SESSION_CWD
    if not args:
        return "Error: 'cd' requires a destination directory."

    path = _resolve_path(args[0])
    if not os.path.isdir(path):
        suggestion = _suggest_best_match(path, match_type='dir')
        return f"Error: Directory not found at '{path}'.{suggestion}"

    try:
        os.chdir(path)
        SESSION_CWD = os.getcwd()
        return f"Current directory is now: {SESSION_CWD}"
    except OSError as e:
        return f"Error changing directory to '{path}': {e}"

def _execute_pwd(args, kwargs=None):
    """Prints the current working directory."""
    return f"Current directory: {SESSION_CWD}"

def _execute_mkdir(args, kwargs=None):
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

def _execute_touch(args, kwargs=None):
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

def _execute_cp(args, kwargs=None):
    """Copies one or more files or directories to a destination."""
    if len(args) < 2:
        return "Error: 'cp' requires at least one source and a destination."
    dest_path = _resolve_path(args[-1])
    source_paths = [_resolve_path(arg) for arg in args[:-1]]
    if len(source_paths) > 1 and not os.path.isdir(dest_path):
        return f"Error: Destination '{dest_path}' is not a directory, which is required for copying multiple items."
    successes = []
    errors = []
    for src_path in source_paths:
        if not os.path.exists(src_path):
            suggestion = _suggest_best_match(src_path)
            errors.append(f"Source '{src_path}' not found.{suggestion}")
            continue
        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, os.path.join(dest_path, os.path.basename(src_path)))
            else:
                shutil.copy2(src_path, dest_path)
            successes.append(src_path)
        except (shutil.Error, OSError) as e:
            errors.append(f"Failed to copy '{src_path}': {e}")
    output = []
    if successes:
        output.append(f"Successfully copied {len(successes)} item(s) to '{dest_path}'.")
    if errors:
        output.append("Errors occurred:\n" + "\n".join(errors))
    return "\n".join(output) if output else "No items were copied."

def _execute_mv(args, kwargs=None):
    """Moves/renames one or more files or directories to a destination."""
    if len(args) < 2:
        return "Error: 'mv' requires at least one source and a destination."
    dest_path = _resolve_path(args[-1])
    source_paths = [_resolve_path(arg) for arg in args[:-1]]
    if len(source_paths) > 1 and not os.path.isdir(dest_path):
        return f"Error: Destination '{dest_path}' is not a directory, which is required for moving multiple items."
    successes = []
    errors = []
    for src_path in source_paths:
        if not os.path.exists(src_path):
            suggestion = _suggest_best_match(src_path)
            errors.append(f"Source '{src_path}' not found.{suggestion}")
            continue
        try:
            shutil.move(src_path, dest_path)
            successes.append(src_path)
        except (shutil.Error, OSError) as e:
            errors.append(f"Failed to move '{src_path}': {e}")
    output = []
    if successes:
        output.append(f"Successfully moved {len(successes)} item(s) to '{dest_path}'.")
    if errors:
        output.append("Errors occurred:\n" + "\n".join(errors))
    return "\n".join(output) if output else "No items were moved."

def _execute_rm(args, kwargs=None):
    """Removes one or more files or directories."""
    if not args:
        return "Error: 'rm' requires at least one target path."
    paths_to_delete = [_resolve_path(arg) for arg in args]
    existing_paths = []
    errors = []
    for path in paths_to_delete:
        if not os.path.exists(path):
            suggestion = _suggest_best_match(path)
            errors.append(f"Path '{os.path.abspath(path)}' not found.{suggestion}")
        else:
            existing_paths.append(path)
    if not existing_paths:
        return "Errors occurred:\n" + "\n".join(errors)
    abs_paths_to_delete = [os.path.abspath(p) for p in existing_paths]
    confirm = input(f"Are you sure you want to permanently delete:\n" + "\n".join(abs_paths_to_delete) + "\n(y/n): ").lower().strip()
    if confirm != 'y':
        return f"Deletion of {len(existing_paths)} item(s) cancelled."
    successes = []
    for path in existing_paths:
        abs_path = os.path.abspath(path)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            successes.append(abs_path)
        except OSError as e:
            errors.append(f"Error removing '{abs_path}': {e}")
    output = []
    if successes:
        output.append(f"Successfully removed {len(successes)} item(s).")
    if errors:
        output.append("Errors occurred:\n" + "\n".join(errors))
    return "\n".join(output) if output else "No items were removed."

def _execute_find_files(args, kwargs=None):
    """Finds files by name pattern, with optional advanced filters."""
    if kwargs is None:
        kwargs = {}
    if not args:
        return "Error: 'find_files' requires at least a name pattern."
    name_pattern = args[0]
    path = _resolve_path(args[1]) if len(args) > 1 else SESSION_CWD
    try:
        matches = search.find_files(name_pattern, path, **kwargs)
        if not matches:
            if kwargs:
                filters = ", ".join([f"{k}='{v}'" for k, v in kwargs.items()])
                return f"No files found matching '{name_pattern}' in '{path}' with filters: {filters}."
            return f"No files found matching '{name_pattern}' in '{path}'."
        return "Found files:\n" + "\n".join(matches)
    except Exception as e:
        return f"Error finding files: {e}"

def _execute_search_in_files(args, kwargs=None):
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
    preview(plan)
    if not confirm():
        print("Execution cancelled by user.")
        return {"summary": "User cancelled.", "results": []}

    results = []
    last_step_output_files = []

    for step in plan.get("steps", []):
        command_name = step.get("cmd")
        args = step.get("args", [])
        kwargs = step.get("kwargs", {})

        # --- Pronoun Resolution ---
        resolved_args = []
        pronoun_error = None
        for arg in args:
            if arg == "$results.last":
                if not last_step_output_files:
                    pronoun_error = "Used a pronoun like 'them' but the previous step produced no files."
                    break
                resolved_args.extend(last_step_output_files)
            else:
                resolved_args.append(arg)

        if pronoun_error:
            results.append({"status": "error", "output": pronoun_error})
            break

        args = resolved_args
        # --- End Pronoun Resolution ---

        if not command_name:
            results.append({"status": "error", "output": "Step is missing a command."})
            continue

        if command_name in COMMAND_MAP:
            try:
                output = COMMAND_MAP[command_name](args, kwargs)
                print(output)
                results.append({"status": "success", "output": output})

                if command_name == "find_files" and output.startswith("Found files:\n"):
                    # Handle case where no files are found
                    file_list = output.strip().split('\n')[1:]
                    last_step_output_files = [f for f in file_list if f] # Filter out empty strings
                else:
                    last_step_output_files = []

                log_args = ' '.join(map(str, args))
                log_kwargs = ' '.join([f"--{k}={v}" for k, v in kwargs.items()])
                log_command(f"{command_name} {log_args} {log_kwargs}".strip())
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