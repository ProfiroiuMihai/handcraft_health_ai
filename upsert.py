from constant import index
from langchain_community.document_loaders import Docx2txtLoader,UnstructuredWordDocumentLoader,PyPDFLoader

loader = UnstructuredWordDocumentLoader("./data/FunChiMed Patterns.docx")

def upsert():
    data = loader.load()
    print(data)
    # index.upsert()
    
upsert()   