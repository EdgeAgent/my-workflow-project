import json
import os
import pandas as pd
import sys

def extract_metadata(json_files_path):
    data = []
    for file_path in json_files_path:
        try:
            with open(file_path, 'r') as f:
                content = json.load(f)
                file_name = os.path.basename(file_path)
                workflow_name = content.get('name', 'N/A')
                data.append({'filename': file_name, 'workflow_name': workflow_name, 'filepath': file_path})
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
    return pd.DataFrame(data)

if __name__ == '__main__':
    json_files = sys.argv[1:]
    if not json_files:
        print("Usage: python3.11 extract_metadata.py <json_file1> <json_file2> ...", file=sys.stderr)
        sys.exit(1)
    
    df = extract_metadata(json_files)
    df.to_csv('workflow_metadata.csv', index=False)
