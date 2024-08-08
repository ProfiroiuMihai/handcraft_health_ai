import json
import os
from pathlib import Path

def load_json_file(file_path):
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return json.load(file)
        except UnicodeDecodeError:
            continue
        except json.JSONDecodeError as e:
            print(f"JSON decode error in file {file_path} with {encoding} encoding: {e}")
            continue
    raise ValueError(f"Unable to decode the file {file_path} with any of the encodings: {encodings}")

def merge_json_files(folder_path, output_file):
    folder = Path(folder_path)
    all_data = []

    # Iterate through all JSON files in the folder
    for file_path in folder.glob('*.json'):
        try:
            data = load_json_file(file_path)
            if isinstance(data, list):
                all_data.extend(data)
            else:
                print(f"Warning: {file_path} does not contain a JSON array. Skipping.")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_data, outfile, indent=2)

    return len(all_data)

def main():
    folder_path = 'json'  # Replace with your folder path
    output_file = 'merged_output.json'

    try:
        total_items = merge_json_files(folder_path, output_file)
        print(f"Successfully merged JSON files.")
        print(f"Total items in merged file: {total_items}")
        print(f"Merged data saved to: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()