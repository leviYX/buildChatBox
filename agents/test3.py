from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool,
)
from langchain import hub
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent,AgentType
from dotenv import load_dotenv



# 实例化 Ollama 模型
llm = ChatOllama(
    base_url="http://127.0.0.1:11434",
    model="qwen:1.8b",
    temperature=0.5,
    num_predict=10000
)
# 实例化数据库连接
db = SQLDatabase.from_uri("mysql+pymysql://dba:dba*#2022@172.16.10.27:3306/a1")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()
print(tools)
#
# prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
#
# assert len(prompt_template.messages) == 1
# print(prompt_template.input_variables)
#
# system_message = prompt_template.format(dialect="SQLite", top_k=5)


# verbose表示详细输出处理过程
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

resp = agent.run('查询数据表数据表名字test_llm中的id=4的数据')
print("****************")
print(resp)
















