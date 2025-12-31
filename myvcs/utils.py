"""Filesystem utilities for myvcs."""

import os


MYVCS_DIR = ".myvcs"


def get_all_files(root_dir="."):
    """
    Walk through directory tree and return all tracked files.
    Ignores .myvcs/ directory and its contents.
    """
    all_files = []
    root_dir = os.path.abspath(root_dir)
    myvcs_path = os.path.join(root_dir, MYVCS_DIR)
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .myvcs directory
        if os.path.abspath(dirpath).startswith(myvcs_path):
            continue
        
        # Remove .myvcs from dirnames to prevent walking into it
        if MYVCS_DIR in dirnames:
            dirnames.remove(MYVCS_DIR)
        
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Convert to relative path
            rel_path = os.path.relpath(filepath, root_dir)
            all_files.append(rel_path)
    
    return sorted(all_files)


def read_file_binary(filepath):
    """Read file contents in binary mode."""
    with open(filepath, "rb") as f:
        return f.read()


def write_file_binary(filepath, content):
    """Write file contents in binary mode."""
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(content)


def read_file_text(filepath):
    """Read file contents in text mode."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_file_text(filepath, content):
    """Write file contents in text mode."""
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def file_exists(filepath):
    """Check if file exists."""
    return os.path.exists(filepath)


def remove_file(filepath):
    """Remove a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)


def ensure_dir(dirpath):
    """Ensure directory exists."""
    os.makedirs(dirpath, exist_ok=True)
