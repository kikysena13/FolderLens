from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich.prompt import Prompt

console = Console()


def show_banner(version: str) -> None:
    """Display the FolderLens welcome panel with its Braille dot-art logo."""
    logo_art = (
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡆⠀⠀⠀⠀⠀⢀⣾⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣷⡄⠀⠀⠀⢠⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⢻⣷⣄⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣶⣤⣤⣿⣿⣿⣿⡆⠀⠀⠀⠀⢀⣀⣠⣤⣤⣤⣄⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠈⢿⣿⣷⣤⣀⣀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣠⣴⣾⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢋⣉⣩⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣿⣿⠟⢡⢶⠷⡻⡵⡿⡿⣟⣶⡌⠻⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⢏⣠⣿⡳⡻⡚⡚⠝⣼⢼⣕⢽⣦⠜⣿⣿⣿⣇⣀⣀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠲⢶⣤⣤⣤⣤⣤⣴⣾⣿⣿⣿⣿⢫⣯⡟⡯⡋⡑⡈⢚⠢⢎⢮⣾⢿⡯⣺⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀\n"
        "⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⢝⣿⣪⡾⣩⠢⡡⣰⢈⣌⢕⡾⣻⡮⣺⣿⣿⣿⣿⡿⠟⠛⠻⠿⠿⢷⣄\n"
        "⠀⠀⠀⠀⠀⠀⠉⠉⠛⢻⣿⣿⣿⣗⡿⣿⡵⣷⢏⣤⢕⢭⣲⣻⣾⣿⢽⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣟⣿⣿⣕⣾⡯⣯⣾⣿⣾⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⠿⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠉⠛⠻⣿⣿⣷⡀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠒⠛⠟⠻⠛⠋⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠙⢿⣷⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠏⠀⠀⠀⠙⢿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠙⠄⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡿⠋⠀⠀⠀⠀⠀⠘⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
    )
    sun_logo = Text(
        logo_art,
        style="bold yellow",
        justify="center",
    )
    details = Group(
        Text("F O L D E R L E N S", style="bold yellow"),
        Text("Project Structure Analyzer", style="cyan"),
        Text("by Kikysena", style="magenta"),
        Text("\nScan · inspect · explain project structure", style="dim"),
    )

    if console.width < 100:
        banner_content = Group(sun_logo, details)
    else:
        layout = Table.grid(expand=True, padding=(0, 2))
        layout.add_column(width=42, justify="center")
        layout.add_column(ratio=1)
        layout.add_row(sun_logo, details)
        banner_content = layout

    console.print(
        Panel(
            banner_content,
            title=f"FolderLens v{version}",
            border_style="yellow",
            padding=(1, 2),
        )
    )


def show_menu() -> str:
    """Display the available actions and return the user's choice."""
    menu = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    menu.add_column("Option", style="bold cyan", no_wrap=True)
    menu.add_column("Action")
    menu.add_row("1", "Analisis folder")
    menu.add_row("2", "Bantuan")
    menu.add_row("3", "Versi")
    menu.add_row("0", "Keluar")
    console.print(Panel(menu, title="Menu", border_style="cyan"))
    return Prompt.ask("[bold cyan]Pilih menu[/]", choices=["1", "2", "3", "0"], default="1")


def show_help() -> None:
    """Display short usage instructions."""
    console.print(
        Panel(
            "Pilih [bold]1[/bold] lalu masukkan path folder untuk menganalisis project.\n"
            "Path kosong berarti folder saat ini.\n\n"
            "Contoh command langsung: [cyan]folderlens .[/cyan] atau [cyan]folderlens \"B:\\ProjectSaya\"[/cyan]\n"
            "Opsi lainnya: [cyan]folderlens --help[/cyan] dan [cyan]folderlens -v[/cyan]",
            title="Bantuan FolderLens",
            border_style="blue",
        )
    )


def _add_tree_children(parent: Tree, node: dict) -> None:
    """Add each analyzed child to a Rich tree."""
    for child in node["children"]:
        is_directory = child["type"] == "directory"
        icon = "📁" if is_directory else "📄"
        suffix = "/" if is_directory else ""
        label = Text(
            f"{icon} {child['name']}{suffix}",
            style="bold cyan" if is_directory else "white",
        )
        branch = parent.add(label)
        if is_directory:
            _add_tree_children(branch, child)


def show_analysis(analysis: dict) -> None:
    """Render the tree and summary using Rich components."""
    root = analysis["tree"]
    tree = Tree(Text(f"📁 {root['name']}/", style="bold yellow"), guide_style="dim")
    _add_tree_children(tree, root)
    console.print(Panel(tree, title="[bold]Project Structure[/bold]", border_style="yellow"))

    summary = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    summary.add_column("Label", style="bold cyan", no_wrap=True)
    summary.add_column("Value")
    summary.add_row("Type", analysis["project_type"])
    summary.add_row("Folders", str(analysis["folder_count"]))
    summary.add_row("Files", str(analysis["file_count"]))
    summary.add_row("Components", ", ".join(analysis["components"]) or "Tidak terdeteksi")
    summary.add_row("Technologies", ", ".join(analysis["technologies"]) or "Tidak terdeteksi")
    console.print(Panel(summary, title="[bold]Project Summary[/bold]", border_style="green"))
    console.print(
        Panel(
            Text(analysis["explanation"]),
            title="[bold]Structure Explanation[/bold]",
            border_style="blue",
        )
    )