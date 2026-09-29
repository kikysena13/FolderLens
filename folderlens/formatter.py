"""Format FolderLens analysis results for the terminal."""


def _format_tree(node: dict) -> list[str]:
    """Render the nested tree using readable Unicode branches."""
    lines = [f"📁 {node['name']}/"]

    def add_children(parent: dict, prefix: str) -> None:
        children = parent["children"]
        for index, child in enumerate(children):
            is_last = index == len(children) - 1
            branch = "└── " if is_last else "├── "
            icon = "📁" if child["type"] == "directory" else "📄"
            suffix = "/" if child["type"] == "directory" else ""
            lines.append(f"{prefix}{branch}{icon} {child['name']}{suffix}")
            if child["type"] == "directory":
                next_prefix = prefix + ("    " if is_last else "│   ")
                add_children(child, next_prefix)

    add_children(node, "")
    return lines


def format_report(analysis: dict) -> str:
    """Create the complete four-section report."""
    lines = ["[1] PROJECT STRUCTURE", ""]
    lines.extend(_format_tree(analysis["tree"]))

    lines.extend(["", "[2] PROJECT SUMMARY", ""])
    lines.append(f"Type: {analysis['project_type']}")
    lines.append(f"Folders: {analysis['folder_count']}")
    lines.append(f"Files: {analysis['file_count']}")
    lines.append("Detected components:")
    if analysis["components"]:
        lines.extend(f"- {component}" for component in analysis["components"])
    else:
        lines.append("- Belum ada komponen umum yang dikenali")

    lines.extend(["", "[3] DETECTED TECHNOLOGIES", ""])
    if analysis["technologies"]:
        lines.extend(f"- {technology}" for technology in analysis["technologies"])
    else:
        lines.append("- Belum ada teknologi yang dikenali")

    lines.extend(["", "[4] STRUCTURE EXPLANATION", ""])
    lines.append(analysis["explanation"])
    return "\n".join(lines)
