import unittest
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui import colors, persona
from src.vision import ascii_art

class TestUIPersona(unittest.TestCase):

    def test_colors(self):
        """Test that the color functions wrap text in ANSI codes."""
        # The new implementation uses colorama, so we check for its output format
        self.assertIn("\x1b[32m", colors.green("success")) # GREEN
        self.assertIn("\x1b[33m", colors.yellow("warning")) # YELLOW
        self.assertIn("\x1b[31m", colors.red("danger"))   # RED
        self.assertIn("\x1b[36m", colors.cyan("info"))    # CYAN
        self.assertIn("\x1b[1m", colors.bold("command"))  # BOLD
        self.assertIn("\x1b[0m", colors.green("success")) # RESET

    def test_persona_greet(self):
        """Test the greeting function."""
        intent = "test my app"
        greeting = persona.greet(intent)
        self.assertIn("Samantha:", greeting)
        self.assertIn(intent, greeting)

    def test_persona_inform_error(self):
        """Test the error reporting function."""
        error_msg = "something broke"
        error_info = persona.inform_error(error_msg)
        self.assertIn("Samantha:", error_info)
        self.assertIn("snag", error_info)
        self.assertIn(error_msg, error_info)

    def test_directory_tree(self):
        """Test the ASCII directory tree drawing function."""
        structure = {"src": {"main.py": None}, "README.md": None}
        tree = ascii_art.draw_directory_tree(structure)
        self.assertIn("src", tree)
        self.assertIn("main.py", tree)
        self.assertIn("README.md", tree)
        self.assertIn("├──", tree)
        self.assertIn("└──", tree)

    def test_bar_chart(self):
        """Test the ASCII bar chart drawing function."""
        data = {"A": 10, "B": 20}
        chart = ascii_art.draw_bar_chart(data, max_width=20)
        self.assertIn("A │", chart)
        self.assertIn("B │", chart)
        self.assertIn("10", chart)
        self.assertIn("20", chart)
        self.assertIn("███", chart) # Check for the bar character

if __name__ == '__main__':
    unittest.main()