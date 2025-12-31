"""Commit creation and management for myvcs."""

import os
import time
from myvcs import utils, storage, repo


def create_commit(message):
    """
    Create a new commit with the current working directory state.
    Returns (success, commit_id_or_error_message).
    """
    if not repo.is_repo_initialized():
        return False, "Not a myvcs repository"
    
    if not message:
        return False, "Commit message is required"
    
    # Get all files in working directory
    all_files = utils.get_all_files()
    
    # Hash and store all file contents
    file_hashes = {}
    for filepath in all_files:
        try:
            content = utils.read_file_binary(filepath)
            file_hash = storage.store_object(content)
            file_hashes[filepath] = file_hash
        except Exception as e:
            return False, f"Error reading file {filepath}: {e}"
    
    # Create commit metadata
    parent_commit = repo.get_head()
    timestamp = str(int(time.time()))
    
    # Generate deterministic commit ID
    commit_id = _generate_commit_id(parent_commit, timestamp, message, file_hashes)
    
    # Store commit metadata
    success, error = _store_commit_metadata(commit_id, parent_commit, timestamp, message, file_hashes)
    if not success:
        return False, error
    
    # Update HEAD
    repo.set_head(commit_id)
    
    # Update index
    repo.write_index(file_hashes)
    
    return True, commit_id


def _generate_commit_id(parent_commit, timestamp, message, file_hashes):
    """Generate deterministic commit ID based on content."""
    # Create a deterministic string from commit data
    commit_data = f"{parent_commit}\n{timestamp}\n{message}\n"
    
    # Add sorted file list
    for filepath in sorted(file_hashes.keys()):
        commit_data += f"{filepath} {file_hashes[filepath]}\n"
    
    return storage.compute_hash(commit_data)


def _store_commit_metadata(commit_id, parent_commit, timestamp, message, file_hashes):
    """Store commit metadata to commits directory."""
    commit_path = os.path.join(repo.COMMITS_DIR, commit_id)
    
    # Build metadata content
    lines = [
        f"commit {commit_id}",
        f"parent {parent_commit}",
        f"timestamp {timestamp}",
        f"message {message}",
        "files"
    ]
    
    for filepath in sorted(file_hashes.keys()):
        lines.append(f"{filepath} {file_hashes[filepath]}")
    
    metadata = "\n".join(lines)
    
    try:
        utils.write_file_text(commit_path, metadata)
        return True, None
    except Exception as e:
        return False, f"Error storing commit: {e}"


def load_commit(commit_id):
    """
    Load commit metadata.
    Returns dict with: commit_id, parent, timestamp, message, files (dict)
    """
    commit_path = os.path.join(repo.COMMITS_DIR, commit_id)
    
    if not utils.file_exists(commit_path):
        return None
    
    content = utils.read_file_text(commit_path)
    lines = content.split("\n")
    
    commit_data = {
        "commit_id": "",
        "parent": "",
        "timestamp": "",
        "message": "",
        "files": {}
    }
    
    in_files_section = False
    for line in lines:
        if line.startswith("commit "):
            commit_data["commit_id"] = line.split(" ", 1)[1]
        elif line.startswith("parent "):
            commit_data["parent"] = line.split(" ", 1)[1]
        elif line.startswith("timestamp "):
            commit_data["timestamp"] = line.split(" ", 1)[1]
        elif line.startswith("message "):
            commit_data["message"] = line.split(" ", 1)[1]
        elif line == "files":
            in_files_section = True
        elif in_files_section and line:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                filepath, file_hash = parts
                commit_data["files"][filepath] = file_hash
    
    return commit_data


def commit_exists(commit_id):
    """Check if commit exists."""
    commit_path = os.path.join(repo.COMMITS_DIR, commit_id)
    return utils.file_exists(commit_path)
