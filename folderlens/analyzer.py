"""Analyze folder and file names without opening file contents."""

from collections import Counter
from pathlib import Path


# Directory names are compared without case sensitivity for Windows compatibility.
IGNORED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    ".dart_tool",
    ".idea",
    ".vscode",
}

EXTENSION_TECHNOLOGIES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".dart": "Dart",
    ".java": "Java",
    ".php": "PHP",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".sql": "SQL",
}


def _is_ignored_directory(name: str, excluded_dirs: set[str] | None = None) -> bool:
    """Return whether a directory should be skipped during analysis."""
    normalized_name = name.casefold()
    return (
        normalized_name in IGNORED_DIRS
        or normalized_name.endswith(".egg-info")
        or normalized_name in (excluded_dirs or set())
    )


def list_project_directories(project_path: Path) -> list[str]:
    """List selectable project directories as paths relative to the project root."""
    project_path = project_path.resolve()
    directories: list[str] = []
    pending = [project_path]

    while pending:
        current_path = pending.pop()
        try:
            entries = sorted(
                current_path.iterdir(), key=lambda item: item.name.casefold()
            )
        except (PermissionError, OSError):
            continue

        for entry in entries:
            try:
                if entry.is_symlink() or not entry.is_dir():
                    continue
            except (PermissionError, OSError):
                continue

            if _is_ignored_directory(entry.name):
                continue

            directories.append(entry.relative_to(project_path).as_posix())
            pending.append(entry)

    return sorted(directories, key=str.casefold)


def _validate_include_dirs(
    project_path: Path, include_dirs: list[str], excluded_dirs: set[str]
) -> list[tuple[str, ...]]:
    """Validate selected relative directories and return their path components."""
    root = project_path.resolve()
    selected: list[tuple[str, ...]] = []

    for directory in include_dirs:
        relative_path = Path(directory)
        if (
            not directory.strip()
            or relative_path.is_absolute()
            or relative_path.drive
            or ".." in relative_path.parts
            or not relative_path.parts
        ):
            raise ValueError(f"Path folder harus relatif di dalam project: {directory}")

        candidate = root / relative_path
        current = root
        for part in relative_path.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError(f"Folder symlink tidak dapat dipilih: {directory}")
            if _is_ignored_directory(part, excluded_dirs):
                raise ValueError(f"Folder ini dikecualikan dari scan: {directory}")

        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            raise ValueError(f"Folder tidak ditemukan di dalam project: {directory}") from None

        if not resolved.is_dir():
            raise ValueError(f"Path yang dipilih bukan folder: {directory}")

        selected.append(resolved.relative_to(root).parts)

    return selected


def _is_path_prefix(prefix: tuple[str, ...], path: tuple[str, ...]) -> bool:
    """Return whether prefix is equal to or an ancestor of path."""
    return len(prefix) <= len(path) and all(
        left.casefold() == right.casefold()
        for left, right in zip(prefix, path)
    )


def _infer_project_type(technologies: list[str], names: set[str]) -> str:
    """Guess a broad project type from the names found in the project."""
    if "pubspec.yaml" in names or "Flutter" in technologies:
        return "Flutter Project"
    if "Python" in technologies:
        return "Python Project"
    if "TypeScript" in technologies:
        return "TypeScript Project"
    if "JavaScript" in technologies or "package.json" in names:
        return "JavaScript Project"
    if "Java" in technologies:
        return "Java Project"
    if "PHP" in technologies:
        return "PHP Project"
    if "Dart" in technologies:
        return "Dart Project"
    if "HTML" in technologies or "CSS" in technologies:
        return "Web Project"
    return "General Project"


