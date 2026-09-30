


"""Command-line entry point for FolderLens."""

import argparse
import sys
from pathlib import Path

from analyzer import analyze_project, list_project_directories
from ui import console, show_analysis, show_banner, show_help, show_menu


VERSION = "1.0.0"


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Tampilkan struktur folder dan ringkasan project.",
        epilog="Contoh: folderlens .",
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="Path folder project yang akan dianalisis.",
    )
    parser.add_argument(
        "--include",
        action="extend",
        nargs="+",
        metavar="FOLDER",
        help="Analisis hanya folder relatif yang dipilih, contoh: --include src tests.",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"FolderLens {VERSION}",
    )
    return parser


def _prompt_for_folders(project_path: Path) -> list[str] | None:
    """Prompt for project subfolders, returning None to analyze the whole project."""
    folders = list_project_directories(project_path)
    if not folders:
        console.print("Tidak ada subfolder yang dapat dipilih; seluruh folder dianalisis.", style="dim")
        return None

    console.print("\n[bold]Pilih subfolder yang ingin dianalisis:[/]")
    for index, folder in enumerate(folders, start=1):
        console.print(f"  [cyan]{index}[/]. {folder}")
    console.print("Pisahkan nomor dengan koma. Kosongkan untuk menganalisis semua folder.", style="dim")

    while True:
        selection = console.input("[bold cyan]Pilihan[/]: ").strip()
        if not selection:
            return None

        try:
            indexes = [int(value.strip()) for value in selection.split(",")]
            if not indexes or any(index < 1 or index > len(folders) for index in indexes):
                raise ValueError
        except ValueError:
            console.print("Masukkan nomor folder yang tersedia, dipisahkan koma.", style="bold red")
            continue

        return list(dict.fromkeys(folders[index - 1] for index in indexes))


def analyze_path(
    path: Path,
    include_dirs: list[str] | None = None,
    prompt_for_folders: bool = False,
) -> int:
    """Validate and analyze one folder path."""
    try:
        if not path.exists():
            console.print(f"Error: Folder tidak ditemukan:\n{path}", style="bold red")
            return 1
        if not path.is_dir():
            console.print(f"Error: Path bukan folder:\n{path}", style="bold red")
            return 1
        project_path = path.resolve()
    except OSError as error:
        console.print(
            f"Error: Tidak dapat mengakses folder:\n{path}\n{error}",
            style="bold red",
        )
        return 1

    if prompt_for_folders:
        include_dirs = _prompt_for_folders(project_path)

    try:
        analysis = analyze_project(project_path, include_dirs)
    except ValueError as error:
        console.print(f"Error: {error}", style="bold red")
        return 1

    show_analysis(analysis)
    return 0


def run_menu() -> int:
    """Show the Rich menu and respond to the selected action."""
    show_banner(VERSION)
    while True:
        choice = show_menu()
        if choice == "0":
            console.print("Sampai jumpa!", style="dim")
            return 0
        if choice == "1":
            path_text = console.input("[bold cyan]Path folder[/] [dim](kosong = .):[/] ")
            path_text = path_text.strip().strip('"') or "."
            analyze_path(Path(path_text), prompt_for_folders=True)
        elif choice == "2":
            show_help()
        elif choice == "3":
            console.print(f"FolderLens {VERSION}", style="bold yellow")


def main() -> int:
    """Start the menu or analyze a folder passed as an argument."""
    parser = create_parser()
    args = parser.parse_args()

    if args.path is not None or args.include is not None:
        return analyze_path(args.path or Path("."), args.include)
    return run_menu()


if __name__ == "__main__":
    raise SystemExit(main())
