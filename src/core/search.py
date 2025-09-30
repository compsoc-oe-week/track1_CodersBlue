import os
import fnmatch
import difflib
from datetime import datetime
from .utils import parse_size_filter, parse_date_filter, FILE_TYPE_MAPPINGS

def find_files(name_pattern, path='.', size=None, modified=None, file_type=None):
    """
    Finds files by name using a cross-platform implementation, with optional filters for size, modification date, and file type.
    """
    matches = []
    size_op, size_val = parse_size_filter(size)
    date_op, date_val = parse_date_filter(modified)

    type_extensions = None
    if file_type and file_type in FILE_TYPE_MAPPINGS:
        type_extensions = FILE_TYPE_MAPPINGS[file_type]

    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, name_pattern):
            filepath = os.path.join(root, filename)

            try:
                # Size filter
                if size_op and size_val is not None:
                    file_size = os.path.getsize(filepath)
                    if size_op == '>' and not file_size > size_val:
                        continue
                    if size_op == '<' and not file_size < size_val:
                        continue
                    if size_op == '=' and not file_size == size_val:
                        continue

                # Date filter
                if date_op and date_val:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    # '>' means older than, so mtime should be less than the calculated date
                    if date_op == '>' and not file_mtime < date_val:
                        continue
                    # '<' means newer than, so mtime should be greater than the calculated date
                    if date_op == '<' and not file_mtime > date_val:
                        continue
                    if date_op == '=' and not file_mtime.date() == date_val.date():
                        continue

                # File type filter
                if type_extensions:
                    if not any(filename.lower().endswith(ext) for ext in type_extensions):
                        continue

                matches.append(filepath)
            except FileNotFoundError:
                # File might have been deleted during the walk, so we skip it
                continue

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