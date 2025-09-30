import json
from typing import Dict

def create_mock_plan(user_intent: str) -> Dict:
    """
    Generates a mock plan based on simple keyword matching for testing purposes.
    This is a placeholder for the real AI-based planning.
    """
    user_intent = user_intent.lower()
    words = user_intent.split()

    plan = {
        "assumptions": ["Running in mock mode. This is not a real AI-generated plan."],
        "steps": []
    }

    # Command matching logic (ordered by likely specificity)
    if "find files" in user_intent:
        try:
            name_pattern_index = words.index("named") + 1
            path_index = words.index("in") + 1
            name_pattern = words[name_pattern_index].strip("'\"")
            path = " ".join(words[path_index:]).strip("'\"")
            plan["steps"].append({
                "cmd": "find_files",
                "args": [name_pattern, path],
                "why": "To find files matching the specified pattern in the given directory."
            })
        except (ValueError, IndexError):
            pass  # Fallback to the generic error message if parsing fails
    elif "search for" in user_intent:
        try:
            for_index = words.index("for")
            content_start_index = for_index + 1
            path = "."
            content_end_index = len(words)

            if "in" in words[content_start_index:]:
                in_index = words.index("in", content_start_index)
                content_end_index = in_index
                path_start_index = in_index + 1
                if path_start_index < len(words):
                    path = " ".join(words[path_start_index:]).strip("'\"")

            content_pattern = " ".join(words[content_start_index:content_end_index]).strip("'\"")
            plan["steps"].append({
                "cmd": "search_in_files",
                "args": [content_pattern, path],
                "why": "To search for content in files in the specified directory."
            })
        except (ValueError, IndexError):
            pass
    elif "copy" in words or "cp" in words:
        try:
            to_index = words.index("to")
            cp_index = words.index("copy") if "copy" in words else words.index("cp")
            src = " ".join(words[cp_index + 1:to_index]).strip("'\"")
            dest = " ".join(words[to_index + 1:]).strip("'\"")
            plan["steps"].append({"cmd": "cp", "args": [src, dest], "why": "To copy a file or directory."})
        except (ValueError, IndexError):
            pass
    elif "move" in words or "mv" in words:
        try:
            to_index = words.index("to")
            mv_index = words.index("move") if "move" in words else words.index("mv")
            src = " ".join(words[mv_index + 1:to_index]).strip("'\"")
            dest = " ".join(words[to_index + 1:]).strip("'\"")
            plan["steps"].append({"cmd": "mv", "args": [src, dest], "why": "To move a file or directory."})
        except (ValueError, IndexError):
            pass
    elif "remove" in words or "delete" in words or "rm" in words:
        try:
            cmd_index = -1
            if "remove" in words: cmd_index = words.index("remove")
            elif "delete" in words: cmd_index = words.index("delete")
            else: cmd_index = words.index("rm")

            path = " ".join(words[cmd_index + 1:]).strip("'\"")
            plan["steps"].append({"cmd": "rm", "args": [path], "why": "To remove a file or directory."})
        except (ValueError, IndexError):
            pass
    elif ("make" in words and "directory" in words) or "mkdir" in words:
        try:
            path_start_word = "mkdir"
            if "directory" in words:
                path_start_word = "directory"

            path_index = words.index(path_start_word) + 1
            path = " ".join(words[path_index:]).strip("'\"")
            plan["steps"].append({"cmd": "mkdir", "args": [path], "why": "To create a directory."})
        except (ValueError, IndexError):
            pass
    elif ("create" in words and "file" in words) or "touch" in words:
        try:
            path_start_word = "touch"
            if "file" in words:
                path_start_word = "file"

            path_index = words.index(path_start_word) + 1
            path = " ".join(words[path_index:]).strip("'\"")
            plan["steps"].append({"cmd": "touch", "args": [path], "why": "To create a file."})
        except (ValueError, IndexError):
            pass
    elif "list" in words or "ls" in words:
        path = "."
        if "in" in words:
            try:
                path_index = words.index("in") + 1
                if path_index < len(words):
                    path = " ".join(words[path_index:]).strip("'\"")
            except (ValueError, IndexError):
                pass
        plan["steps"].append({
            "cmd": "ls",
            "args": [path],
            "why": "To list files in the specified directory."
        })
    elif "cd" in words or "go to" in user_intent or "change directory" in user_intent:
        try:
            path_start_index = -1
            if "to" in words: path_start_index = words.index("to") + 1
            elif "directory" in words: path_start_index = words.index("directory") + 1
            elif "cd" in words: path_start_index = words.index("cd") + 1

            if path_start_index != -1 and path_start_index < len(words):
                 path = " ".join(words[path_start_index:]).strip("'\"")
                 plan["steps"].append({"cmd": "cd", "args": [path], "why": "To change the current directory."})
        except (ValueError, IndexError):
            pass

    # If no command was successfully parsed, provide a fallback message.
    if not plan.get("steps"):
        plan["steps"].append({
            "cmd": "echo",
            "args": [f"I'm sorry, I couldn't understand the command '{user_intent}' in mock mode."],
            "why": "To inform the user that the command was not understood."
        })

    return plan