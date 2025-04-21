from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import ChatOllama

llm = ChatOllama(
    base_url = "http://127.0.0.1:11434",
    model = "huihui_ai/deepseek-r1-abliterated:14b",
    temperature = 0.5,
    num_predict = 10000
)

embed = OllamaEmbeddings(model="llama3.2:latest")
elastic_vector_search = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="langchain_index",
    embedding=embed,
)
retriever = elastic_vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k":1}
)

# 构建检索，并且制定return_source_documents为true，因为我们要获取元信息，里面有文档来源
qa_chain = RetrievalQA.from_chain_type(llm,retriever=retriever,return_source_documents=True)
response = qa_chain.invoke("请告诉我潍坊的美食有哪些?")
# 遍历结果集，封装为set集合，去重
sources = set(doc.metadata.get("source","Unknown") for doc in response["source_documents"])
print(response['result'])
print("\n 引用来源:")
for source in sources:
    print(f"{source}")


