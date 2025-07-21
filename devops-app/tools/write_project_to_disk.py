import re
from pathlib import Path
from langchain_core.tools import tool

@tool
def write_project_to_disk(project_files_xml: str) -> str:
    """
    Parses an XML-like string containing a Terraform project structure and writes the files to a dedicated 'workspace/terraform_project_latest' directory.
    This tool will overwrite any existing files in that directory. Use this tool to create or update a Terraform project.

    Args:
        project_files_xml: A string containing the entire project structure, with each file enclosed in <file path="...">...</file> tags.
    Returns:
        A summary of the files that were written to disk, including the absolute path to the directory.
    """
    blocks = re.findall(r'<file path="(.+?)">(.*?)</file>', project_files_xml, re.DOTALL)
    if not blocks:
        return "No valid file blocks found."

    out_dir = Path("workspace/terraform_project_latest")
    out_dir.mkdir(parents=True, exist_ok=True)

    for path, content in blocks:
        fp = out_dir / path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content.strip(), encoding="utf-8")

    return f"Saved {len(blocks)} files to {out_dir.resolve()}"
