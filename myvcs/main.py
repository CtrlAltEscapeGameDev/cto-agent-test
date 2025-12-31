"""CLI entry point and command routing for myvcs."""

import sys
from myvcs import repo, commit, status, diff, checkout


def print_usage():
    """Print usage information."""
    usage = """Usage: python -m myvcs <command> [<args>]

Commands:
  init                Initialize a new myvcs repository
  status              Show working tree status
  commit -m <msg>     Record changes to the repository
  diff                Show changes between working directory and last commit
  checkout <id>       Restore working directory to a specific commit
"""
    print(usage)


def cmd_init():
    """Handle init command."""
    success, message = repo.init_repo()
    print(message)
    return 0 if success else 1


def cmd_status():
    """Handle status command."""
    status_dict, error = status.get_status()
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    
    status.print_status(status_dict)
    return 0


def cmd_commit(args):
    """Handle commit command."""
    # Parse -m flag
    if len(args) < 2 or args[0] != "-m":
        print("Error: commit requires -m flag with message", file=sys.stderr)
        print("Usage: python -m myvcs commit -m \"message\"", file=sys.stderr)
        return 1
    
    message = args[1]
    
    success, result = commit.create_commit(message)
    if success:
        print(result)
        return 0
    else:
        print(f"Error: {result}", file=sys.stderr)
        return 1


def cmd_diff():
    """Handle diff command."""
    diff_text, error = diff.get_diff()
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    
    diff.print_diff(diff_text)
    return 0


def cmd_checkout(args):
    """Handle checkout command."""
    if len(args) < 1:
        print("Error: checkout requires commit id", file=sys.stderr)
        print("Usage: python -m myvcs checkout <commit_id>", file=sys.stderr)
        return 1
    
    commit_id = args[0]
    
    success, message = checkout.checkout_commit(commit_id)
    print(message)
    return 0 if success else 1


def main():
    """Main entry point for CLI."""
    if len(sys.argv) < 2:
        print_usage()
        return 1
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "init":
        return cmd_init()
    elif command == "status":
        return cmd_status()
    elif command == "commit":
        return cmd_commit(args)
    elif command == "diff":
        return cmd_diff()
    elif command == "checkout":
        return cmd_checkout(args)
    else:
        print(f"Error: unknown command '{command}'", file=sys.stderr)
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
