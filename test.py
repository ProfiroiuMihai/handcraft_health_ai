from datasets import load_dataset
import pandas as pd

# NOTE: Make sure you have an Hugging Face token (HF_TOKEN) in your development environemnt
# NOTE: https://huggingface.co/datasets/MongoDB/airbnb_embeddings
# NOTE: This dataset contains several records with datapoint representing an airbnb listing.
# NOTE: This dataset contains text and image embeddings, but this lessons only uses the text embeddings
dataset = load_dataset("MongoDB/airbnb_embeddings", streaming=True, split="train")
dataset = dataset.take(100)
# Convert the dataset to a pandas dataframe
dataset_df = pd.DataFrame(dataset)
dataset_df.head(5)
print("Columns:", dataset.to_json())

# import os
# import glob
# import pandas as pd

# contents = []
# json_dir_name = '/data/json'

# json_pattern = os.path.join(json_dir_name, '*.json')
# file_list = glob.glob(json_pattern)
# for file in file_list:
#   contents.append(pd.read(file))

# print(contents)

# import json
# import pandas as pd
# from glob import glob

# def merge_JsonFiles(filename):
#     result = list()
#     for f1 in filename:
#         with open(f1, 'r') as infile:
#             result.extend(json.load(infile))

#     with open('counseling3.json', 'w') as output_file:
#         json.dump(result, output_file)
# data=[]        
# for f_name in glob('data/json/*.json'):
#     data.append(f_name)
# print(data)    
# merge_JsonFiles(data)
# df = pd.concat([pd.read_json(f_name, lines=True) for f_name in glob('data/json/*.json')])