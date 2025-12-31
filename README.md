# myvcs - Minimal Version Control System

A lightweight, offline Git-like version control system implemented in Python using only the standard library. myvcs provides essential version control functionality including commits, diffs, status tracking, and checkout capabilities without any external dependencies.

## Features

- **Offline-first**: No network connectivity required, all operations are local
- **Content-addressed storage**: Files are stored by their content hash, ensuring deduplication
- **Snapshot-based commits**: Each commit captures the complete state of your project
- **Unified diff support**: Line-by-line comparison using Python's difflib
- **Simple and deterministic**: Reproducible commit IDs based on content hashing

## Usage

All commands are run using Python's module syntax:

### Initialize a Repository

```bash
python -m myvcs init
```

Creates a `.myvcs/` directory in your current working directory with the following structure:
- `objects/` - Content-addressed storage for file blobs
- `commits/` - Commit metadata files
- `index` - Staging area snapshot
- `HEAD` - Points to the current commit

### Check Status

```bash
python -m myvcs status
```

Displays changes in your working directory compared to the last commit:
- **Modified files**: Existing files with changed content
- **New files**: Files not present in the last commit
- **Deleted files**: Files present in the last commit but removed from working directory

Example output:
```
Modified files:
  src/main.py

New files:
  src/utils.py

Deleted files:
  old_file.txt
```

### Create a Commit

```bash
python -m myvcs commit -m "Your commit message here"
```

Creates a new commit with all current files in your working directory. The command:
1. Hashes all file contents using SHA-256
2. Stores file blobs in the objects directory (deduplicated automatically)
3. Creates commit metadata with timestamp and file mappings
4. Updates HEAD to point to the new commit
5. Prints the deterministic commit ID

Example output:
```
a3f5c8d9e2b4f1a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

### View Differences

```bash
python -m myvcs diff
```

Shows a unified diff of all changes between your working directory and the last commit. Uses standard diff format with:
- File headers showing paths
- Line numbers and change indicators
- `+` for added lines
- `-` for removed lines

Example output:
```
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
 def main():
+    print("Hello, world!")
     pass
```

### Restore a Previous Commit

```bash
python -m myvcs checkout <commit_id>
```

Restores your working directory to the exact state of the specified commit:
- Overwrites all tracked files with their committed versions
- Removes files that weren't present in that commit
- Updates HEAD to point to the checked-out commit

Example:
```bash
python -m myvcs checkout a3f5c8d9e2b4f1a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```

## Architecture and Design Decisions

### Content-Addressed Storage

myvcs uses a content-addressed storage model where each file is stored in the `.myvcs/objects/` directory with its SHA-256 hash as the filename. This approach provides several benefits:

1. **Automatic deduplication**: Identical file contents are stored only once, regardless of filename or location
2. **Integrity verification**: The hash serves as a checksum, ensuring data hasn't been corrupted
3. **Deterministic storage**: The same content always produces the same hash and storage location

### Snapshot-Based Commits

Unlike delta-based systems, myvcs uses a snapshot model where each commit represents the complete state of all files at that point in time. Each commit stores:

- **Commit ID**: Deterministically generated from parent commit, timestamp, message, and complete file list
- **Parent commit**: Reference to the previous commit (empty for first commit)
- **Timestamp**: Unix timestamp when the commit was created
- **Message**: User-provided commit description
- **File mappings**: Dictionary of all file paths to their content hashes

This snapshot approach simplifies the implementation while maintaining full history. The deterministic commit ID ensures that identical project states always produce the same commit hash, making the system reproducible.

### Module Organization

The codebase is organized into focused modules with clear separation of concerns:

- **main.py**: CLI parsing and command routing
- **repo.py**: Repository initialization and state management (HEAD, index)
- **storage.py**: Low-level content hashing and object storage
- **commit.py**: Commit creation and metadata handling
- **status.py**: Working directory comparison logic
- **diff.py**: Unified diff generation using difflib
- **checkout.py**: Snapshot restoration and file cleanup
- **utils.py**: Filesystem utilities with .myvcs directory filtering

This modular structure keeps functions small (typically under 30 lines), makes the code easy to test and maintain, and allows each module to focus on a single responsibility.

## Technical Constraints

- **Python standard library only**: No external dependencies required
- **No global state**: All state is passed through function parameters or stored in `.myvcs/`
- **Deterministic operations**: Same input always produces same output
- **Offline operation**: No network calls or external services
- **Linear history**: No branches, merges, or complex graph structures

## File Tracking

myvcs automatically tracks all files in your working directory except:
- The `.myvcs/` directory itself and all its contents
- Files are compared by content hash, not modification time

There is no explicit "add" or "stage" command - all files are included in each commit.

## Limitations

This is a minimal VCS designed for educational purposes and simple use cases. It does not support:
- Branching or merging
- Remote repositories or synchronization
- Partial commits (staging specific files)
- Configuration files or ignore patterns
- Commit history traversal commands
- Tags or references beyond HEAD

## Error Handling

myvcs provides clear error messages for common issues:
- Operations outside a myvcs repository
- Missing commit messages
- Non-existent commit IDs during checkout
- File read/write errors

All errors are reported to stderr with descriptive messages and appropriate exit codes.
