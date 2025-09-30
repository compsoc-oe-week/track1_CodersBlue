import subprocess
import os
from datetime import datetime
from src.core import safety

UNDO_LOG_FILE = os.path.expanduser("~/.samantha/undo.log")

def _ensure_log_directory_exists():
    """Ensures that the directory for the undo log exists."""
    log_dir = os.path.dirname(UNDO_LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

def preview_commands(commands):
    """Prints a numbered list of commands that are planned for execution."""
    print("Planned commands:")
    for i, command in enumerate(commands, 1):
        print(f"{i}. {command}")

def confirm_execution():
    """Asks the user to confirm (y/n) before proceeding."""
    response = input("Do you want to execute these commands? (y/n): ").lower().strip()
    return response == 'y'

def log_command(command):
    """Logs a command to the undo log file."""
    _ensure_log_directory_exists()
    timestamp = datetime.now().isoformat()
    with open(UNDO_LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {command}\n")

def run_commands(commands):
    """
    Runs a list of commands after safety checks, confirmation, and logging.
    """
    preview_commands(commands)

    if not confirm_execution():
        print("Execution cancelled by user.")
        return

    for command in commands:
        if not safety.validate_command(command):
            # The safety module will print its own error messages.
            print(f"Skipping unsafe command: {command}")
            continue

        try:
            # Execute the command
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

            # Log the successful command
            log_command(command)

            # Print stdout and stderr
            if result.stdout:
                print("STDOUT:")
                print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}")
            print(f"Return code: {e.returncode}")
            print("STDOUT:")
            print(e.stdout)
            print("STDERR:")
            print(e.stderr)
            # Decide if we should stop on error
            print("Stopping execution due to error.")
            break
        except Exception as e:
            print(f"An unexpected error occurred while executing '{command}': {e}")
            break