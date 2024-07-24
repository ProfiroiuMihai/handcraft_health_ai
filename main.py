import streamlit as st
from constant import SYSTEM_PROMPT,CHAT_LLM, SYSTEM_PROMPT_PRODUCTS,vectorstore
from utils import get_query_embeddings, query_pinecone_index, better_query_response
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.conversational_retrieval.base import   ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def main():
    st.title("Healtheart ")
    user_question = st.text_input("Ask your question about your health issue:")
    submit_button = st.button("Enter")

    if submit_button:
        # query_embeddings = get_query_embeddings(user_question)
        # answers = query_pinecone_index(query_embeddings,top_k=8)
        # print(answers)
        # conv_chain = ConversationalRetrievalChain.from_llm(
        #   llm=CHAT_LLM,
        #   chain_type="stuff",
        #   retriever=vectorstore.as_retriever(search_kwargs={"k": 5}), 
        #   memory=st.session_state.memory,
        #   condense_question_prompt=prompt,
        #   combine_docs_chain_kwargs={"prompt": user_question},
        #   output_key='answer',
        #   return_source_documents=True,
        #   get_chat_history=lambda h : h,
        #   verbose = False
        # )
        # responseData = conv_chain.run(user_question)
        # qa = RetrievalQA.from_llm(  
        #     llm=CHAT_LLM,  
        #     chain_type="stuff",  
        #     retriever=vectorstore.as_retriever(),
        # )
        prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
        ]
        )
        question_answer_chain = create_stuff_documents_chain(CHAT_LLM, prompt)
        chain = create_retrieval_chain(vectorstore.as_retriever(search_kwargs={'k':10}), question_answer_chain)
        responseData= chain.invoke({"input": user_question})
        answerr = responseData['answer']
        humanMessage= answerr
        messages = [
            ("system", SYSTEM_PROMPT_PRODUCTS),
            ("human",humanMessage),
        ]
        productList=CHAT_LLM.invoke(messages)
        st.write(productList.content)


if __name__ == "__main__":
    main()