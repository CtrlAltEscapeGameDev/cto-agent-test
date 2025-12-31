"""Diff command implementation for myvcs."""

import difflib
from myvcs import utils, storage, repo, commit


def get_diff():
    """
    Generate unified diff between working directory and last commit.
    Returns (diff_text, error).
    """
    if not repo.is_repo_initialized():
        return None, "Not a myvcs repository"
    
    head_commit = repo.get_head()
    
    if not head_commit:
        return "", "No commits yet"
    
    # Load last commit
    commit_data = commit.load_commit(head_commit)
    if not commit_data:
        return None, "Failed to load commit"
    
    last_commit_files = commit_data["files"]
    
    # Get current files
    current_files = set(utils.get_all_files())
    last_files = set(last_commit_files.keys())
    
    all_files = sorted(current_files | last_files)
    
    diff_output = []
    
    for filepath in all_files:
        in_current = filepath in current_files
        in_last = filepath in last_files
        
        if in_current and in_last:
            # File exists in both - check for changes
            try:
                current_content = utils.read_file_binary(filepath)
                last_hash = last_commit_files[filepath]
                last_content = storage.retrieve_object(last_hash)
                
                if current_content != last_content:
                    file_diff = _generate_file_diff(filepath, last_content, current_content)
                    if file_diff:
                        diff_output.append(file_diff)
            except Exception:
                # Skip binary files or unreadable files
                continue
        
        elif in_current and not in_last:
            # New file
            diff_output.append(f"New file: {filepath}\n")
        
        elif not in_current and in_last:
            # Deleted file
            diff_output.append(f"Deleted file: {filepath}\n")
    
    return "\n".join(diff_output), None


def _generate_file_diff(filepath, old_content, new_content):
    """Generate unified diff for a single file."""
    try:
        old_lines = old_content.decode("utf-8").splitlines(keepends=True)
        new_lines = new_content.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        # Binary file
        return f"Binary file changed: {filepath}\n"
    
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"a/{filepath}",
        tofile=f"b/{filepath}",
        lineterm=""
    )
    
    diff_text = "".join(diff)
    return diff_text if diff_text else ""


def print_diff(diff_text):
    """Print diff output."""
    if diff_text:
        print(diff_text)
    else:
        print("No changes")
