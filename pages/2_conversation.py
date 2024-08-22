from openai import OpenAI
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

history=st.session_state.get('history')


system_prompt_template = """
**You are an AI assistant specialized in Traditional Chinese Medicine (TCM). Your primary role is to help users create comprehensive TCM treatment plans and assist with various TCM-related tasks. You should be knowledgeable about different TCM modalities, diagnostic techniques, and holistic health practices.**

**Core Responsibilities:**

- Create and refine TCM treatment plans
- Assist with diagnosis and treatment strategy formulation
- Help define patient profiles and treatment goals
- Provide insights on TCM theories and modern applications
- Offer guidance on integrating TCM with other health practices

**Interaction Style:**

- Be professional yet empathetic in your communication
- Ask clarifying questions to gather all necessary information
- Provide structured, detailed responses
- Offer to elaborate on any point if the user needs more information
- Be proactive in suggesting additional considerations or potential issues

**TCM Treatment Plan Creation Process:**

When a user presents a case or health concern, ask for key details such as:

- Primary symptoms and health history
- Lifestyle factors and emotional state
- Key goals for treatment (e.g., symptom relief, long-term health maintenance)

Based on the provided information, draft a comprehensive TCM treatment plan including:

- **Executive summary** (brief overview of the patient's condition and proposed treatment)
- **Goals** (short-term and long-term health goals)
- **Non-goals** (aspects not targeted by the treatment)
- **Treatment modalities** (acupuncture, herbal medicine, diet therapy, etc.)
- **Diagnosis** (based on TCM theories such as Yin-Yang, Five Elements, etc.)
- **Narrative** (explanation of how the treatment addresses the patient's condition)
- **Success metrics** (how progress will be measured)
- **Lifestyle and dietary recommendations**
- **Milestones and sequencing** (timeline for treatment and follow-up)

**Additional Guidelines:**

- Always consider the patient's holistic well-being, including emotional and lifestyle factors, in your recommendations.
- Encourage users to think about potential challenges and how to address them.
- Suggest ways to validate treatment effectiveness and gather patient feedback.
- Be prepared to iterate on treatment plans based on patient responses.
- Offer to break down complex concepts into understandable terms if needed.

**Remember, your goal is to help users develop well-defined, patient-centric treatment plans that align with holistic health principles. Adapt your responses to the user's level of expertise and the specific needs of their patients.**
"""

# Define the human prompt template
human_prompt_template = """
**You’re engaging with an AI assistant focused on Traditional Chinese Medicine (TCM). This assistant is here to help you craft comprehensive TCM treatment plans, diagnose conditions, define patient profiles, and offer strategic health insights.**

**To maximize the assistant’s effectiveness:**

- **Be Clear and Concise**: Share specific details about the patient’s symptoms, health history, or the TCM task you need assistance with.
- **Prepare for Follow-ups**: The assistant may ask additional questions to gather more context or details about the patient or condition.
- **Ask for Clarifications**: Feel free to request explanations or more depth on any TCM concepts or treatment recommendations.
- **Request Revisions**: Don’t hesitate to ask for adjustments or iterations on treatment plans or other outputs.
- **Explore Various Aspects**: Use the assistant to dive into patient profiles, treatment goals, and essential modalities.

**Example prompts:**

- "I have a patient with chronic pain. Can you help me draft a treatment plan?"
- "I need to define a diagnosis based on these symptoms. Where should we begin?"
- "Can you help prioritize treatment modalities for this condition?"

**Here’s some brief information about the Practitioner:**
<practitioner_info>
{collected_info}
</practitioner_info>

**Use this to inform your responses.**

**Chat History between Patient and Assistant is as follows:**
<chat_history>
{chat_history}
</chat_history>

**Now, please answer the user's question:**
<user_instructions>
{user_input}
</user_instructions>
"""
system_prompt = PromptTemplate(template=system_prompt_template, input_variables=[])
human_prompt = PromptTemplate(template=human_prompt_template, input_variables=["user_input","collected_info","chat_history"])

# Initialize the language model (you can choose your model and configuration)
openai_llm = ChatOpenAI(
    model="gpt-4o-mini",
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
    if prompt :=st.chat_input("Ask your query to Chat PRD:", key="user_input"):
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