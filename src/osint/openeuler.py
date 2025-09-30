import subprocess
import logging

def _run_command(command: list[str]) -> str:
    """
    Runs a system command and returns its output.

    TODO: Add more robust error handling.
    """
    try:
        logging.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        logging.error(f"Command not found: {command[0]}")
        return f"Error: Command not found: {command[0]}"
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {' '.join(command)}\n{e.stderr}")
        return f"Error: {e.stderr}"

def get_kernel_version() -> str:
    """Returns the current kernel version."""
    return _run_command(["uname", "-r"])

def list_installed_kernels() -> str:
    """Lists all installed kernel packages."""
    # TODO: This command might need adjustment based on the exact openEuler setup.
    return _run_command(["rpm", "-q", "kernel"])

def dnf_search(pkg: str) -> str:
    """Searches for a package using DNF."""
    return _run_command(["dnf", "search", pkg])

def dnf_info(pkg: str) -> str:
    """Gets information about a package using DNF."""
    return _run_command(["dnf", "info", pkg])

def dnf_install(pkg: str) -> str:
    """
    Installs a package using DNF.

    TODO: Implement a safer way to handle package installation.
    This should probably require user confirmation.
    """
    return _run_command(["dnf", "install", "-y", pkg])