def _detect_components(
    names: set[str], directory_names: set[str], extensions: Counter[str]
) -> list[str]:
    """Return short descriptions of recognizable project components."""
    components: list[str] = []

    if any(
        extension in extensions
        for extension in (".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".dart", ".java", ".php")
    ):
        components.append("Source code")
    if directory_names.intersection({"test", "tests"}):
        components.append("Test directory")
    if names.intersection(
        {
            "requirements.txt", "pyproject.toml", "package.json", "package-lock.json",
            "yarn.lock", "pnpm-lock.yaml", "pubspec.yaml", "composer.json",
            "pom.xml", "build.gradle", "go.mod",
        }
    ):
        components.append("Dependency/build configuration")
    if "readme.md" in names or ".md" in extensions:
        components.append("Documentation")
    if ".git" in names or ".gitignore" in names:
        components.append("Git configuration")
    if "dockerfile" in names or "docker-compose.yml" in names or "compose.yaml" in names:
        components.append("Docker configuration")
    if directory_names.intersection({"assets", "public"}):
        components.append("Static assets")
    if "config" in directory_names or "config" in names:
        components.append("Configuration directory/files")

    return components


def _explain_structure(
    directory_names: set[str], names: set[str], project_type: str
) -> str:
    """Build a beginner-friendly explanation using only detected names."""
    sentences = [f"Project ini terlihat seperti {project_type.lower()}."]

    if "src" in directory_names:
        sentences.append("Folder `src` kemungkinan berisi source code utama.")
    if "lib" in directory_names:
        sentences.append("Folder `lib` biasanya menyimpan library atau kode yang dapat digunakan ulang.")
    if directory_names.intersection({"tests", "test"}):
        sentences.append("Folder `tests` atau `test` digunakan untuk menyimpan pengujian.")
    if directory_names.intersection({"components", "pages", "app"}):
        found = ", ".join(
            f"`{name}`" for name in ("app", "components", "pages") if name in directory_names
        )
        sentences.append(f"Folder {found} kemungkinan berisi bagian-bagian aplikasi.")
    if "requirements.txt" in names or "pyproject.toml" in names:
        sentences.append("File konfigurasi Python tersebut biasanya mencatat dependency project.")
    if "package.json" in names:
        sentences.append("`package.json` biasanya mencatat informasi dan dependency project JavaScript.")
    if "readme.md" in names or "readme" in names:
        sentences.append("File README kemungkinan berisi dokumentasi project.")
    if "docs" in directory_names:
        sentences.append("Folder `docs` kemungkinan berisi dokumentasi tambahan.")
    if len(sentences) == 1:
        sentences.append("Ringkasan ini dibuat dari nama file, ekstensi, dan folder yang ditemukan.")

    return "\n".join(sentences)


def analyze_project(
    project_path: Path,
    include_dirs: list[str] | None = None,
    excluded_dirs: list[str] | None = None,
    max_depth: int | None = None,
) -> dict:
    """Build a tree and project summary without reading any file contents."""
    project_path = project_path.resolve()
    if max_depth is not None and max_depth < 0:
        raise ValueError("Kedalaman maksimum tidak boleh negatif.")
    normalized_excluded_dirs = {
        directory.casefold() for directory in (excluded_dirs or [])
    }
    selected_dirs = (
        _validate_include_dirs(project_path, include_dirs, normalized_excluded_dirs)
        if include_dirs
        else None
    )
    root = {
        "name": project_path.name or str(project_path),
        "type": "directory",
        "children": [],
    }
    directory_names: set[str] = set()
    names: set[str] = set()
    extensions: Counter[str] = Counter()
    directory_count = 0
    file_count = 0

    # A stack avoids recursion depth issues. Symlinks are skipped to prevent loops.
    pending = [(project_path, root)]
    while pending:
        current_path, current_node = pending.pop()
        current_relative = current_path.relative_to(project_path).parts
        try:
            entries = list(current_path.iterdir())
        except (PermissionError, OSError):
            continue

        directories = []
        files = []
        for entry in entries:
            try:
                if entry.is_symlink():
                    continue
                is_directory = entry.is_dir()
            except (PermissionError, OSError):
                continue

            if is_directory:
                if (
                    selected_dirs is None
                    and entry.name.casefold() not in normalized_excluded_dirs
                ):
                    names.add(entry.name)
                    directory_names.add(entry.name.casefold())
                if _is_ignored_directory(entry.name, normalized_excluded_dirs):
                    continue

                entry_relative = current_relative + (entry.name,)
                if selected_dirs and not any(
                    _is_path_prefix(entry_relative, selected)
                    or _is_path_prefix(selected, entry_relative)
                    for selected in selected_dirs
                ):
                    continue

                names.add(entry.name)
                directory_names.add(entry.name.casefold())
                if max_depth is None or len(current_relative) < max_depth:
                    directories.append(entry)
            else:
                if selected_dirs and not any(
                    _is_path_prefix(selected, current_relative)
                    for selected in selected_dirs
                ):
                    continue

                names.add(entry.name)
                files.append(entry)
                extensions[entry.suffix.casefold()] += 1

        # Directories appear before files, with each group sorted alphabetically.
        for entry in sorted(directories, key=lambda item: item.name.casefold()):
            child = {"name": entry.name, "type": "directory", "children": []}
            current_node["children"].append(child)
            directory_count += 1
            pending.append((entry, child))

        for entry in sorted(files, key=lambda item: item.name.casefold()):
            current_node["children"].append(
                {"name": entry.name, "type": "file", "children": []}
            )
            file_count += 1

    # Names are kept with their original spelling; normalize them for detection.
    normalized_names = {name.casefold() for name in names}
    normalized_directories = directory_names
    technologies = []
    for technology in EXTENSION_TECHNOLOGIES.values():
        if technology not in technologies and any(
            EXTENSION_TECHNOLOGIES.get(extension) == technology for extension in extensions
        ):
            technologies.append(technology)

    if ".git" in normalized_names or ".gitignore" in normalized_names:
        technologies.append("Git")
    if "dockerfile" in normalized_names or "docker-compose.yml" in normalized_names or "compose.yaml" in normalized_names:
        technologies.append("Docker")
    if "pubspec.yaml" in normalized_names:
        technologies.append("Flutter")

    # Keep filename checks case-insensitive while retaining readable names above.
    project_type = _infer_project_type(technologies, normalized_names)
    components = _detect_components(normalized_names, normalized_directories, extensions)

    return {
        "tree": root,
        "folder_count": directory_count,
        "file_count": file_count,
        "technologies": technologies,
        "project_type": project_type,
        "components": components,
        "explanation": _explain_structure(
            normalized_directories, normalized_names, project_type
        ),
    }
