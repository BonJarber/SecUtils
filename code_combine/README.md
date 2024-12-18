# Code Combine

A Python utility for combining multiple code files into a single file while preserving syntax highlighting and file structure.

## Description

Code Combine is a simple tool that helps you merge multiple source code files into a single, well-formatted output file. It's particularly useful for:
- Sharing source code with an LLM
- Creating documentation that includes code from multiple files
- Preparing code submissions that require a single file

## Features

- Maintains original file paths as headers
- Ignores files in .gitignore
- Creates clean, readable output

## Usage

To use Code Combine, simply run the script with the path to your source directory and the output file name. The script will process all files in the directory and its subdirectories, excluding any files that match patterns in .gitignore.

```bash
python combine.py <source_dir> <output_file>
```

This will create a new file named `output_file` containing the combined code from all files in the source directory (excluding any files that match patterns in .gitignore).

## Requirements

- Python 3.6 or higher

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests to improve this tool.