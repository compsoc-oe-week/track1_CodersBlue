import unittest
from unittest.mock import patch, mock_open, call
import subprocess
import os
from datetime import datetime

# It's good practice to make sure the test can find the modules it needs to test.
# This assumes the test is run from the root directory of the project.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import executor
from src.core import safety

class TestExecutor(unittest.TestCase):

    def setUp(self):
        """Set up a clean environment for each test."""
        # Define a temporary log file path to avoid cluttering the user's home directory
        self.test_log_file = "test_undo.log"
        executor.UNDO_LOG_FILE = self.test_log_file
        # Ensure the log file doesn't exist before a test
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def tearDown(self):
        """Clean up after each test."""
        # Remove the temporary log file
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        # Restore the original log file path if needed, though it's less critical in a test suite
        executor.UNDO_LOG_FILE = os.path.expanduser("~/.samantha/undo.log")

    @patch('sys.stdout')
    def test_preview_commands(self, mock_stdout):
        """Test that the command preview prints correctly."""
        from io import StringIO

        commands = ["echo 'hello'", "ls -l"]

        # Redirect stdout to a string buffer
        with patch('sys.stdout', new=StringIO()) as fake_out:
            executor.preview_commands(commands)
            output = fake_out.getvalue()

        # Check the captured output
        self.assertIn("Planned commands:", output)
        self.assertIn("1. echo 'hello'", output)
        self.assertIn("2. ls -l", output)

    @patch('builtins.input', return_value='y')
    def test_confirm_execution_yes(self, mock_input):
        """Test that confirmation returns True for 'y'."""
        self.assertTrue(executor.confirm_execution())

    @patch('builtins.input', return_value='n')
    def test_confirm_execution_no(self, mock_input):
        """Test that confirmation returns False for 'n'."""
        self.assertFalse(executor.confirm_execution())

    @patch('src.core.executor.log_command')
    @patch('subprocess.run')
    @patch('src.core.safety.validate_command', return_value=True)
    @patch('builtins.input', return_value='y')
    def test_run_commands_successful_execution(self, mock_input, mock_validate, mock_run, mock_log):
        """Test a full successful run of a single command."""
        commands = ["ls -la"]
        # Mock a successful subprocess result
        mock_run.return_value = subprocess.CompletedProcess(args=commands[0], returncode=0, stdout="files", stderr="")

        executor.run_commands(commands)

        mock_validate.assert_called_once_with(commands[0])
        mock_run.assert_called_once_with(commands[0], shell=True, check=True, text=True, capture_output=True)
        mock_log.assert_called_once_with(commands[0])

    @patch('builtins.input', return_value='n')
    @patch('subprocess.run')
    def test_run_commands_user_cancels(self, mock_run, mock_input):
        """Test that no command is run if the user cancels."""
        commands = ["do-not-run"]
        executor.run_commands(commands)
        mock_run.assert_not_called()

    @patch('src.core.safety.validate_command', return_value=False)
    @patch('builtins.input', return_value='y')
    @patch('subprocess.run')
    def test_run_commands_skips_unsafe_command(self, mock_run, mock_input, mock_validate):
        """Test that unsafe commands are skipped."""
        commands = ["rm -rf /"]
        executor.run_commands(commands)
        mock_validate.assert_called_once_with(commands[0])
        mock_run.assert_not_called()

    def test_log_command(self):
        """Test that the undo log is written to correctly."""
        command = "echo 'test log'"
        # Ensure the log directory exists (the function should handle this)
        executor.log_command(command)

        self.assertTrue(os.path.exists(self.test_log_file))
        with open(self.test_log_file, "r") as f:
            content = f.read()
            self.assertIn(command, content)
            # Check for a rough timestamp format to ensure it's being logged
            self.assertRegex(content, r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+')

if __name__ == '__main__':
    unittest.main()