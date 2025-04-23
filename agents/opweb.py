from langchain_ollama import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# 加载langsmith，因为下面的create_react_agent操作要推送监控，这里不加载会报错，
load = load_dotenv("./.env")
# 构建llm对象
llm = ChatOllama(base_url = "http://127.0.0.1:11434",model = "llama3.2",temperature = 0.5,num_predict = 10000)
# 构建数据库连接，这个连接mysql的url我在官网没找到，是在一个博客看到的
db = SQLDatabase.from_uri("mysql+pymysql://dba:dba*#2022@172.16.10.27:3306/a1")
# 构建SQLDatabaseToolkit对象，绑定llm和db，形成tools
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
print(toolkit.get_tools())

# 从prompt_hub拉取一个sql类型操作的prompt模板
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
# 填充模板
system_message = prompt_template.format(dialect="SQLite", top_k=5)
# 构建agent对象
agent_executor = create_react_agent(llm, toolkit.get_tools(), prompt=system_message)

# 用户问题
question = "查询数据表数据表名字test_llm中的id=4的数据,以表格的形式输出"

# stream方式执行agent
events = agent_executor.stream(
    {"messages": [("user", question)]},
    stream_mode="values",
)
# 输出结果
for event in events:
    event["messages"][-1].pretty_print()