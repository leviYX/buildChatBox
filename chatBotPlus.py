from dotenv import load_dotenv
from langchain_community.chat_message_histories import ElasticsearchChatMessageHistory
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate

from streamlit import streamlit as st

load = load_dotenv("./.env")
es_url = "http://localhost:9200"
index_name = "chat_history"
def get_session_history(session_id: str) :
    return ElasticsearchChatMessageHistory(index=index_name,session_id=session_id,es_url=es_url,ensure_ascii=False)
# init llm
llm = ChatOllama(
    base_url = "http://127.0.0.1:11434",
    model = "huihui_ai/deepseek-r1-abliterated:14b",
    temperature = 0.5,
    num_predict = 10000
)

user_id = "levi"

with st.sidebar:
    st.image("./orange.png", width=150)
    user_id = st.text_input("输入你的id", user_id)
    role = st.radio("你想获得什么级别的回答呢?", ["初学者", "专家", "大佬"], index=0)
    if st.button("清空历史上下文，开启新的对话"):
        st.session_state.chat_history = []
        get_session_history(user_id).clear()
        
st.markdown(
    """
    <div style='display: flex; height: 70vh; justify-content: center; align-items: center;'>
        <h2>请问你需要什么帮助呢?</h2>
    </div>
    """,
    unsafe_allow_html=True
)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
       st.markdown(message['content'])

template = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ('system', f"你作为一个 {role} 级别的人来回答这个问题"),
    ('human', "{prompt}")
])

chain = template | llm | StrOutputParser()

def invoke_history(chain, session_id, prompt):
    history = RunnableWithMessageHistory(chain, 
                                         get_session_history,
                                         input_messages_key="prompt",
                                         history_messages_key="history")
    
    for response in history.stream({"prompt": prompt},config={"configurable": {"session_id": session_id}}):
        yield response

prompt = st.chat_input("输入你的问题，小橘会为你回答。")

if prompt:
    st.session_state.chat_history.append({'role': 'user', "content": prompt})

    with st.chat_message('user'):
        st.markdown(prompt)
    
    with st.chat_message('assistant'):
        streamResponse = st.write_stream(invoke_history(chain, user_id, prompt))

    st.session_state.chat_history.append({'role': 'assistant', "content": streamResponse})
