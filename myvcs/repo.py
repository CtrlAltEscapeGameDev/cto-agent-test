"""Repository initialization and management for myvcs."""

import os
from myvcs import utils, storage


HEAD_FILE = os.path.join(utils.MYVCS_DIR, "HEAD")
INDEX_FILE = os.path.join(utils.MYVCS_DIR, "index")
COMMITS_DIR = os.path.join(utils.MYVCS_DIR, "commits")


def init_repo():
    """
    Initialize a new myvcs repository.
    Creates .myvcs/ directory structure.
    """
    if utils.file_exists(utils.MYVCS_DIR):
        return False, "Repository already initialized"
    
    # Create directory structure
    utils.ensure_dir(utils.MYVCS_DIR)
    utils.ensure_dir(storage.OBJECTS_DIR)
    utils.ensure_dir(COMMITS_DIR)
    
    # Initialize HEAD (empty initially)
    utils.write_file_text(HEAD_FILE, "")
    
    # Initialize index (empty initially)
    utils.write_file_text(INDEX_FILE, "")
    
    return True, "Initialized empty myvcs repository"


def is_repo_initialized():
    """Check if current directory is a myvcs repository."""
    return utils.file_exists(utils.MYVCS_DIR) and os.path.isdir(utils.MYVCS_DIR)


def get_head():
    """
    Get current HEAD commit id.
    Returns empty string if no commits exist yet.
    """
    if not utils.file_exists(HEAD_FILE):
        return ""
    return utils.read_file_text(HEAD_FILE).strip()


def set_head(commit_id):
    """Set HEAD to specified commit id."""
    utils.write_file_text(HEAD_FILE, commit_id)


def read_index():
    """
    Read index file and return as dictionary.
    Format: filepath hash
    """
    if not utils.file_exists(INDEX_FILE):
        return {}
    
    index_content = utils.read_file_text(INDEX_FILE).strip()
    if not index_content:
        return {}
    
    index = {}
    for line in index_content.split("\n"):
        if line:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                filepath, file_hash = parts
                index[filepath] = file_hash
    
    return index


def write_index(file_dict):
    """
    Write index file from dictionary.
    Format: filepath hash
    """
    lines = []
    for filepath in sorted(file_dict.keys()):
        lines.append(f"{filepath} {file_dict[filepath]}")
    
    content = "\n".join(lines)
    utils.write_file_text(INDEX_FILE, content)
