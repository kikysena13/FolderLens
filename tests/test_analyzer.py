import tempfile
import unittest
from pathlib import Path

from analyzer import analyze_project, list_project_directories


class AnalyzeProjectSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.project_path = Path(self.temporary_directory.name)
        (self.project_path / "src").mkdir()
        (self.project_path / "src" / "main.py").write_text("", encoding="utf-8")
        (self.project_path / "src" / "nested").mkdir()
        (self.project_path / "src" / "nested" / "helper.py").write_text(
            "", encoding="utf-8"
        )
        (self.project_path / "tests").mkdir()
        (self.project_path / "tests" / "test_main.py").write_text(
            "", encoding="utf-8"
        )
        (self.project_path / "README.md").write_text("", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_selected_folder_excludes_siblings_and_root_files(self) -> None:
        analysis = analyze_project(self.project_path, ["src"])

        self.assertEqual(analysis["file_count"], 2)
        self.assertEqual(analysis["folder_count"], 2)
        self.assertEqual(
            [child["name"] for child in analysis["tree"]["children"]], ["src"]
        )
        self.assertEqual(analysis["technologies"], ["Python"])

    def test_nested_folder_selection_keeps_its_tree_ancestors(self) -> None:
        analysis = analyze_project(self.project_path, ["src/nested"])

        self.assertEqual(analysis["file_count"], 1)
        self.assertEqual(analysis["folder_count"], 2)
        src = analysis["tree"]["children"][0]
        self.assertEqual(src["name"], "src")
        self.assertEqual([child["name"] for child in src["children"]], ["nested"])

    def test_invalid_or_outside_selection_is_rejected(self) -> None:
        for selected in ("missing", "../outside", str(self.project_path)):
            with self.subTest(selected=selected):
                with self.assertRaises(ValueError):
                    analyze_project(self.project_path, [selected])

    def test_directory_listing_uses_relative_paths(self) -> None:
        (self.project_path / "src" / "node_modules").mkdir()

        self.assertEqual(
            list_project_directories(self.project_path), ["src", "src/nested", "tests"]
        )

    def test_full_scan_still_includes_root_files_and_git_detection(self) -> None:
        (self.project_path / ".git").mkdir()

        analysis = analyze_project(self.project_path)

        self.assertEqual(analysis["file_count"], 4)
        self.assertIn("Git", analysis["technologies"])
        self.assertIn("Markdown", analysis["technologies"])

    def test_custom_excluded_directory_is_skipped_case_insensitively(self) -> None:
        analysis = analyze_project(self.project_path, excluded_dirs=["SRC"])

        self.assertEqual(analysis["file_count"], 2)
        self.assertEqual(analysis["folder_count"], 1)
        self.assertEqual(
            [child["name"] for child in analysis["tree"]["children"]],
            ["tests", "README.md"],
        )

        without_tests = analyze_project(self.project_path, excluded_dirs=["tests"])
        self.assertNotIn("Test directory", without_tests["components"])

    def test_max_depth_limits_directories_but_keeps_root_files(self) -> None:
        analysis = analyze_project(self.project_path, max_depth=1)

        self.assertEqual(analysis["folder_count"], 2)
        self.assertEqual(analysis["file_count"], 3)
        src = next(child for child in analysis["tree"]["children"] if child["name"] == "src")
        self.assertEqual([child["name"] for child in src["children"]], ["main.py"])

    def test_negative_max_depth_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            analyze_project(self.project_path, max_depth=-1)

if __name__ == "__main__":
    unittest.main()
