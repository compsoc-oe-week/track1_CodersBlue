"""
This module provides functions for generating ASCII art, such as directory trees and bar charts.
"""

def draw_directory_tree(structure, prefix=""):
    """
    Recursively draws a directory tree.
    'structure' should be a dictionary where keys are directory or file names
    and values are sub-dictionaries for directories or None for files.
    """
    lines = []
    items = sorted(structure.items())
    for i, (name, content) in enumerate(items):
        connector = "├── " if i < len(items) - 1 else "└── "
        lines.append(f"{prefix}{connector}{name}")
        if isinstance(content, dict):
            extension = "│   " if i < len(items) - 1 else "    "
            lines.extend(draw_directory_tree(content, prefix + extension).splitlines())
    return "\n".join(lines)

def draw_bar_chart(data, max_width=50):
    """
    Draws a simple horizontal bar chart.
    'data' should be a dictionary of labels and values.
    """
    lines = []
    if not data:
        return ""

    max_label_length = max(len(label) for label in data.keys())
    max_value = max(data.values())

    if max_value == 0:
        for label, value in data.items():
            lines.append(f"{label.ljust(max_label_length)} │ 0")
        return "\n".join(lines)

    scale = max_width / max_value

    for label, value in data.items():
        bar_length = int(value * scale)
        bar = '█' * bar_length
        lines.append(f"{label.ljust(max_label_length)} │ {bar} {value}")

    return "\n".join(lines)