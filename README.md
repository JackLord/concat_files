
# Concat Files Tool

## Overview

`concat_file` is a CLI tool to concatenate the content of specified files in a directory. The tool supports filtering files using whitelist and blacklist options and respects `.gitignore` files.

## Installation

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. Install the package and dependencies:

   ```bash
   pip install .
   ```

3. Run the setup script based on your operating system:

   - **Linux**:

     ```bash
     bash scripts/setup_linux.sh
     ```

   - **macOS**:

     ```bash
     bash scripts/setup_mac.sh
     ```

   - **Windows**:

     ```cmd
     scripts\setup_windows.bat
     ```

## Usage

```bash
concat_file.py [OPTIONS] [root_dir]
```

### Options

- `--out OUT`: Output file. If omitted, output will be printed to stdout.
- `--list-files`: List the files that were read.
- `--dryrun`: Show which files would be read without actually reading or writing.
- `--white WHITE`: Comma-separated list of file extensions and names to whitelist.
- `--black BLACK`: Comma-separated list of file extensions and names to blacklist.

### Example

To concatenate all Python, JSON, and Markdown files in the current directory, excluding `README.md`, and write the output to `all.txt`:

```bash
concat_file.py --list-files --out all.txt --white py,json,md --black README.md
```

### Notes

- If both `--white` and `--black` are provided, the tool will first apply the whitelist and then apply the blacklist to filter out specific files.
- The tool respects `.gitignore` files and will ignore files and directories listed there.

## Development

### Adding New Features

1. Fork the repository.
2. Create a new branch for your feature.
3. Implement your feature and write tests.
4. Open a pull request to the main repository.

### Running Tests

To run the tests, use the following command:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
