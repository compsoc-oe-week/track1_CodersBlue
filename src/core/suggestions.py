import os
import glob

def suggest_desktop_cleanup(desktop_path="~/Desktop", threshold=5):
    """
    Analyzes the desktop for a large number of specific file types (e.g., screenshots)
    and suggests moving them to a dedicated folder.
    """
    desktop_path = os.path.expanduser(desktop_path)
    if not os.path.isdir(desktop_path):
        return None

    # Common screenshot patterns for macOS and other systems
    screenshot_patterns = [
        os.path.join(desktop_path, "Screen Shot *.png"),
        os.path.join(desktop_path, "Screenshot_*.png")
    ]

    screenshot_files = []
    for pattern in screenshot_patterns:
        screenshot_files.extend(glob.glob(pattern))

    if len(screenshot_files) >= threshold:
        suggestion = {
            "type": "organizational",
            "title": "Desktop Cleanup Suggestion",
            "message": f"You have {len(screenshot_files)} screenshots on your Desktop. Would you like to move them to a 'Screenshots' folder?",
            "actionable_plan": {
                "assumptions": [
                    "The user wants to organize their desktop.",
                    f"A 'Screenshots' folder will be created on the Desktop if it doesn't exist."
                ],
                "steps": [
                    {
                        "cmd": "mkdir",
                        "args": [os.path.join(desktop_path, "Screenshots")],
                        "why": "To create a dedicated folder for screenshots on the Desktop."
                    },
                    {
                        "cmd": "mv",
                        "args": screenshot_files + [os.path.join(desktop_path, "Screenshots")],
                        "why": "To move all detected screenshots into the new folder."
                    }
                ]
            }
        }
        return suggestion

    return None