import os
import fnmatch
import difflib

def find_files(name_pattern, path='.'):
    """
    Finds files by name using a cross-platform implementation.
    """
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, name_pattern):
            matches.append(os.path.join(root, filename))
    return matches

def search_in_files(content_pattern, path='.'):
    """
    Searches for content in files using a cross-platform implementation.
    """
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        if content_pattern in line:
                            matches.append(f"{filepath}:{i}:{line.strip()}")
            except (IOError, OSError):
                # Ignore files that can't be opened
                continue
    return matches

def find_best_match(query, candidates):
    """
    Finds the best fuzzy match for a query from a list of candidates.
    """
    if not candidates:
        return []
    return difflib.get_close_matches(query, candidates, n=1, cutoff=0.6)