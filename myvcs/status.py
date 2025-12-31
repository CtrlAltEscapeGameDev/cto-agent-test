"""Status command implementation for myvcs."""

from myvcs import utils, storage, repo, commit


def get_status():
    """
    Compare working directory with last commit.
    Returns dict with: modified, new, deleted files.
    """
    if not repo.is_repo_initialized():
        return None, "Not a myvcs repository"
    
    head_commit = repo.get_head()
    
    # Get current working directory files
    current_files = {}
    all_files = utils.get_all_files()
    for filepath in all_files:
        try:
            content = utils.read_file_binary(filepath)
            file_hash = storage.compute_hash(content)
            current_files[filepath] = file_hash
        except Exception:
            continue
    
    # Get last commit files
    if head_commit:
        commit_data = commit.load_commit(head_commit)
        if commit_data:
            last_commit_files = commit_data["files"]
        else:
            last_commit_files = {}
    else:
        last_commit_files = {}
    
    # Compare
    modified = []
    new = []
    deleted = []
    
    # Check for new and modified files
    for filepath, file_hash in current_files.items():
        if filepath not in last_commit_files:
            new.append(filepath)
        elif last_commit_files[filepath] != file_hash:
            modified.append(filepath)
    
    # Check for deleted files
    for filepath in last_commit_files:
        if filepath not in current_files:
            deleted.append(filepath)
    
    return {
        "modified": sorted(modified),
        "new": sorted(new),
        "deleted": sorted(deleted)
    }, None


def print_status(status_dict):
    """Print status in readable format."""
    if status_dict["modified"]:
        print("Modified files:")
        for filepath in status_dict["modified"]:
            print(f"  {filepath}")
        print()
    
    if status_dict["new"]:
        print("New files:")
        for filepath in status_dict["new"]:
            print(f"  {filepath}")
        print()
    
    if status_dict["deleted"]:
        print("Deleted files:")
        for filepath in status_dict["deleted"]:
            print(f"  {filepath}")
        print()
    
    if not status_dict["modified"] and not status_dict["new"] and not status_dict["deleted"]:
        print("No changes")
