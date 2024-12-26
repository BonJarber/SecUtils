# Codebase Combiner

A Python script that combines all files from a code repository into a single file, making it easier to share codebases with Large Language Models (LLMs). The script respects `.gitignore` patterns and allows for additional file/directory exclusions.

## Features

- Combines all text files from a directory into a single file
- Respects existing `.gitignore` patterns
- Allows additional patterns to be skipped via command line
- Adds clear file headers and separators for better readability
- Handles both simple patterns and path-based patterns for exclusion
- Automatically skips binary and non-UTF-8 files
- Sorts files alphabetically for consistent output

## Installation

No installation required beyond Python 3. Simply download the script and make it executable:

```bash
chmod +x combine.py
```

## Usage

Basic usage:
```bash
python3 combine.py <source_directory> <output_file>
```

With additional skip patterns:
```bash
python3 combine.py <source_directory> <output_file> --skip "pattern1,pattern2"
```

### Examples

Combine all files from a project, excluding common build artifacts:
```bash
python3 combine.py ~/Code/my-project output.txt --skip "poetry.lock,package-lock.json"
```

Skip specific directories and files:
```bash
python3 combine.py ~/Code/my-project output.txt --skip "tests/,docs/,specific/file.py"
```

### Skip Patterns

The `--skip` (or `-s`) flag accepts a comma-separated list of patterns. These patterns can be:

- Simple filenames: `"poetry.lock"`
- Directory names (with trailing slash): `"tests/"`
- Path-based patterns: `"src/components/test.js"`

## Output Format

The script generates a single file with clear separators between files:

```
================================================================================
File: src/main.py
================================================================================

[file contents here]


================================================================================
File: src/utils.py
================================================================================

[file contents here]
```

## Default Exclusions

The script automatically excludes:
- All patterns from your project's `.gitignore`
- The `.git` directory
- The `.venv` directory
- Binary files and files that can't be decoded as UTF-8

## Error Handling

- Files that can't be read as UTF-8 text are skipped with a warning
- Missing `.gitignore` file is handled gracefully
- Invalid command-line arguments show a help message