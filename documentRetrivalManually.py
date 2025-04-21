from langchain_ollama import OllamaEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import Client

# 构建llm对象
llm = ChatOllama(
    base_url = "http://127.0.0.1:11434",
    model = "huihui_ai/deepseek-r1-abliterated:14b",
    temperature = 0.5,
    num_predict = 10000
)

# question问题
query = "请告诉我潍坊的美食有哪些?"
# 构建向量库检索
embed = OllamaEmbeddings(model="llama3.2:latest")
elastic_vector_search = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="langchain_index",
    embedding=embed,
)
# 检索器，执行相似度检索，k=1
retriever = elastic_vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k":1}
)
# 执行相似性检索，把与问题相关的文档全部获取
retrieved_docs = retriever.get_relevant_documents(query)
# 遍历获取的文档，组合成为上下文
context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

# 使用prompt hub来构建prompt，然后我们没有api-key，所以我们传入空
client = Client()
prompt = client.pull_prompt("rlm/rag-prompt", include_model=True)

# 构建chain
chain = prompt | llm | StrOutputParser()
# 执行问答
response = chain.invoke({"context":context_text,"question":query})
print(response)

