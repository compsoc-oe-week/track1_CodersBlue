import unittest
import json
import os
from unittest.mock import patch, MagicMock

# Add src to path to allow importing nl2cmd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.nl2cmd import nl_to_plan, InvalidPlanError, _validate_plan_structure

class TestNl2Cmd(unittest.TestCase):

    @patch.dict(os.environ, {"CODER_BASE_URL": "http://fake-url"})
    @patch("core.nl2cmd.openai.OpenAI")
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

    @patch.dict(os.environ, {"CODER_BASE_URL": "http://fake-url"})
    @patch("core.nl2cmd.openai.OpenAI")
    def test_nl_to_plan_retry_on_invalid_json(self, mock_openai_class):
        """Test retry logic when the model returns invalid JSON first."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        valid_plan = {
            "steps": [{"cmd": "cat", "args": ["file.txt"], "why": "Read file."}],
            "assumptions": []
        }
        invalid_response = MagicMock()
        invalid_response.choices[0].message.content = "this is not json"
        valid_response = MagicMock()
        valid_response.choices[0].message.content = json.dumps(valid_plan)

        # Simulate invalid JSON, then valid JSON
        mock_client.chat.completions.create.side_effect = [invalid_response, valid_response]

        plan = nl_to_plan("read file.txt")
        self.assertEqual(plan, valid_plan)
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)

    @patch.dict(os.environ, {"CODER_BASE_URL": "http://fake-url"})
    @patch("core.nl2cmd.openai.OpenAI")
    def test_nl_to_plan_fail_after_max_retries(self, mock_openai_class):
        """Test that InvalidPlanError is raised after max retries."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        invalid_response = MagicMock()
        invalid_response.choices[0].message.content = "invalid json"
        mock_client.chat.completions.create.return_value = invalid_response

        with self.assertRaises(InvalidPlanError):
            nl_to_plan("some command")

        # Check that it was called MAX_RETRIES times (defined in nl2cmd.py)
        from core.nl2cmd import MAX_RETRIES
        self.assertEqual(mock_client.chat.completions.create.call_count, MAX_RETRIES)

    @patch.dict(os.environ, {}, clear=True)
    def test_nl_to_plan_no_base_url(self):
        """Test that a ValueError is raised if CODER_BASE_URL is not set."""
        with self.assertRaises(ValueError):
            nl_to_plan("any command")

    def test_validate_plan_structure(self):
        """Test the plan structure validation logic."""
        valid_plan = {
            "steps": [{"cmd": "c", "args": ["a"], "why": "w"}],
            "assumptions": ["a"]
        }
        self.assertTrue(_validate_plan_structure(valid_plan))

        # Test invalid structures
        self.assertFalse(_validate_plan_structure({}))
        self.assertFalse(_validate_plan_structure({"steps": []}))
        self.assertFalse(_validate_plan_structure({"assumptions": []}))
        self.assertFalse(_validate_plan_structure({"steps": "not a list", "assumptions": []}))
        self.assertFalse(_validate_plan_structure({"steps": [{}], "assumptions": []}))
        self.assertFalse(_validate_plan_structure({"steps": [{"cmd": 1}], "assumptions": []}))

if __name__ == "__main__":
    unittest.main()