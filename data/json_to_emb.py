import json
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle

def load_json(file_path):
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return json.load(file)
        except UnicodeDecodeError:
            continue
        except json.JSONDecodeError as e:
            print(f"JSON decode error with {encoding} encoding: {e}")
            continue
    raise ValueError(f"Unable to decode the file with any of the encodings: {encodings}")

def extract_fields_and_metadata(data):
    extracted = []
    metadata = []
    for item in data:
        product_id = str(item.get("PRODUCTID", ""))
        ingredients = str(item.get("INGREDIENTS", ""))
        long_ingredients = str(item.get("DETAILED_DESCRIPTION", ""))
        description = item.get("SHORT_DESCRIPTION", "")

        name = item.get("NAME", "")
        combined = f"{name} {description} {long_ingredients} {ingredients}".strip()
        extracted.append(combined)
        metadata.append({
            "PRODUCTID": product_id,
            "NAME": name
        })
    return extracted, metadata

def create_embeddings(data, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(data)
    return embeddings

def save_embeddings_and_metadata(embeddings, metadata, output_file):
    data_to_save = {
        "embeddings": embeddings,
        "metadata": metadata
    }
    with open(output_file, 'wb') as f:
        pickle.dump(data_to_save, f)

def main():
    input_file = 'merged_output.json'
    output_file = 'embeddings_with_metadata.pkl'

    try:
        # Load JSON data
        json_data = load_json(input_file)
        
        # Extract relevant fields and metadata
        extracted_data, metadata = extract_fields_and_metadata(json_data)

        # Create embeddings
        embeddings = create_embeddings(extracted_data)

        # Save embeddings and metadata
        save_embeddings_and_metadata(embeddings, metadata, output_file)

        print(f"Embeddings and metadata saved to {output_file}")
        print(f"Number of embeddings created: {len(embeddings)}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()