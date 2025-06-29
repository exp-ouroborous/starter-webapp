#!/usr/bin/env python3
"""
Branch Comparison Script

This script compares local and remote Git branches and shows differences.

REQUIREMENTS:
    pip install GitPython PyGithub

USAGE:
    python3 scripts/compare-branches.bash

OPTIONAL SETUP:
    export GITHUB_TOKEN=your_github_token
    
    With a GitHub token, the script will show additional repository information
    and can access private repositories. Create a token at:
    https://github.com/settings/tokens

WHAT IT DOES:
    - Fetches latest remote information
    - Lists all local and remote branches
    - Shows branches that exist locally but not remotely
    - Shows branches that exist remotely but not locally
    - For common branches, shows if local is ahead/behind remote
    - With GitHub token: shows additional repository metadata
"""

import git
from github import Github
import os
import sys

def get_github_repo():
    """Get GitHub repository object from remote origin URL."""
    try:
        repo = git.Repo('.')
        origin_url = repo.remotes.origin.url
        
        # Parse GitHub repo from URL
        if 'github.com' in origin_url:
            if origin_url.startswith('git@'):
                # SSH format: git@github.com:user/repo.git
                repo_path = origin_url.split(':')[1].replace('.git', '')
            else:
                # HTTPS format: https://github.com/user/repo.git
                repo_path = origin_url.split('github.com/')[1].replace('.git', '')
            
            # Get GitHub token from environment
            token = os.getenv('GITHUB_TOKEN')
            if token:
                g = Github(token)
                return g.get_repo(repo_path), repo
            else:
                print("Warning: GITHUB_TOKEN not set, remote branch info may be limited")
                return None, repo
        else:
            print("Not a GitHub repository")
            return None, repo
    except Exception as e:
        print(f"Error accessing repository: {e}")
        return None, None

def compare_branches():
    """Compare local and remote branches."""
    github_repo, local_repo = get_github_repo()
    
    if not local_repo:
        print("Error: Could not access local repository")
        return
    
    print("Fetching latest remote information...")
    try:
        local_repo.remotes.origin.fetch(prune=True)
    except Exception as e:
        print(f"Warning: Could not fetch from remote: {e}")
    
    print("\n=== Branch Comparison Report ===\n")
    
    # Get local branches
    local_branches = [ref.name for ref in local_repo.heads]
    
    # Get remote branches
    remote_branches = []
    try:
        remote_branches = [ref.name.replace('origin/', '') for ref in local_repo.remotes.origin.refs if 'HEAD' not in ref.name]
    except Exception as e:
        print(f"Warning: Could not get remote branches: {e}")
    
    print("Local branches:")
    for branch in sorted(local_branches):
        print(f"  {branch}")
    
    print("\nRemote branches:")
    for branch in sorted(remote_branches):
        print(f"  {branch}")
    
    print("\n=== Differences ===\n")
    
    # Find branches that exist locally but not remotely
    local_only = set(local_branches) - set(remote_branches)
    if local_only:
        print("Branches that exist locally but NOT remotely:")
        for branch in sorted(local_only):
            print(f"  {branch}")
    else:
        print("All local branches exist remotely.")
    
    print()
    
    # Find branches that exist remotely but not locally
    remote_only = set(remote_branches) - set(local_branches)
    if remote_only:
        print("Branches that exist remotely but NOT locally:")
        for branch in sorted(remote_only):
            print(f"  {branch}")
    else:
        print("All remote branches exist locally.")
    
    print("\n=== Commit Differences ===\n")
    
    # For branches that exist in both places, check if they're in sync
    common_branches = set(local_branches) & set(remote_branches)
    
    if common_branches:
        print("Checking commit differences for common branches:")
        for branch_name in sorted(common_branches):
            try:
                local_branch = local_repo.heads[branch_name]
                remote_branch = local_repo.remotes.origin.refs[branch_name]
                
                # Count commits ahead/behind
                ahead_commits = list(local_repo.iter_commits(f'{remote_branch}..{local_branch}'))
                behind_commits = list(local_repo.iter_commits(f'{local_branch}..{remote_branch}'))
                
                ahead_count = len(ahead_commits)
                behind_count = len(behind_commits)
                
                if ahead_count > 0 or behind_count > 0:
                    print(f"  {branch_name}:")
                    if ahead_count > 0:
                        print(f"    Local is {ahead_count} commit(s) ahead of remote")
                    if behind_count > 0:
                        print(f"    Local is {behind_count} commit(s) behind remote")
            except Exception as e:
                print(f"  {branch_name}: Could not compare ({e})")
    else:
        print("No common branches found.")
    
    # Additional GitHub info if available
    if github_repo:
        try:
            print(f"\n=== GitHub Repository Info ===")
            print(f"Repository: {github_repo.full_name}")
            print(f"Default branch: {github_repo.default_branch}")
            
            # Get GitHub branches
            github_branches = [branch.name for branch in github_repo.get_branches()]
            print(f"Total GitHub branches: {len(github_branches)}")
            
        except Exception as e:
            print(f"Could not fetch GitHub info: {e}")
    
    # Check if local-only branches have been merged to main
    if local_only:
        print("\n=== Merge Status Check ===\n")
        print("Checking if local-only branches have been merged to main:")
        
        try:
            # Get the default/main branch
            main_branch = 'main'
            if github_repo:
                main_branch = github_repo.default_branch
            
            # Check if main branch exists locally
            if main_branch not in local_branches:
                print(f"Warning: {main_branch} branch not found locally")
            else:
                for branch_name in sorted(local_only):
                    try:
                        # Check if branch has been merged into main
                        main_commits = set(commit.hexsha for commit in local_repo.iter_commits(main_branch))
                        branch_commits = set(commit.hexsha for commit in local_repo.iter_commits(branch_name))
                        
                        # If all branch commits are in main, it's been merged
                        if branch_commits.issubset(main_commits):
                            print(f"  {branch_name}: ✓ MERGED (safe to delete)")
                        else:
                            # Check if branch is ahead of main
                            unmerged_commits = list(local_repo.iter_commits(f'{main_branch}..{branch_name}'))
                            if unmerged_commits:
                                print(f"  {branch_name}: ✗ NOT MERGED ({len(unmerged_commits)} unique commits)")
                            else:
                                print(f"  {branch_name}: ✓ MERGED (safe to delete)")
                    except Exception as e:
                        print(f"  {branch_name}: Could not check merge status ({e})")
        except Exception as e:
            print(f"Could not check merge status: {e}")

    print("\nDone!")

if __name__ == "__main__":
    # Check if required libraries are installed
    try:
        import git
        from github import Github
    except ImportError as e:
        print(f"Error: Required libraries not installed.")
        print("Please install with: pip install GitPython PyGithub")
        sys.exit(1)
    
    compare_branches()