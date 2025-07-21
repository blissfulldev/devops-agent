from langchain_core.tools import tool
from pathlib import Path

@tool
def configure_pipeline(project_dir: str, pipeline_name: str) -> str:
    """
    Parses an XML-like string containing a Terraform project structure and writes the files to a new, unique directory.
    Use this tool as the final step after generating all necessary Terraform code. A unique directory will be created automatically.

    Args:
        project_files_xml: A string containing the entire project structure, with each file enclosed in <file path="...">...</file> tags.
    Returns:
        A summary of the files that were written to disk, including the name of the new directory.
    """
    wf_dir = Path(project_dir) / ".github" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    wf_file = wf_dir / f"{pipeline_name}.yml"
    wf_file.write_text(f"# CI/CD pipeline for {pipeline_name}\n", encoding="utf-8")
    return f"Created CI/CD file at {wf_file}"
