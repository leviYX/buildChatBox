from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_ollama import ChatOllama

# 实例化 Ollama 模型
llm = ChatOllama(
    base_url="http://127.0.0.1:11434",
    model="qwen:1.8b",
    temperature=0.5,
    num_predict=10000
)
# 实例化数据库连接
db = SQLDatabase.from_uri("mysql+pymysql://dba:dba*#2022@172.16.10.27:3306/a1")
chain = create_sql_query_chain(llm=llm, db=db)
response = chain.invoke({"question": "查询数据表数据表名字test_llm中的id=4的数据"})
print("Chain执行结果：" + response)
# 删除response无用部分
sql = response.replace("sql: ", "").replace("```sql", "").replace("```", "")
print("自然语言转SQL：" + sql)
res = db.run(sql)
print("查询结果：", res)
