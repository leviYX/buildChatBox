from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ElasticsearchChatMessageHistory

from streamlit import streamlit as st

# load env file
load = load_dotenv("./.env")

 # 无密码的elasticsearch配置
es_url = "http://localhost:9200"
# 存储的索引，我们不用预先创建索引，因为说实话我也不知道字段，langchain会创建，并且自动映射字段
index_name = "chat_history"
# streamlit code
session_id = "levi"

# init llm
llm = ChatOllama(
    base_url = "http://127.0.0.1:11434",
    model = "huihui_ai/deepseek-r1-abliterated:14b",
    temperature = 0.5,
    num_predict = 10000
)
# 构建ElasticsearchChatMessageHistory
def get_session_history(session_id: str) :
    return ElasticsearchChatMessageHistory(
        index=index_name,
        session_id=session_id,
        es_url=es_url,
        ensure_ascii=False
    )


st.title("你好，这里是橘子GPT，我是小橘")
st.write("请把您的问题输入，小橘会认真回答的哦。")
# 设置一个输入框，用户输入的内容来替代默认的session_id。
session_id = st.text_input("请输入一个session_id,否则我们将使用默认值levi",session_id)
# 添加一个按钮，点击按钮的时候清空历史会话
isClickButton:bool = st.button("点击按钮，开启新的对话")
if isClickButton:
    # 注意这一行会去调用es客户端delete_by_query物理删除es中的上下文数据，最好自己定制，不要直接用
    get_session_history(session_id).clear()
    # 清除当前窗口的上下文记录
    st.session_state.chat_history = []

# query input
user_prompt = st.chat_input("我是小橘，请输入你的问题吧")

# 构建langchain执行
def invoke_history_by_stream(chain,prompt,session_id):
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key = prompt,
        history_messages_key="history",
    )
    responseStream = chain_with_history.stream({"prompt": prompt},config={"configurable": {"session_id": session_id}})
    for response in responseStream:
        yield response


# 如果没有就创建，不要每次都建立新的
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
# 遍历里面的内容，取出来存进去的每一组role 和 content
for message in st.session_state.chat_history :
    # 通过取出来的信息，构建st.chat_message，不同的角色会有不同的ui样式，这里就是做这个的
    with st.chat_message(message['role']):
        # 把内容展示出来
        st.markdown(message['content'])

template = ChatPromptTemplate.from_messages([
    ('human',"{prompt}"),
    ('placeholder',"{history}")
])
chain = template | llm | StrOutputParser()

# 如果感知到输入
if user_prompt :
    # 保存历史，上面用来遍历显示，避免后面覆盖前面的显示
    st.session_state.chat_history.append({'role':'user','content':user_prompt})
    with st.chat_message('user'):
        st.markdown(user_prompt)

    with st.chat_message('assistant'):
        streamResp = st.write_stream(invoke_history_by_stream(chain,user_prompt,session_id))
        # 保存历史，上面用来遍历显示，避免后面覆盖前面的显示
        st.session_state.chat_history.append({'role': 'assistant', 'content': streamResp})




