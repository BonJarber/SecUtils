#!/usr/bin/env python3
import os
from pathlib import Path
import fnmatch
import argparse


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


def should_ignore(path, ignore_patterns, additional_skip_patterns=None):
    """Check if path matches any gitignore pattern or additional skip patterns."""
    # First check if path is in an excluded directory
    if is_in_excluded_dir(path):
        return True

    # Convert to string and get relative path for matching
    path_str = str(path)
    relative_path_str = str(Path(path_str).relative_to(Path(path_str).parent.parent))
    filename = os.path.basename(path_str)

    # First check gitignore patterns
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith("/"):
            if fnmatch.fnmatch(path_str + "/", "*/" + pattern):
                return True
        # Handle patterns with path separators
        elif "/" in pattern:
            if fnmatch.fnmatch(path_str, pattern):
                return True
        # Handle simple file patterns (match in any directory)
        else:
            if fnmatch.fnmatch(filename, pattern):
                return True

    # Then check additional skip patterns if any exist
    if additional_skip_patterns:
        for pattern in additional_skip_patterns:
            # Handle directory patterns (ending with /)
            if pattern.endswith("/"):
                if fnmatch.fnmatch(relative_path_str, pattern + "*"):
                    return True
            # For patterns with path separators, match against the full relative path
            elif "/" in pattern:
                if fnmatch.fnmatch(relative_path_str, pattern):
                    return True
            # For simple patterns, match against filename only
            else:
                if fnmatch.fnmatch(filename, pattern):
                    return True

    return False


def concatenate_files(start_dir, output_file, additional_skip=None):
    """Concatenate all files with their paths, respecting .gitignore and additional skip patterns."""
    start_path = Path(start_dir).resolve()
    gitignore_path = start_path / ".gitignore"
    ignore_patterns = parse_gitignore(gitignore_path)

    if additional_skip:
        print(f"Using additional skip patterns: {additional_skip}")

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
                d
                for d in dirs
                if not should_ignore(Path(root) / d, ignore_patterns, additional_skip)
            ]

            for file in sorted(files):  # Sort files for consistent output
                file_path = Path(root) / file

                # Skip .gitignore itself and ignored files
                if file == ".gitignore" or should_ignore(
                    file_path, ignore_patterns, additional_skip
                ):
                    continue

                # Get relative path from start directory
                relative_path = file_path.relative_to(start_path)
                print(f"Including file: {relative_path}")

                try:
                    with open(file_path, "r") as infile:
                        # Write a clear file header with separators
                        outfile.write("\n")  # Extra space before header
                        outfile.write("=" * 80 + "\n")  # Top separator
                        outfile.write(f"File: {relative_path}\n")  # Filename
                        outfile.write("=" * 80 + "\n")  # Bottom separator
                        outfile.write("\n")  # Space after header
                        outfile.write(infile.read())
                        outfile.write("\n\n")  # Extra space after content
                except (UnicodeDecodeError, IOError) as e:
                    print(f"Warning: Could not read {file_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate code files while respecting .gitignore"
    )
    parser.add_argument("directory", help="Source directory to process")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument(
        "--skip", "-s", help="Additional patterns to skip (comma-separated)", default=""
    )

    args = parser.parse_args()

    # Convert skip patterns string to list, handling empty string case
    additional_skip = [p.strip() for p in args.skip.split(",")] if args.skip else None

    concatenate_files(args.directory, args.output_file, additional_skip)
    print(f"Files have been concatenated into {args.output_file}")
