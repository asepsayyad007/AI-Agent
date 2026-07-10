from git import Repo, InvalidGitRepositoryError
from pathlib import Path


def _get_repo(path: str = "."):
    """Get a Git repo object from path."""
    try:
        return Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        return None


def git_status(path: str = "."):
    """Show working tree status."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    return {
        "success": True,
        "branch": repo.active_branch.name,
        "is_dirty": repo.is_dirty(),
        "untracked": repo.untracked_files,
        "changed": [item.a_path for item in repo.index.diff(None)],
        "staged": [item.a_path for item in repo.index.diff("HEAD")],
    }


def git_log(path: str = ".", count: int = 10):
    """Show recent commits."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    commits = []
    for commit in repo.iter_commits(max_count=count):
        commits.append({
            "hash": commit.hexsha[:7],
            "message": commit.message.strip(),
            "author": str(commit.author),
            "date": commit.committed_datetime.isoformat(),
        })

    return {"success": True, "commits": commits}


def git_diff(path: str = ".", staged: bool = False):
    """Show diff of changes."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    if staged:
        diff = repo.git.diff("--cached")
    else:
        diff = repo.git.diff()

    return {"success": True, "diff": diff}


def git_add(path: str = ".", files: list = None):
    """Stage files for commit."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    try:
        if files is None or files == ["."] or files == ["all"]:
            repo.git.add(A=True)
        else:
            repo.index.add(files)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def git_commit(path: str = ".", message: str = ""):
    """Commit staged changes."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    if not message:
        return {"success": False, "error": "Commit message is required"}

    try:
        repo.index.commit(message)
        return {"success": True, "message": message}
    except Exception as e:
        return {"success": False, "error": str(e)}


def git_branch(path: str = ".", name: str = None, checkout: bool = False):
    """List branches or create/checkout a branch."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    try:
        if name is None:
            branches = [b.name for b in repo.branches]
            return {
                "success": True,
                "current": repo.active_branch.name,
                "branches": branches,
            }

        if checkout:
            repo.git.checkout(name)
            return {"success": True, "switched_to": name}
        else:
            repo.create_head(name)
            return {"success": True, "created": name}

    except Exception as e:
        return {"success": False, "error": str(e)}


def git_checkout(path: str = ".", branch: str = ""):
    """Switch to a branch."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    try:
        repo.git.checkout(branch)
        return {"success": True, "switched_to": branch}
    except Exception as e:
        return {"success": False, "error": str(e)}


def git_push(path: str = ".", remote: str = "origin", branch: str = None):
    """Push commits to remote."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    try:
        if branch is None:
            branch = repo.active_branch.name
        repo.git.push(remote, branch)
        return {"success": True, "pushed": f"{remote}/{branch}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def git_pull(path: str = ".", remote: str = "origin", branch: str = None):
    """Pull from remote."""
    repo = _get_repo(path)
    if repo is None:
        return {"success": False, "error": "Not a git repository"}

    try:
        if branch is None:
            branch = repo.active_branch.name
        repo.git.pull(remote, branch)
        return {"success": True, "pulled": f"{remote}/{branch}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
