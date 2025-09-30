import json
import re
from typing import Dict, Optional

def _parse_single_command(user_intent: str) -> Optional[Dict]:
    """
    Parses a single command phrase into a plan step.
    Handles pronoun resolution for commands like 'mv' and 'cp'.
    """
    words = user_intent.strip().split()
    pronouns = ["them", "it", "those", "the files"]

    # Command matching logic (ordered by likely specificity)
    file_types = ["images", "documents", "videos", "audio", "archives"]
    is_find_query = "find" in words
    has_file_type_keyword = any(ft in user_intent for ft in file_types)

    if is_find_query and ("files" in user_intent or has_file_type_keyword):
        args = ["*", "."]
        kwargs = {}
        path_match = re.search(r"\s+in\s+((?:[a-zA-Z0-9._~-]+/)*[a-zA-Z0-9._~-]+)", user_intent)
        if path_match:
            args[1] = path_match.group(1).strip("'\"")
        name_match = re.search(r"\s+named\s+(['\"]?[\w*.-]+['\"]?)", user_intent)
        if name_match:
            args[0] = name_match.group(1).strip("'\"")
        size_larger_match = re.search(r"larger than\s+((?:\d+\.?\d*)\s*(?:kb|mb|gb|tb|b))", user_intent, re.IGNORECASE)
        if size_larger_match:
            kwargs["size"] = f">{size_larger_match.group(1).replace(' ', '').lower()}"
        size_smaller_match = re.search(r"smaller than\s+((?:\d+\.?\d*)\s*(?:kb|mb|gb|tb|b))", user_intent, re.IGNORECASE)
        if size_smaller_match:
            kwargs["size"] = f"<{size_smaller_match.group(1).replace(' ', '').lower()}"
        if "modified yesterday" in user_intent:
            kwargs["modified"] = "<1d"
        else:
            older_match = re.search(r"older than\s+(\d+)\s*days?", user_intent)
            if older_match:
                kwargs["modified"] = f">{older_match.group(1)}d"
            newer_match = re.search(r"newer than\s+(\d+)\s*days?", user_intent)
            if newer_match:
                kwargs["modified"] = f"<{newer_match.group(1)}d"
        for ft in file_types:
            if ft in user_intent:
                kwargs["file_type"] = ft
                break
        step = {"cmd": "find_files", "args": args, "why": "To find files based on advanced search criteria."}
        if kwargs:
            step["kwargs"] = kwargs
        return step

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
            return {"cmd": "search_in_files", "args": [content_pattern, path], "why": "To search for content in files."}
        except (ValueError, IndexError):
            return None

    elif "copy" in words or "cp" in words:
        try:
            to_index = words.index("to")
            cp_index = words.index("copy") if "copy" in words else words.index("cp")
            src = " ".join(words[cp_index + 1:to_index]).strip("'\"")
            dest = " ".join(words[to_index + 1:]).strip("'\"")
            if src.lower() in pronouns:
                src = "$results.last"
            return {"cmd": "cp", "args": [src, dest], "why": "To copy files or directories."}
        except (ValueError, IndexError):
            return None

    elif "move" in words or "mv" in words:
        try:
            to_index = words.index("to")
            mv_index = words.index("move") if "move" in words else words.index("mv")
            src = " ".join(words[mv_index + 1:to_index]).strip("'\"")
            dest = " ".join(words[to_index + 1:]).strip("'\"")
            if src.lower() in pronouns:
                src = "$results.last"
            return {"cmd": "mv", "args": [src, dest], "why": "To move files or directories."}
        except (ValueError, IndexError):
            return None

    elif "remove" in words or "delete" in words or "rm" in words:
        try:
            cmd_index = -1
            if "remove" in words: cmd_index = words.index("remove")
            elif "delete" in words: cmd_index = words.index("delete")
            else: cmd_index = words.index("rm")
            path = " ".join(words[cmd_index + 1:]).strip("'\"")
            if path.lower() in pronouns:
                path = "$results.last"
            return {"cmd": "rm", "args": [path], "why": "To remove files or directories."}
        except (ValueError, IndexError):
            return None

    elif ("make" in words and "directory" in words) or "mkdir" in words:
        try:
            path = ""
            if "mkdir" in words:
                path_index = words.index("mkdir") + 1
                if path_index < len(words):
                    path = " ".join(words[path_index:]).strip("'\"")
            elif "make" in words and "directory" in words:
                # Handle "make directory called 'name'" or "make directory name"
                if "called" in words:
                    path_index = words.index("called") + 1
                    if path_index < len(words):
                        path = " ".join(words[path_index:]).strip("'\"")
                else:
                    dir_index = words.index("directory")
                    if dir_index + 1 < len(words):
                        path = " ".join(words[dir_index + 1:]).strip("'\"")
            
            if path:
                return {"cmd": "mkdir", "args": [path], "why": "To create a directory."}
        except (ValueError, IndexError):
            return None

    elif "cd" in words or "go to" in user_intent or "change directory" in user_intent:
        try:
            path = ""
            if "cd" in words:
                path_index = words.index("cd") + 1
                if path_index < len(words):
                    path = " ".join(words[path_index:]).strip("'\"")
            elif "go to" in user_intent:
                to_index = words.index("to") + 1
                if to_index < len(words):
                    path = " ".join(words[to_index:]).strip("'\"")
            elif "change directory" in user_intent:
                dir_index = words.index("directory") + 1
                if dir_index < len(words):
                    path = " ".join(words[dir_index:]).strip("'\"")
            
            if path:
                return {"cmd": "cd", "args": [path], "why": "To change the current directory."}
        except (ValueError, IndexError):
            return None

    elif ("create" in words and "file" in words) or "touch" in words:
        try:
            path = ""
            if "touch" in words:
                path_index = words.index("touch") + 1
                if path_index < len(words):
                    path = " ".join(words[path_index:]).strip("'\"")
            elif "create" in words and "file" in words:
                # Handle "create file called 'name'" or "create file name"
                if "called" in words:
                    path_index = words.index("called") + 1
                    if path_index < len(words):
                        path = " ".join(words[path_index:]).strip("'\"")
                else:
                    file_index = words.index("file")
                    if file_index + 1 < len(words):
                        path = " ".join(words[file_index + 1:]).strip("'\"")
            
            if path:
                return {"cmd": "touch", "args": [path], "why": "To create a file."}
        except (ValueError, IndexError):
            return None

    elif "list" in words or "ls" in words:
        path = "."
        cmd_index = -1
        if "ls" in words: cmd_index = words.index("ls")
        elif "list" in words: cmd_index = words.index("list")

        # If 'in' is present, path is what follows
        if 'in' in words:
            try:
                path_index = words.index('in') + 1
                if path_index < len(words):
                    path = " ".join(words[path_index:]).strip("'\"")
            except (ValueError, IndexError):
                pass
        # else if there's text after the command itself
        elif cmd_index != -1 and cmd_index + 1 < len(words):
            # what if it's "list files"? then path becomes "files" which is wrong.
            # so we check if the word after the command is "files"
            if words[cmd_index+1] == 'files':
                # if there is something after 'files', it's the path
                if cmd_index + 2 < len(words):
                    path = " ".join(words[cmd_index+2:]).strip("'\"")
                # else path is "."
            else: # it is the path
                path = " ".join(words[cmd_index+1:]).strip("'\"")

        return {"cmd": "ls", "args": [path], "why": "To list files in a directory."}

    return None


def create_mock_plan(user_intent: str) -> Dict:
    """
    Generates a mock plan based on simple keyword matching for testing purposes.
    Supports multi-step commands separated by 'then'.
    """
    plan = {
        "assumptions": ["Running in mock mode. This is not a real AI-generated plan."],
        "steps": []
    }

    # Split commands by 'then' for multi-step operations
    commands = re.split(r'\s+then\s+', user_intent.lower())

    for command_phrase in commands:
        step = _parse_single_command(command_phrase)
        if step:
            plan["steps"].append(step)

    # If no command was successfully parsed, provide a fallback message.
    if not plan.get("steps"):
        plan["steps"].append({
            "cmd": "echo",
            "args": [f"I'm sorry, I couldn't understand the command '{user_intent}' in mock mode."],
            "why": "To inform the user that the command was not understood."
        })

    return plan