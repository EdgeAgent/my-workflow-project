import pandas as pd
import os

def sanitize_name(name):
    return "".join(c for c in name if c.isalnum() or c in (".", "_", "-")).rstrip()

def generate_main_readme(metadata_csv_path, output_path):
    df = pd.read_csv(metadata_csv_path)

    readme_content = "# My Workflow Project\n\n"
    readme_content += "This repository contains a collection of workflow definitions, each organized into its own directory with a dedicated README file.\n\n"
    readme_content += "## Workflows\n\n"
    readme_content += "| Workflow Name | Directory |\n"
    readme_content += "|---------------|-----------|\n"

    for index, row in df.iterrows():
        workflow_name = row["workflow_name"]
        sanitized_workflow_name = sanitize_name(workflow_name)
        # Link to the individual workflow's README.md
        readme_content += f"| {workflow_name} | [./workflows/{sanitized_workflow_name}/README.md](./workflows/{sanitized_workflow_name}/README.md) |\n"
    
    with open(output_path, "w") as f:
        f.write(readme_content)
    print(f"Generated main README at {output_path}")

if __name__ == "__main__":
    metadata_csv = "workflow_metadata.csv"
    output_file = "README.md"
    generate_main_readme(metadata_csv, output_file)

