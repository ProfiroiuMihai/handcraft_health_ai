import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate, LLMChain




PINECONE_API_KEY="0fe93d1e-9dbe-440b-a385-25a0d77cc348" # available at app.pinecone.io
OPENAI_API_KEY="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" # available at platform.openai.com/api-keys
MONGO_URI="mongodb+srv://sobhakharpoudel97:YOb50KBnELl80yDY@cluster0.6f3j5jy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
index_name = "index1"
pineconeNamespace='default'

EMBEDDINGS = OpenAIEmbeddings(api_key=OPENAI_API_KEY,embedding_ctx_length=3072,model='text-embedding-3-large')


CHAT_LLM = ChatOpenAI(api_key=OPENAI_API_KEY,model_name='gpt-3.5-turbo',temperature=0)



# Create Pinecone client with the API key
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(name=index_name)


vectorstore = PineconeVectorStore(index_name=index_name, embedding=EMBEDDINGS,pinecone_api_key=PINECONE_API_KEY)


SYSTEM_PROMPT = """
You are a expert in Traditional Chinese Medicine(TMC) . Take a reference from  `Notes from South Mountain : A guide to concentrate Herbs and Granules` and `Fundamentals of Chinese Medicine` to answer.

Use this Patient Medicine History: 

Medications: Valsartan HCTZ 320/25 mg once a day, Amlodipine Besylate 5 mg once a day, Atorvastatin 10 mg once a day, Metformin HCL ER 750 mg once a day, Aspirin 81 mg once a day. Allergies: Seasonal allergies causing sneezing/runny nose. Supplements: Probiotic - Bacillus Coagulans 133 mg once a day, Magnesium Citramate 135 mg once a day. Devices: CPAP machine

We have a list of product from which we will suggest some product for user

"Context: {context}"
"""

SYSTEM_PROMPT_PRODUCTS = """
You are a expert in Traditional Chinese Medicine(TMC) and a very good Medical diagnosis

Extract/suggest some medicinal products based on the text below. Don't suggest anything else just the products list in a comma seperated format: \n\n
"""