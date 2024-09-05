from openai import OpenAI
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from streamlit_extras.switch_page_button import switch_page


# Check if history exists and is not empty
history = st.session_state.get('history')






system_prompt_template = """
You are an AI assistant specialized in various health and wellness practices. Your primary role is to help practitioners create comprehensive treatment plans and assist with tasks related to their specific modality. You should be knowledgeable about different health approaches, diagnostic techniques, and holistic practices.
Core Responsibilities:
- Create and refine treatment plans for various health modalities
- Assist with diagnosis and treatment strategy formulation
- Help define patient profiles and treatment goals
- Provide insights on health theories and modern applications
- Offer guidance on integrating different health practices
Interaction Style:
- Be professional yet empathetic in your communication
- Ask clarifying questions to gather all necessary information
- Provide structured, detailed responses
- Offer to elaborate on any point if the user needs more information
- Be proactive in suggesting additional considerations or potential issues
Treatment Plan Creation Process:
When a practitioner presents a case or health concern, ask for key details such as:
- Primary symptoms and health history
- Lifestyle factors and emotional state
- Key goals for treatment
Based on the provided information, draft a comprehensive treatment plan including:
- Executive summary
- Goals and non-goals
- Treatment modalities specific to the practitioner's field
- Diagnosis (based on the practitioner's modality)
- Narrative explanation of the treatment
- Success metrics
- Lifestyle and dietary recommendations
- Milestones and sequencing
Additional Guidelines:
- Consider the patient's holistic well-being in your recommendations
- Encourage practitioners to think about potential challenges
- Suggest ways to validate treatment effectiveness
- Be prepared to iterate on treatment plans
- Offer to explain complex concepts in understandable terms
Remember to adapt your responses to the practitioner's specific modality, level of expertise, and the needs of their patients.
"""
# Human Prompt Template
human_prompt_template = """
You're engaging with an AI assistant focused on health and wellness practices. This assistant is here to help you craft comprehensive treatment plans, assist with diagnoses, define patient profiles, and offer strategic health insights tailored to your specific modality.
To maximize the assistant's effectiveness:
- Be Clear and Concise: Share specific details about the patient's symptoms, health history, or the task you need assistance with.
- Prepare for Follow-ups: The assistant may ask additional questions to gather more context or details.
- Ask for Clarifications: Feel free to request explanations on any concepts or recommendations.
- Request Revisions: Don't hesitate to ask for adjustments or iterations on treatment plans or other outputs.
- Explore Various Aspects: Use the assistant to dive into patient profiles, treatment goals, and essential modalities specific to your practice.
Here's some brief information about the Practitioner:
<practitioner_info>
{collected_info}
</practitioner_info>
Use this to inform your responses.
Chat History between Practitioner and Assistant:
<chat_history>
{chat_history}
</chat_history>
Now, please answer the practitioner's question:
<user_instructions>
{user_input}
</user_instructions>
""" 

system_prompt = PromptTemplate(template=system_prompt_template, input_variables=[])
human_prompt = PromptTemplate(template=human_prompt_template, input_variables=["user_input","collected_info","chat_history"])

# Initialize the language model (you can choose your model and configuration)
openai_llm = ChatOpenAI(
    model="gpt-4o-2024-08-06",
    temperature=0.5,
    api_key= st.session_state.openai_key,
    streaming=True
)
# Create LLMChain for the system prompt
system_llm_chain = LLMChain(prompt=system_prompt, llm=openai_llm)

# Create LLMChain for the human prompt
human_llm_chain = LLMChain(prompt=human_prompt, llm=openai_llm,verbose=True,)

def warningMarkdown():
    st.warning(f"**Information Collection Not Completed please go back")
    if st.button("Go Back", type='primary'):
        switch_page("app")

def handle_submit():
    if st.session_state.user_input:
        user_input = st.session_state.user_input
        st.session_state.conversation.append({
            "role": "user", 
            "content": user_input,
        })
        with st.chat_message("user"):
            st.markdown(user_input)
        # First run the system prompt to establish context
        # system_response = system_llm_chain.run()
        collectedData= history[len(history)-1]
        
        # Then run the human prompt with user input
        response = human_llm_chain.run(user_input=user_input,collected_info=collectedData['collected_data'],chat_history=st.session_state.conversation)
       
        st.session_state.conversation.append({
            "role": "assistant", 
            "content": response,
        })
        with st.chat_message("assistant"):
            st.write(response)
        # st.session_state.user_input = ""
        st.components.v1.html(scroll_to_bottom_script)
        return response
        
def startConveration():
    # User input form
    # with st.form(key='user_input_form'):
    #     user_input = st.text_input("Ask your query to Chat PRD:", key="user_input")
    #     submit_button = st.form_submit_button(label='Send', on_click=handle_submit)
    if prompt :=st.chat_input("Ask me anything:", key="user_input"):
        handle_submit()
        
        
 
if 'conversation' not in st.session_state:
    st.session_state.conversation = []       


scroll_to_bottom_script = """
<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
"""

# Display chat history
for i, message in enumerate(st.session_state.conversation):
     with st.chat_message(message['role']):
        st.markdown(message['content'])
        st.markdown("---")  # Ad

if history:
    
    collectedData= history[len(history)-1]
    print(collectedData['collected_data'])
    if 'isCompleted' in collectedData:
        if(collectedData['isCompleted']):
            startConveration()
        else:
            warningMarkdown()   
    else:
        warningMarkdown()    
else:
    warningMarkdown()            
    if message["role"] == "human":
        # st.markdown(f"You:{message['content']}")
        with st.chat_message("user"):
            st.markdown(message['content'])
    elif message["role"] == "ai":
        with st.chat_message("assistant"):
            st.markdown(message['content'])
        # st.markdown(f"**AI:** {message['content']}")        
    st.markdown("---")  # Ad