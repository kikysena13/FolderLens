import unittest

from formatter import format_markdown


class MarkdownFormatterTests(unittest.TestCase):
    def test_markdown_report_contains_summary_tree_and_explanation(self) -> None:
        analysis = {
            "tree": {
                "name": "demo",
                "type": "directory",
                "children": [
                    {"name": "src", "type": "directory", "children": []},
                    {"name": "main.py", "type": "file", "children": []},
                ],
            },
            "folder_count": 1,
            "file_count": 1,
            "project_type": "Python Project",
            "components": ["Source code"],
            "technologies": ["Python"],
            "explanation": "Contoh penjelasan.",
        }

        report = format_markdown(analysis)

        self.assertIn("# FolderLens Report", report)
        self.assertIn("- **Type:** Python Project", report)
        self.assertIn("📄 main.py", report)
        self.assertIn("Contoh penjelasan.", report)

    def test_tree_fence_cannot_be_closed_by_file_name(self) -> None:
        analysis = {
            "tree": {
                "name": "demo",
                "type": "directory",
                "children": [{"name": "```", "type": "file", "children": []}],
            },
            "folder_count": 0,
            "file_count": 1,
            "project_type": "General Project",
            "components": [],
            "technologies": [],
            "explanation": "Contoh penjelasan.",
        }

        report = format_markdown(analysis)

        self.assertIn("````\n📁 demo/", report)
        self.assertIn("└── 📄 ```", report)


if __name__ == "__main__":
    unittest.main()
