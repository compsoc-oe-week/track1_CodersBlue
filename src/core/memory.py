import os
from typing import List, Dict, Any

class Memory:
    def __init__(self, max_history_size=10):
        self.last_plan: Dict[str, Any] = None
        self.last_results: List[Dict[str, Any]] = []
        self.last_working_directory: str = os.getcwd()
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_size = max_history_size

    def add_to_history(self, role: str, content: str):
        """Adds a new entry to the conversation history."""
        # Ensure role is either 'user' or 'assistant'
        if role not in ['user', 'assistant']:
            raise ValueError("Role must be 'user' or 'assistant'")

        self.conversation_history.append({"role": role, "content": content})

        # Trim history if it exceeds the max size
        if len(self.conversation_history) > self.max_history_size:
            # Keep the last `max_history_size` items
            self.conversation_history = self.conversation_history[-self.max_history_size:]

    def get_history(self) -> List[Dict[str, str]]:
        """Returns the current conversation history."""
        return self.conversation_history

    def get_history_as_text(self) -> str:
        """Returns the conversation history formatted as a single string."""
        return "\n".join([f"{item['role'].capitalize()}: {item['content']}" for item in self.conversation_history])

    def set_last_plan(self, plan: Dict[str, Any]):
        self.last_plan = plan

    def set_last_results(self, results: List[Dict[str, Any]]):
        self.last_results = results

    def set_last_working_directory(self, cwd: str):
        self.last_working_directory = cwd

    def get_last_plan(self) -> Dict[str, Any]:
        return self.last_plan

    def get_last_results(self) -> List[Dict[str, Any]]:
        return self.last_results

    def get_last_working_directory(self) -> str:
        return self.last_working_directory

    def resolve_pronoun(self, pronoun: str) -> List[str]:
        """
        Resolves a pronoun to the file paths from the last successful 'find_files' command.
        """
        if pronoun.lower() in ['them', 'those', 'those files', 'it']:
            # Find the last successful find_files result
            for result in reversed(self.last_results):
                if result.get("status") == "success" and "find_files" in result.get("output", ""):
                    # This is a bit brittle; assumes a specific output format.
                    # A better approach would be to have structured output from commands.
                    try:
                        lines = result["output"].strip().split('\n')
                        if lines and lines[0].startswith("Found files:"):
                            return [line.strip() for line in lines[1:] if line.strip()]
                    except (IndexError, AttributeError):
                        continue
        return None

    def update(self, plan: Dict[str, Any], results: List[Dict[str, Any]], user_request: str):
        """
        Updates the memory with the latest plan, results, and conversation history.
        """
        self.set_last_plan(plan)
        self.set_last_results(results)
        self.add_to_history("user", user_request)
        # We could add the assistant's response (plan) here too, if desired
        # self.add_to_history("assistant", json.dumps(plan))