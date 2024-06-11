#!/usr/bin/env python3

import os
import fnmatch
import argparse
from typing import List, Optional
import argcomplete  # Importiere argcomplete

def read_gitignore(path: str) -> List[str]:
    """
    Reads the .gitignore file from the specified path and returns a list of ignored patterns.
    
    Args:
        path (str): The directory containing the .gitignore file.

    Returns:
        List[str]: A list of patterns to ignore.
    """
    gitignore_path = os.path.join(path, '.gitignore')
    if not os.path.isfile(gitignore_path):
        return []
    try:
        with open(gitignore_path, 'r') as file:
            lines = file.readlines()
    except (IOError, OSError) as e:
        print(f"Error reading .gitignore file: {e}")
        return []
    ignored_patterns = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return ignored_patterns

def is_ignored(file_path: str, ignored_patterns: List[str], root_dir: str) -> bool:
    """
    Checks if a given file path should be ignored based on the patterns in .gitignore.
    
    Args:
        file_path (str): The file path to check.
        ignored_patterns (List[str]): The list of patterns from .gitignore.
        root_dir (str): The root directory of the project.

    Returns:
        bool: True if the file should be ignored, False otherwise.
    """
    relative_path = os.path.relpath(file_path, root_dir)
    for pattern in ignored_patterns:
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(relative_path + '/', pattern):
            return True
        parts = relative_path.split(os.sep)
        for i in range(1, len(parts) + 1):
            partial_path = os.path.join(*parts[:i])
            if fnmatch.fnmatch(partial_path, pattern) or fnmatch.fnmatch(partial_path + '/', pattern):
                return True
    return False

def should_process_file(file: str, whitelist: Optional[List[str]], blacklist: Optional[List[str]]) -> bool:
    """
    Checks if a file should be processed based on its extension and the provided whitelist or blacklist.
    
    Args:
        file (str): The file name.
        whitelist (Optional[List[str]]): A list of file extensions and names to whitelist.
        blacklist (Optional[List[str]]): A list of file extensions and names to blacklist.

    Returns:
        bool: True if the file should be processed, False otherwise.
    """
    file_name = os.path.basename(file)
    file_extension = os.path.splitext(file)[1][1:]  # Get the file extension without the dot

    # Whitelist check
    if whitelist:
        if file_name not in whitelist and file_extension not in whitelist:
            return False

    # Blacklist check
    if blacklist:
        if file_name in blacklist or file_extension in blacklist:
            return False

    return True

def read_file_content(file_path: str) -> str:
    """
    Tries to read the content of a file with different encodings.
    
    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            return infile.read()
    except UnicodeDecodeError:
        print(f"Warning: UTF-8 decoding failed for {file_path}. Trying ISO-8859-1.")
        try:
            with open(file_path, 'r', encoding='iso-8859-1') as infile:
                return infile.read()
        except UnicodeDecodeError as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

def concat_files_in_directory(root_dir: str, output_file: Optional[str] = None, list_files: bool = False, dryrun: bool = False, whitelist: Optional[List[str]] = None, blacklist: Optional[List[str]] = None) -> None:
    """
    Concatenates the content of specified files in a directory, ignoring files specified in .gitignore and filtering by whitelist and blacklist.
    
    Args:
        root_dir (str): The root directory of the project.
        output_file (Optional[str]): The output file to write the concatenated content to. If None, prints to stdout.
        list_files (bool): If True, lists the files that were read.
        dryrun (bool): If True, shows which files would be read without actually reading or writing.
        whitelist (Optional[List[str]]): A list of file extensions and names to whitelist.
        blacklist (Optional[List[str]]): A list of file extensions and names to blacklist.
    """
    ignored_patterns = read_gitignore(root_dir)
    file_contents = []
    read_files = []

    for subdir, _, files in os.walk(root_dir):
        if is_ignored(subdir, ignored_patterns, root_dir):
            continue
        for file in files:
            file_path = os.path.join(subdir, file)
            if should_process_file(file_path, whitelist, blacklist):
                if not is_ignored(file_path, ignored_patterns, root_dir):
                    relative_file_path = os.path.relpath(file_path, root_dir)
                    read_files.append(relative_file_path)
                    if not dryrun:
                        content = read_file_content(file_path)
                        if content:
                            file_contents.append(f"{relative_file_path}:\n\n{content}\n\n")

    if not dryrun:
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.writelines(file_contents)
            except (IOError, OSError) as e:
                print(f"Error writing to output file {output_file}: {e}")
        else:
            for content in file_contents:
                print(content)
    
    if list_files or dryrun:
        print("Files to be read:" if dryrun else "Files read:")
        for file in read_files:
            print(file)

def main() -> None:
    """
    Main function to parse arguments and execute the file concatenation.
    """
    parser = argparse.ArgumentParser(description="CLI tool to concatenate specified files in a directory.")
    parser.add_argument('root_dir', nargs='?', default=os.getcwd(), type=str, help='The root directory of the project. Defaults to the current directory.')
    parser.add_argument('--out', type=str, help='Output file. If omitted, output will be printed to stdout.')
    parser.add_argument('--list-files', action='store_true', help='List the files that were read.')
    parser.add_argument('--dryrun', action='store_true', help='Show which files would be read without actually reading or writing.')
    parser.add_argument('--white', type=str, help='Comma-separated list of file extensions and names to whitelist.')
    parser.add_argument('--black', type=str, help='Comma-separated list of file extensions and names to blacklist.')

    argcomplete.autocomplete(parser)  # Hinzufügen der Autocomplete-Unterstützung
    args = parser.parse_args()

    whitelist = args.white.split(',') if args.white else None
    blacklist = args.black.split(',') if args.black else None

    try:
        concat_files_in_directory(args.root_dir, args.out, args.list_files, args.dryrun, whitelist, blacklist)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
