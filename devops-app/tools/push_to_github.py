import os
from langchain_core.tools import tool
from github import Github
import pathlib

@tool
def push_to_github(project_dir: str, repo_name: str, commit_message: str = "Add generated infra") -> str:
    """
    Parses an XML-like string containing a Terraform project structure and writes the files to a new, unique directory.
    Use this tool as the final step after generating all necessary Terraform code. A unique directory will be created automatically.

    Args:
        project_files_xml: A string containing the entire project structure, with each file enclosed in <file path="...">...</file> tags.
    Returns:
        A summary of the files that were written to disk, including the name of the new directory.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "Error: GITHUB_TOKEN missing"

    gh = Github(token)
    user = gh.get_user()
    repo = gh.get_repo(repo_name)

    for fp in pathlib.Path(project_dir).rglob("*"):
        if fp.is_file():
            rel = fp.relative_to(project_dir).as_posix()
            content = fp.read_text()
            try:
                existing = repo.get_contents(rel)
                repo.update_file(existing.path, commit_message, content, existing.sha)
            except:
                repo.create_file(rel, commit_message, content)

    return f"🔗 https://github.com/{repo_name}"
