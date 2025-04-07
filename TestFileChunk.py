from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from uuid import uuid4

from langchain_core.documents import Document

pdf1 = './baijie.pdf'
pdfs = [pdf1]
docs = []

# 解析pdf拆分文档
for pdf in pdfs:
    loader = PyPDFLoader(pdf)
    docs.extend(loader.load())

# print(len(docs))
# print(docs[2:3])

# 对文档结果做切分，每一块切1000个字符，重叠大约200个，并且设置索引(做编号，标记这个切分结果来自于文档切分的哪一块)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,add_start_index=True)
split_text_list = text_splitter.split_documents(docs)
# print(split_text_list[1])

# 向量化
embed = OllamaEmbeddings(model="llama3.2:latest")
# vector0 = embed.embed_query(split_text_list[0].page_content)
# vector1 = embed.embed_query(split_text_list[1].page_content)

# 存储es
elastic_vector_search = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="langchain_index",
    embedding=embed,
)

page = 1
documents = []
for text in split_text_list:
    # vector = embed.embed_query(text.page_content)
    print(text.page_content)
    print("**********************",page)
    print(text.metadata)

    document = Document(
        page_content = text.page_content,
        metadata = text.metadata,
    )
    documents.append(document)
    page += 1
    if page >= 100:
        break

uuids = [str(uuid4()) for _ in range(len(documents))]
elastic_vector_search.add_documents(documents=documents, ids=uuids)
