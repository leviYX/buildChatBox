from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_elasticsearch import ElasticsearchStore
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage


model_name = "llama3.2"
load = load_dotenv("./.env")
llm = ChatOllama(base_url = "http://127.0.0.1:11434",model = model_name,temperature = 1.0,num_predict = 10000)

# tools
db = SQLDatabase.from_uri("mysql+pymysql://dba:dba*#2022@172.16.10.27:3306/llm")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# 构建向量化组件
embed = OllamaEmbeddings(model=model_name)
# 存储es
elastic_vector_search = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="langchain_index",
    embedding=embed,
)

retriever = elastic_vector_search.as_retriever(
    search_type="mmr",
    search_kwargs={"k":100}
)

@tool
def check_food(query:str) -> str:
    """
    你必须使用这个tool，根据传入的参数query来回答问题
    """
    return retriever.invoke(query)

# 把我们自己的tool添加到tools数组中，此时就等于把rag做成了tool，加入到了我们的目标调用中
tools.append(check_food)

# agent
memory = MemorySaver()
print("**********************打印一下现在的tool")
print(tools)
agent_executor = create_react_agent(llm, tools, checkpointer=memory)
# 用户问题
config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="潍坊市有哪些美食")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()









