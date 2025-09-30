import unittest
from unittest.mock import patch, MagicMock
import os
import shutil

# Make sure the test can find the modules it needs to test.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import executor

class TestExecutor(unittest.TestCase):

    def setUp(self):
        """Set up a clean environment for each test."""
        self.test_log_file = "test_undo.log"
        self.test_dir = "test_temp_dir"
        executor.UNDO_LOG_FILE = self.test_log_file
        os.makedirs(self.test_dir, exist_ok=True)
        executor.SESSION_CWD = os.path.abspath(self.test_dir)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        executor.SESSION_CWD = os.getcwd()

    @patch('sys.stdout')
    def test_preview(self, mock_stdout):
        """Test that the plan preview prints correctly."""
        from io import StringIO
        plan = {"assumptions": ["Doing a test."], "steps": [{"cmd": "ls", "args": ["-la"], "why": "To see files."}]}
        with patch('sys.stdout', new=StringIO()) as fake_out:
            executor.preview(plan)
            output = fake_out.getvalue()
        self.assertIn("Here is the plan:", output)
        self.assertIn("Doing a test.", output)
        self.assertIn('1. ls "-la"', output)

    @patch('builtins.input', return_value='y')
    def test_confirm_yes(self, mock_input):
        self.assertTrue(executor.confirm())

    @patch('builtins.input', return_value='n')
    def test_confirm_no(self, mock_input):
        self.assertFalse(executor.confirm())

    def test_run_successful_execution(self):
        """Test a full successful run of a plan by mocking the command function."""
        plan = {"steps": [{"cmd": "ls", "args": ["."], "why": "testing"}]}

        # To test the dispatcher, we patch the command map itself
        mock_ls = MagicMock(return_value="ls success")
        with patch.dict(executor.COMMAND_MAP, {'ls': mock_ls}):
            with patch('src.core.executor.confirm', return_value=True):
                with patch('src.core.executor.preview'):
                    results = executor.run(plan)

        mock_ls.assert_called_once_with(['.'], {})
        self.assertEqual(results["results"][0]["status"], "success")
        self.assertEqual(results["results"][0]["output"], "ls success")

    @patch('src.core.executor.confirm', return_value=False)
    @patch('src.core.executor.preview')
    def test_run_user_cancels(self, mock_preview, mock_confirm):
        plan = {"steps": [{"cmd": "ls", "args": [], "why": "test"}]}
        with patch.dict(executor.COMMAND_MAP, {'ls': MagicMock()}) as mock_map:
            executor.run(plan)
            mock_map['ls'].assert_not_called()
        mock_preview.assert_called_once_with(plan)
        mock_confirm.assert_called_once()

    def test_execute_mkdir_and_ls(self):
        executor._execute_mkdir(["new_folder"])
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "new_folder")))
        result = executor._execute_ls([])
        self.assertIn("new_folder/", result)

    def test_execute_touch_and_rm(self):
        executor._execute_touch(["test_file.txt"])
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_file.txt")))
        with patch('builtins.input', return_value='y'):
            executor._execute_rm(["test_file.txt"])
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "test_file.txt")))

    def test_log_command(self):
        """Test that the undo log is written to correctly."""
        command_str = "ls -la"
        executor.log_command(command_str)
        self.assertTrue(os.path.exists(self.test_log_file))
        with open(self.test_log_file, "r") as f:
            content = f.read()
            self.assertIn(command_str, content)
            # Correct regex for ISO 8601 format with microseconds
            self.assertRegex(content, r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+.*')

if __name__ == '__main__':
    unittest.main()