import os
import json
import openai
from typing import Dict
from dotenv import load_dotenv

MAX_RETRIES = 3

class InvalidPlanError(Exception):
    """Raised when the plan from the model is invalid."""
    pass

# A more detailed system prompt that defines the available tools and provides few-shot examples.
SYSTEM_PROMPT = """
You are Samantha, a helpful AI assistant that converts natural language requests into a structured JSON plan for a Python execution engine.
You are empathetic, knowledgeable, and prioritize safety. Your goal is to create a clear, step-by-step plan that the user can approve.

The execution engine has the following Python functions available:
- `ls(path: str)`: Lists files and directories.
- `cd(path: str)`: Changes the current directory.
- `pwd()`: Shows the current directory.
- `mkdir(path: str)`: Creates a new directory.
- `touch(path: str)`: Creates an empty file.
- `cp(source: str, destination: str)`: Copies a file or directory.
- `mv(source: str, destination: str)`: Moves or renames a file or directory.
- `rm(path: str)`: Removes a file or directory (this is destructive and will require user confirmation).
- `find_files(name_pattern: str, path: str = '.')`: Finds files matching a pattern (e.g., '*.pdf').
- `search_in_files(content_pattern: str, path: str = '.')`: Searches for text content inside files.

Based on the user's request, provide a plan in the following JSON format.
Respond with ONLY the JSON object, nothing else.

{
    "assumptions": [
        "A list of any assumptions you made. For example, if a path is ambiguous, state the path you chose."
    ],
    "steps": [
        {
            "cmd": "command_name",
            "args": ["arg1", "arg2"],
            "why": "A brief, user-friendly justification for this step."
        }
    ]
}

---
Here are some examples:
---

User request: "Make a folder called 'Hackathon Project'"
{
    "assumptions": [
        "Creating the folder in the current directory."
    ],
    "steps": [
        {
            "cmd": "mkdir",
            "args": ["Hackathon Project"],
            "why": "To create the new folder as requested."
        }
    ]
}

---
User request: "copy all PDFs from downloads to docs"
{
    "assumptions": [
        "Assuming 'downloads' refers to './demo_data/downloads' and 'docs' refers to './demo_data/documents'.",
        "This plan will not run immediately; it will be previewed first."
    ],
    "steps": [
        {
            "cmd": "find_files",
            "args": ["*.pdf", "./demo_data/downloads"],
            "why": "First, I need to find all the PDF files in the downloads folder."
        },
        {
            "cmd": "cp",
            "args": ["{result_of_step_1}", "./demo_data/documents"],
            "why": "Then, I will copy the found PDF files to the documents folder."
        }
    ]
}

---
User request: "Show me what's in the new hackathon folder"
{
    "assumptions": [
        "Assuming the 'hackathon folder' is the 'Hackathon Project' directory created earlier."
    ],
    "steps": [
        {
            "cmd": "ls",
            "args": ["Hackathon Project"],
            "why": "To list the contents of the specified folder."
        }
    ]
}
"""

def _validate_plan_structure(plan: Dict) -> bool:
    """Validates the structure of the plan."""
    if not isinstance(plan, dict): return False
    if "steps" not in plan or "assumptions" not in plan: return False
    if not isinstance(plan["steps"], list) or not isinstance(plan["assumptions"], list): return False

    for step in plan["steps"]:
        if not isinstance(step, dict): return False
        if "cmd" not in step or "args" not in step or "why" not in step: return False
        if not isinstance(step["cmd"], str) or not isinstance(step["args"], list) or not isinstance(step["why"], str): return False
    return True

def nl_to_plan(text: str) -> Dict:
    """
    Converts a natural language string to a structured plan using an AI model.
    """
    load_dotenv()
    base_url = os.environ.get("CODER_BASE_URL")
    model_name = os.environ.get("CODER_MODEL_NAME")
    api_key = os.environ.get("OPENAI_API_KEY")

    if not base_url: raise ValueError("CODER_BASE_URL environment variable not set.")
    if not model_name: raise ValueError("CODER_MODEL_NAME environment variable not set.")
    if not api_key: raise ValueError("OPENAI_API_KEY environment variable not set (can be 'EMPTY').")

    client = openai.OpenAI(base_url=base_url, api_key=api_key)

    for _ in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Here is my request:\n\n{text}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.0, # Make the output deterministic
            )
            content = response.choices[0].message.content
            if content is None:
                continue

            plan = json.loads(content)

            if _validate_plan_structure(plan):
                return plan
            else:
                # Invalid structure, retry
                continue

        except (json.JSONDecodeError, openai.APIError) as e:
            # Invalid JSON or API error, retry
            print(f"Retrying due to error: {e}")
            continue

    raise InvalidPlanError(f"Failed to get a valid plan from the model after {MAX_RETRIES} retries.")

if __name__ == '__main__':
    # Example usage:
    # export CODER_BASE_URL=...
    # export CODER_MODEL_NAME=...
    # export OPENAI_API_KEY=EMPTY
    try:
        user_input = "copy all PDFs from ./demo_data/downloads to ./demo_data/documents"
        generated_plan = nl_to_plan(user_input)
        print(json.dumps(generated_plan, indent=2))
    except (ValueError, InvalidPlanError) as e:
        print(e)