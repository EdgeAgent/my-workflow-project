import pandas as pd
import os
import shutil

def sanitize_name(name):
    return "".join(c for c in name if c.isalnum() or c in (".", "_", "-")).rstrip()

def organize_files(metadata_csv_path, base_workflows_dir):
    df = pd.read_csv(metadata_csv_path)
    
    if not os.path.exists(base_workflows_dir):
        os.makedirs(base_workflows_dir)

    for index, row in df.iterrows():
        original_filepath = row["filepath"]
        workflow_name = row["workflow_name"]
        filename = row["filename"]

        sanitized_workflow_name = sanitize_name(workflow_name)
        destination_dir = os.path.join(base_workflows_dir, sanitized_workflow_name)
        
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        destination_filepath = os.path.join(destination_dir, filename)
        shutil.copy(original_filepath, destination_filepath)
        print(f"Moved {original_filepath} to {destination_filepath}")

if __name__ == "__main__":
    metadata_csv = "workflow_metadata.csv"
    workflows_directory = "workflows"
    organize_files(metadata_csv, workflows_directory)

