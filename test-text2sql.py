from langchain.utilities import SQLDatabase
from langchain import hub
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Initialize database
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# Pull down prompt
prompt = hub.pull("rlm/text-to-sql")

llm = ChatOllama(
    base_url = "http://127.0.0.1:11434",
    model = "huihui_ai/deepseek-r1-abliterated:14b",
    temperature = 0.5,
    num_predict = 10000
)

# Create chain with LangChain Expression Language
inputs = {
    "table_info": lambda x: db.get_table_info(),
    "input": lambda x: x["question"],
    "few_shot_examples": lambda x: "",
    "dialect": lambda x: db.dialect,
}
sql_response = (
    inputs
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

# Call with a given question
sql_response.invoke({"question": "How many customers are there?"})
