#!/usr/bin/env python3
import os
from pathlib import Path
import fnmatch


def parse_gitignore(gitignore_path):
    """Parse .gitignore file and return list of patterns."""
    # Default patterns to always ignore
    patterns = [
        ".git",  # Match .git directory and all contents
        ".venv",  # Match .venv directory and all contents
    ]

    if not os.path.exists(gitignore_path):
        print(f"No .gitignore found at {gitignore_path}")
        return patterns

    print(f"Reading .gitignore from {gitignore_path}")
    with open(gitignore_path, "r") as f:
        # Remove empty lines and comments, add to default patterns
        gitignore_patterns = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]
        patterns.extend(gitignore_patterns)
        print(f"Added patterns from .gitignore: {gitignore_patterns}")

    return patterns


def is_in_excluded_dir(path, excluded_dirs=None):
    """Check if path is within any excluded directory."""
    if excluded_dirs is None:
        excluded_dirs = {".git", ".venv"}

    # Convert path to parts for checking
    parts = Path(path).parts

    # Check if any part of the path starts with an excluded directory name
    return any(part in excluded_dirs for part in parts)


def should_ignore(path, ignore_patterns):
    """Check if path matches any gitignore pattern."""
    # First check if path is in an excluded directory
    if is_in_excluded_dir(path):
        return True

    # Convert to string for pattern matching
    path_str = str(path)

    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith("/"):
            if fnmatch.fnmatch(path_str + "/", pattern):
                return True
        # Handle file patterns
        elif fnmatch.fnmatch(path_str, pattern):
            return True
    return False


def concatenate_files(start_dir, output_file):
    """Concatenate all files with their paths, respecting .gitignore."""
    start_path = Path(start_dir).resolve()
    gitignore_path = start_path / ".gitignore"
    ignore_patterns = parse_gitignore(gitignore_path)
    print(f"Using ignore patterns: {ignore_patterns}")

    excluded_dirs = {".git", ".venv"}  # Set of directories to completely exclude

    with open(output_file, "w") as outfile:
        for root, dirs, files in os.walk(start_path):
            # Skip this directory entirely if it's in an excluded path
            if is_in_excluded_dir(root):
                dirs.clear()  # Clear dirs list to prevent descending
                continue

            # Remove excluded directories from dirs list
            dirs[:] = [
                d for d in dirs if not should_ignore(Path(root) / d, ignore_patterns)
            ]

            for file in sorted(files):  # Sort files for consistent output
                file_path = Path(root) / file

                # Skip .gitignore itself and ignored files
                if file == ".gitignore" or should_ignore(file_path, ignore_patterns):
                    continue

                # Get relative path from start directory
                relative_path = file_path.relative_to(start_path)
                print(f"Including file: {relative_path}")

                try:
                    with open(file_path, "r") as infile:
                        outfile.write(f"{relative_path}\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")
                except (UnicodeDecodeError, IOError) as e:
                    print(f"Warning: Could not read {file_path}: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <output_file>")
        sys.exit(1)

    directory = sys.argv[1]
    output_file = sys.argv[2]

    concatenate_files(directory, output_file)
    print(f"Files have been concatenated into {output_file}")
