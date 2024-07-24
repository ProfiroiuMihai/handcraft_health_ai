# 1. Dataset Loading
from datasets import load_dataset
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from openai import embeddings
import pandas as pd
import pymongo
import json
from pinecone import Pinecone
import os
from langchain.chains import RetrievalQA 
from sentence_transformers import SentenceTransformer


PINECONE_API_KEY="0fe93d1e-9dbe-440b-a385-25a0d77cc348" # available at app.pinecone.io
OPENAI_API_KEY="<your OpenAI API key>" # available at platform.openai.com/api-keys
MONGO_URI="mongodb+srv://sobhakharpoudel97:YOb50KBnELl80yDY@cluster0.6f3j5jy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

myclient = pymongo.MongoClient(MONGO_URI,)
db = myclient.get_database('healtheart')
collection = db.get_collection('products')

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "index1"
pineconeNamespace='default'


def insertToMongoDb():
    with open('data/product.json') as file:
        file_data = json.load(file)
        print("Inserting....")
        collection.insert_many(file_data)


# def upsertToPinecone():
    

def vectorSearch():
    llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-3.5-turbo",
    temperature=0.0
    )
    
    index=Pinecone.Index(index_name)
    embedder = SentenceTransformer('stsb-xlm-r-multilingual')
    xq = embedder.encode("My patient has red eyes, irritability, wakes up at 2am and is prone to anger . What is the TCM diagnosis and what herbal formula and acupoints should I use to treat it?")
    response=index.query(xq,top_k=2)
    print(response)
    

vectorSearch()
    