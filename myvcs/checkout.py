"""Checkout command implementation for myvcs."""

import os
from myvcs import utils, storage, repo, commit


def checkout_commit(commit_id):
    """
    Restore working directory to state at specified commit.
    Returns (success, error_message).
    """
    if not repo.is_repo_initialized():
        return False, "Not a myvcs repository"
    
    if not commit.commit_exists(commit_id):
        return False, f"Commit {commit_id} does not exist"
    
    # Load commit data
    commit_data = commit.load_commit(commit_id)
    if not commit_data:
        return False, f"Failed to load commit {commit_id}"
    
    commit_files = commit_data["files"]
    
    # Get current files in working directory
    current_files = set(utils.get_all_files())
    commit_file_set = set(commit_files.keys())
    
    # Restore all files from commit
    permission_errors = []
    for filepath, file_hash in commit_files.items():
        try:
            content = storage.retrieve_object(file_hash)
            utils.write_file_binary(filepath, content)
        except PermissionError:
            # Skip files with permission errors (e.g., .git objects)
            permission_errors.append(filepath)
        except Exception as e:
            return False, f"Error restoring file {filepath}: {e}"
    
    # Remove files that don't exist in commit
    files_to_remove = current_files - commit_file_set
    for filepath in files_to_remove:
        try:
            utils.remove_file(filepath)
            # Remove empty directories
            _remove_empty_dirs(os.path.dirname(filepath))
        except Exception:
            # Continue even if removal fails
            pass
    
    # Update HEAD
    repo.set_head(commit_id)
    
    # Update index
    repo.write_index(commit_files)
    
    message = f"Checked out commit {commit_id}"
    if permission_errors:
        message += f" (skipped {len(permission_errors)} files due to permissions)"
    
    return True, message


def _remove_empty_dirs(dirpath):
    """Remove empty directories recursively."""
    if not dirpath or dirpath == ".":
        return
    
    try:
        # Don't remove if it's the myvcs directory or contains it
        if utils.MYVCS_DIR in dirpath.split(os.sep):
            return
        
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
                # Recursively try to remove parent
                _remove_empty_dirs(os.path.dirname(dirpath))
    except Exception:
        pass
