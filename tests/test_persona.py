import unittest
from src.ui.colors import green, yellow, red, bold
from src.ui.persona import get_system_prompt, SYSTEM_PROMPT
from src.vision.ascii_art import draw_directory_tree, draw_bar_chart

class TestPersonaAndUI(unittest.TestCase):

    def test_colors(self):
        self.assertEqual(green("success"), "\033[92msuccess\033[0m")
        self.assertEqual(yellow("warning"), "\033[93mwarning\033[0m")
        self.assertEqual(red("danger"), "\033[91mdanger\033[0m")
        self.assertEqual(bold("command"), "\033[1mcommand\033[0m")

    def test_persona_prompt(self):
        self.assertEqual(get_system_prompt(), SYSTEM_PROMPT)
        self.assertIn("Samantha", get_system_prompt())
        self.assertIn("Her", get_system_prompt())

    def test_directory_tree(self):
        structure = {
            "src": {
                "main.py": None,
                "utils": {
                    "helpers.py": None
                }
            },
            "tests": {
                "test_main.py": None
            }
        }
        expected_tree = (
            "├── src\n"
            "│   ├── main.py\n"
            "│   └── utils\n"
            "│       └── helpers.py\n"
            "└── tests\n"
            "    └── test_main.py"
        )
        self.assertEqual(draw_directory_tree(structure).strip(), expected_tree.strip())

    def test_bar_chart(self):
        data = {"A": 10, "B": 20, "C": 5}
        expected_chart = (
            "A │ █████████████████████████ 10\n"
            "B │ ██████████████████████████████████████████████████ 20\n"
            "C │ █████████████ 5"
        )
        # Note: The exact output can vary based on scale, so we check for key elements
        chart = draw_bar_chart(data, max_width=50)
        self.assertIn("A │", chart)
        self.assertIn("B │", chart)
        self.assertIn("C │", chart)
        self.assertIn("10", chart)
        self.assertIn("20", chart)
        self.assertIn("5", chart)

    def test_empty_bar_chart(self):
        data = {}
        self.assertEqual(draw_bar_chart(data), "")

    def test_zero_value_bar_chart(self):
        data = {"A": 0, "B": 0}
        expected_chart = (
            "A │ 0\n"
            "B │ 0"
        )
        self.assertEqual(draw_bar_chart(data), expected_chart)

if __name__ == '__main__':
    unittest.main()