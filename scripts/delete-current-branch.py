#!/usr/bin/env python3
"""
Delete Current Branch Script

This script safely deletes the current branch after verifying it has been merged to main.
Handles both regular merges and squash-and-merge workflows.

REQUIREMENTS:
    pip install GitPython

USAGE:
    python3 scripts/delete-current-branch.py

WHAT IT DOES:
    - Gets the current branch name
    - Pulls latest changes from main
    - Verifies the current branch has been merged to main (or squash merged)
    - Prompts user for confirmation before deletion
    - Deletes the branch and switches back to main
    - Handles safety checks to prevent accidental deletion
    
SQUASH MERGE DETECTION:
    - Checks if remote branch has been deleted (indicates merge)
    - Looks for branch name references in recent main commits
    - Safely handles cases where commits don't match due to squashing
"""

import git
import sys

def get_repo():
    """Get the Git repository object."""
    try:
        repo = git.Repo('.')
        return repo
    except Exception as e:
        print(f"Error: Could not access repository: {e}")
        return None

def pull_main(repo):
    """Pull latest changes from main branch."""
    try:
        print("Pulling latest changes from main...")
        
        # Fetch latest changes
        repo.remotes.origin.fetch()
        
        # Check if main branch exists locally
        if 'main' not in [ref.name for ref in repo.heads]:
            print("Error: 'main' branch not found locally")
            return False
            
        # Switch to main and pull
        main_branch = repo.heads['main']
        main_branch.checkout()
        
        # Pull latest changes
        repo.remotes.origin.pull('main')
        print(" Successfully pulled latest changes from main")
        return True
        
    except Exception as e:
        print(f"Error pulling main: {e}")
        return False

def check_merge_status(repo, branch_name):
    """Check if the branch has been merged to main (handles squash and merge)."""
    try:
        # For squash and merge workflows, we need to check if the remote branch exists
        # If the remote branch has been deleted, it's likely been merged
        
        # First check if remote branch still exists
        remote_branches = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs if 'HEAD' not in ref.name]
        remote_branch_exists = branch_name in remote_branches
        
        # Check for unmerged commits (commits ahead of main)
        unmerged_commits = list(repo.iter_commits(f'main..{branch_name}'))
        
        if not unmerged_commits:
            # No commits ahead of main - safe to delete
            return True, "Branch has no commits ahead of main (safe to delete)"
        
        if not remote_branch_exists:
            # Remote branch deleted and we have local commits - likely squash merged
            return True, f"Remote branch deleted, local has {len(unmerged_commits)} commits (likely squash merged)"
        
        # Remote branch exists and we have unmerged commits
        if len(unmerged_commits) > 0:
            # Check if this might be a squash merge scenario by examining commit messages
            # Look for recent commits in main that might contain the branch name
            recent_main_commits = list(repo.iter_commits('main', max_count=10))
            branch_mentioned_in_main = any(
                branch_name.replace('/', '-') in commit.message.lower() or 
                branch_name.split('/')[-1] in commit.message.lower()
                for commit in recent_main_commits
            )
            
            if branch_mentioned_in_main:
                return True, f"Branch likely squash merged (found reference in recent main commits)"
            else:
                return False, f"Branch has {len(unmerged_commits)} unmerged commits and remote branch exists"
        
        return True, "Branch appears to be merged"
                
    except Exception as e:
        return False, f"Could not check merge status: {e}"

def delete_branch_interactive(repo, branch_name):
    """Interactively delete the branch after confirmation."""
    print(f"\n=== Branch Deletion Confirmation ===")
    print(f"Branch to delete: {branch_name}")
    print(f"You are currently on: main")
    print(f"This action cannot be undone.")
    
    while True:
        response = input(f"\nDelete branch '{branch_name}'? (Y/n): ").strip().lower()
        
        if response in ['y', 'yes', '']:
            try:
                # Delete the branch
                repo.delete_head(branch_name, force=False)
                print(f" Successfully deleted branch '{branch_name}'")
                
                # Try to delete remote branch if it exists
                try:
                    repo.remotes.origin.push(f':refs/heads/{branch_name}')
                    print(f" Successfully deleted remote branch 'origin/{branch_name}'")
                except Exception as e:
                    print(f"Note: Could not delete remote branch (may not exist): {e}")
                
                return True
            except Exception as e:
                print(f"Error deleting branch: {e}")
                return False
                
        elif response in ['n', 'no']:
            print("Branch deletion cancelled.")
            return False
        else:
            print("Please enter 'Y' for yes or 'n' for no.")

def main():
    """Main function to orchestrate branch deletion."""
    print("=== Safe Branch Deletion Script ===\n")
    
    # Check if required libraries are installed
    try:
        import git
    except ImportError:
        print("Error: GitPython not installed.")
        print("Please install with: pip install GitPython")
        sys.exit(1)
    
    # Get repository
    repo = get_repo()
    if not repo:
        sys.exit(1)
    
    # Get current branch
    try:
        current_branch = repo.active_branch.name
    except Exception as e:
        print(f"Error: Could not get current branch: {e}")
        print("Make sure you're not in a detached HEAD state.")
        sys.exit(1)
    
    print(f"Current branch: {current_branch}")
    
    # Safety check: don't delete main branch
    if current_branch == 'main':
        print("Error: Cannot delete the main branch!")
        sys.exit(1)
    
    # Safety check: don't delete if there are uncommitted changes
    if repo.is_dirty():
        print("Error: You have uncommitted changes. Please commit or stash them first.")
        sys.exit(1)
    
    # Pull latest changes from main
    if not pull_main(repo):
        print("Failed to pull latest changes from main. Aborting.")
        sys.exit(1)
    
    # Switch back to the branch we want to delete to check merge status
    try:
        branch_to_delete = repo.heads[current_branch]
        branch_to_delete.checkout()
        print(f"Switched back to {current_branch} for merge verification")
    except Exception as e:
        print(f"Error switching back to branch: {e}")
        sys.exit(1)
    
    # Check if branch has been merged
    is_merged, message = check_merge_status(repo, current_branch)
    
    print(f"\n=== Merge Status Check ===")
    print(f"Branch: {current_branch}")
    print(f"Status: {message}")
    
    if not is_merged:
        print(f"\nBranch '{current_branch}' has NOT been merged to main!")
        print("This branch contains commits that are not in main.")
        print("Please merge this branch first or use 'git branch -D' to force delete.")
        sys.exit(1)
    
    print(f" Branch '{current_branch}' has been merged to main and is safe to delete.")
    
    # Switch back to main before deletion
    try:
        repo.heads['main'].checkout()
        print(f"Switched to main branch")
    except Exception as e:
        print(f"Error switching to main: {e}")
        sys.exit(1)
    
    # Interactive deletion
    if delete_branch_interactive(repo, current_branch):
        print(f"\n Branch cleanup completed successfully!")
        print(f"You are now on the main branch.")
    else:
        print(f"\nBranch '{current_branch}' was not deleted.")

if __name__ == "__main__":
    main()