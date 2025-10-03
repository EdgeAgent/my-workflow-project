import json
import os
import pandas as pd

def generate_readme(workflow_name, json_content, output_dir):
    readme_path = os.path.join(output_dir, "README.md")
    
    # Extract relevant information from JSON
    nodes = json_content.get("nodes", [])
    node_names = [node.get("name", "Unknown Node") for node in nodes]
    node_types = [node.get("type", "Unknown Type") for node in nodes]

    readme_content = f"# Workflow: {workflow_name}\n\n"
    readme_content += f"## Overview\n\nThis document provides an overview of the \'{workflow_name}\' workflow.\n\n"
    
    if node_names:
        readme_content += "## Workflow Steps (Nodes)\n\n"
        readme_content += "| Step Name | Type |\n"
        readme_content += "|-----------|------|\n"
        for i in range(len(node_names)):
            readme_content += f"| {node_names[i]} | {node_types[i]} |\n"
        readme_content += "\n"
    else:
        readme_content += "## Workflow Steps (Nodes)\n\nNo specific nodes found for this workflow.\n\n"

    readme_content += "## Raw JSON\n\n```json\n" + json.dumps(json_content, indent=2) + "\n```\n"

    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"Generated README for {workflow_name} at {readme_path}")

def main():
    base_workflows_dir = "workflows"
    
    for workflow_folder in os.listdir(base_workflows_dir):
        workflow_path = os.path.join(base_workflows_dir, workflow_folder)
        if os.path.isdir(workflow_path):
            json_files = [f for f in os.listdir(workflow_path) if f.endswith(".json")]
            if json_files:
                # Assuming one JSON file per workflow folder
                json_file_name = json_files[0]
                json_file_path = os.path.join(workflow_path, json_file_name)
                
                with open(json_file_path, "r") as f:
                    json_content = json.load(f)
                
                workflow_name = json_content.get("name", workflow_folder.replace("_", " ").title())
                generate_readme(workflow_name, json_content, workflow_path)

if __name__ == "__main__":
    main()

