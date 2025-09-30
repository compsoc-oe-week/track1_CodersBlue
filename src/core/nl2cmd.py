import os
import json
import openai

from typing import Dict, List

MAX_RETRIES = 3

class InvalidPlanError(Exception):
    """Raised when the plan from the model is invalid."""
    pass

def _validate_plan_structure(plan: Dict) -> bool:
    """
    Validates the structure of the plan.

    The expected structure is:
    {
        "steps": [
            {"cmd": "...", "args": ["..."], "why": "..."}
        ],
        "assumptions": ["..."]
    }
    """
    if not isinstance(plan, dict):
        return False
    if "steps" not in plan or "assumptions" not in plan:
        return False
    if not isinstance(plan["steps"], list) or not isinstance(plan["assumptions"], list):
        return False

    for step in plan["steps"]:
        if not isinstance(step, dict):
            return False
        if "cmd" not in step or "args" not in step or "why" not in step:
            return False
        if not isinstance(step["cmd"], str) or not isinstance(step["args"], list) or not isinstance(step["why"], str):
            return False

    return True


def nl_to_plan(text: str) -> Dict:
    """
    Converts a natural language string to a structured plan using an AI model.

    Args:
        text: The natural language input from the user.

    Returns:
        A dictionary representing the structured plan.

    Raises:
        InvalidPlanError: If the model fails to return a valid plan after multiple retries.
        ValueError: If CODER_BASE_URL is not set.
    """
    base_url = os.environ.get("CODER_BASE_URL")
    if not base_url:
        raise ValueError("CODER_BASE_URL environment variable not set.")

    client = openai.OpenAI(base_url=base_url)

    prompt = f"""
    You are a helpful assistant that converts natural language commands into a structured JSON plan.
    The user wants to achieve the following: "{text}"

    Please provide a plan in the following JSON format:
    {{
        "steps": [
            {{
                "cmd": "command_name",
                "args": ["arg1", "arg2"],
                "why": "A brief justification for this step."
            }}
        ],
        "assumptions": [
            "Any assumptions you made."
        ]
    }}

    Respond with only the JSON object.
    """

    for _ in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="gpt-4", # Or any other compatible model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that converts natural language commands into a structured JSON plan."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
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

        except (json.JSONDecodeError, openai.APIError):
            # Invalid JSON or API error, retry
            continue

    raise InvalidPlanError(f"Failed to get a valid plan from the model after {MAX_RETRIES} retries.")

if __name__ == '__main__':
    # Example usage (requires CODER_BASE_URL to be set)
    # export CODER_BASE_URL=...
    try:
        user_input = "list all files in the current directory, then read the first one"
        generated_plan = nl_to_plan(user_input)
        print(json.dumps(generated_plan, indent=2))
    except (ValueError, InvalidPlanError) as e:
        print(e)