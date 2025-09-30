import unittest
import json
import os
from unittest.mock import patch, MagicMock

# Add project root to path to allow importing src modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.nl2cmd import nl_to_plan, InvalidPlanError, _validate_plan_structure

class TestNl2Cmd(unittest.TestCase):

    MOCK_ENV = {
        "CODER_BASE_URL": "https://api.mock-openai.com/v1",
        "CODER_MODEL_NAME": "mock-coder-model",
        "OPENAI_API_KEY": "EMPTY"
    }

    @patch.dict(os.environ, MOCK_ENV)
    @patch("src.core.nl2cmd.openai.OpenAI")
    def test_nl_to_plan_success(self, mock_openai_class):
        """Test successful conversion of NL to a valid plan."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        valid_plan = {
            "steps": [{"cmd": "ls", "args": ["-l"], "why": "List files."}],
            "assumptions": ["I am in the correct directory."]
        }
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps(valid_plan)
        mock_client.chat.completions.create.return_value = mock_response

        plan = nl_to_plan("list all files")
        self.assertEqual(plan, valid_plan)
        mock_client.chat.completions.create.assert_called_once()

    @patch.dict(os.environ, MOCK_ENV)
    @patch("src.core.nl2cmd.openai.OpenAI")
    def test_nl_to_plan_retry_on_invalid_json(self, mock_openai_class):
        """Test retry logic when the model returns invalid JSON first."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        valid_plan = {"steps": [], "assumptions": []}
        mock_client.chat.completions.create.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content="not json"))]),
            MagicMock(choices=[MagicMock(message=MagicMock(content=json.dumps(valid_plan)))])
        ]

        plan = nl_to_plan("read file.txt")
        self.assertEqual(plan, valid_plan)
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)

    @patch.dict(os.environ, MOCK_ENV)
    @patch("src.core.nl2cmd.openai.OpenAI")
    def test_nl_to_plan_fail_after_max_retries(self, mock_openai_class):
        """Test that InvalidPlanError is raised after max retries."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = json.JSONDecodeError("err", "doc", 0)

        with self.assertRaises(InvalidPlanError):
            nl_to_plan("some command")

        from src.core.nl2cmd import MAX_RETRIES
        self.assertEqual(mock_client.chat.completions.create.call_count, MAX_RETRIES)

    @patch('src.core.nl2cmd.load_dotenv') # Prevent loading .env file for this test
    def test_nl_to_plan_raises_on_missing_env_vars(self, mock_load_dotenv):
        """Test that a ValueError is raised if environment variables are not set."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "CODER_BASE_URL"):
                nl_to_plan("any command")

        with patch.dict(os.environ, {"CODER_BASE_URL": "fake"}, clear=True):
            with self.assertRaisesRegex(ValueError, "CODER_MODEL_NAME"):
                nl_to_plan("any command")

        with patch.dict(os.environ, {"CODER_BASE_URL": "fake", "CODER_MODEL_NAME": "fake"}, clear=True):
            with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                nl_to_plan("any command")

    def test_validate_plan_structure(self):
        """Test the plan structure validation logic."""
        valid_plan = {"steps": [{"cmd": "c", "args": ["a"], "why": "w"}], "assumptions": ["a"]}
        self.assertTrue(_validate_plan_structure(valid_plan))

        self.assertFalse(_validate_plan_structure({}))
        self.assertFalse(_validate_plan_structure({"steps": "not a list", "assumptions": []}))
        self.assertFalse(_validate_plan_structure({"steps": [{"cmd": 1}], "assumptions": []}))

if __name__ == "__main__":
    unittest.main()