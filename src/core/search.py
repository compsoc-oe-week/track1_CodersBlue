import subprocess
import difflib

def find_files(name_pattern, path='.'):
    """
    Finds files by name using the find command.
    """
    try:
        result = subprocess.run(['find', path, '-name', name_pattern], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output:
            return []
        return output.split('\n')
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

def search_in_files(content_pattern, path='.'):
    """
    Searches for content in files using grep.
    """
    try:
        # Don't use check=True, as grep returns 1 when no matches are found.
        result = subprocess.run(['grep', '-r', content_pattern, path], capture_output=True, text=True)
        if result.returncode > 1:
            # An actual error occurred.
            return []

        output = result.stdout.strip()
        if not output:
            return []
        return output.split('\n')
    except FileNotFoundError:
        # grep is not installed
        return []

def find_best_match(query, candidates):
    """
    Finds the best fuzzy match for a query from a list of candidates.
    """
    if not candidates:
        return []
    return difflib.get_close_matches(query, candidates, n=1, cutoff=0.6)