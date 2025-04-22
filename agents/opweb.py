

from langchain_ollama import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import create_sql_agent



llm = ChatOllama(base_url="http://127.0.0.1:11434", model="qwen:1.8b", temperature=0.5,num_predict=10000)
db = SQLDatabase.from_uri("mysql+pymysql://dba:dba*#2022@172.16.10.27:3306/a1")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# 创建 Agent
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    use_query_checker=True  # 确保 Agent 会检查并执行查询
)

# 使用 Agent 执行查询
example_query = "显示数据库名字为a1下面的数据表名字为test_llm中的id=4的数据"
query_tool = toolkit.get_tools()[0]  # 获取 QuerySQLDatabaseTool

sql_query = "SELECT * FROM a1.test_llm WHERE id = 4"
result = query_tool.run(tool_input=sql_query)


# result = agent_executor.run(sql_query)
print("***************")
print(result)


# # 获取工具
# list_tool = toolkit.get_tools()[2]  # 获取 ListSQLDatabaseTool
#
# # 调用工具
# tables = list_tool.run(tool_input={})  # 提供空字典作为输入
# print(tables)
# query_tool = toolkit.get_tools()[0]  # 获取 QuerySQLDatabaseTool
#
# # 获取第一个表名
# first_table_name = tables[0]
# # 构造 SQL 查询字符串
# query = f"SELECT * FROM {first_table_name} LIMIT 10"
# result = query_tool.run(tool_input=query)
# print(result)