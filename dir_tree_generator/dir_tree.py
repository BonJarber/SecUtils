#!/usr/bin/env python3
import os
import argparse
from typing import List, Set
from pathlib import Path


class DirectoryTreeGenerator:
    def __init__(
        self,
        root_dir: str,
        ignore_dirs: Set[str] = None,
        ignore_patterns: Set[str] = None,
        max_depth: int = None,
    ):
        self.root_dir = Path(root_dir)
        self.ignore_dirs = ignore_dirs or set()
        self.ignore_patterns = ignore_patterns or set()
        self.max_depth = max_depth
        self.tree_str = ""

    def should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored based on configured patterns."""
        # Check if directory name is in ignore list
        if path.name in self.ignore_dirs:
            return True

        # Check if path matches any ignore pattern
        for pattern in self.ignore_patterns:
            if pattern in str(path):
                return True

        return False

    def generate_tree(
        self, directory: Path = None, prefix: str = "", depth: int = 0
    ) -> str:
        """Generate a tree representation of the directory structure."""
        if directory is None:
            directory = self.root_dir
            self.tree_str = str(directory) + "/\n"

        if self.max_depth is not None and depth >= self.max_depth:
            return

        # Get and sort directory contents
        try:
            entries = sorted(
                directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())
            )
        except PermissionError:
            return

        # Process each entry
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1

            if self.should_ignore(entry):
                continue

            # Create the proper prefix for this item
            current_prefix = "└── " if is_last else "├── "
            next_prefix = "    " if is_last else "│   "

            # Add the entry to the tree
            self.tree_str += f"{prefix}{current_prefix}{entry.name}"
            if entry.is_dir():
                self.tree_str += "/\n"
                self.generate_tree(entry, prefix + next_prefix, depth + 1)
            else:
                self.tree_str += "\n"

        return self.tree_str


DEFAULT_IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".venv",
    "venv",
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate a directory tree visualization"
    )
    parser.add_argument("root_dir", help="Root directory to start from")
    parser.add_argument(
        "--ignore-dirs",
        nargs="*",
        default=[],
        help="Additional directories to ignore (adds to defaults)",
    )
    parser.add_argument(
        "--no-defaults", action="store_true", help="Don't use default ignore list"
    )
    parser.add_argument(
        "--show-defaults",
        action="store_true",
        help="Show default ignored directories and exit",
    )
    parser.add_argument(
        "--ignore-patterns",
        nargs="*",
        default=[],
        help="Patterns to ignore (any path containing these strings will be ignored)",
    )
    parser.add_argument("--max-depth", type=int, help="Maximum depth to traverse")
    parser.add_argument(
        "--output", help="Output file (if not specified, prints to stdout)"
    )

    args = parser.parse_args()

    if args.show_defaults:
        print("Default ignored directories:", ", ".join(sorted(DEFAULT_IGNORE_DIRS)))
        return

    # Combine default and user-specified ignore dirs unless --no-defaults is used
    ignore_dirs = set(args.ignore_dirs)
    if not args.no_defaults:
        ignore_dirs.update(DEFAULT_IGNORE_DIRS)

    tree_gen = DirectoryTreeGenerator(
        args.root_dir,
        ignore_dirs=ignore_dirs,
        ignore_patterns=set(args.ignore_patterns),
        max_depth=args.max_depth,
    )

    tree = tree_gen.generate_tree()

    if args.output:
        with open(args.output, "w") as f:
            f.write(tree)
    else:
        print(tree)


if __name__ == "__main__":
    main()
