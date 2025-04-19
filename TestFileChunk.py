from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from uuid import uuid4

from langchain_core.documents import Document

# 构建一个文件数组，后期用来解析
pdf1 = './weifangfood.pdf'
pdf2 = './lutai.pdf'
pdfs = [pdf1,pdf2]
docs = []

# 解析pdf拆分文档
for pdf in pdfs:
    # 构建pdf loader
    loader = PyPDFLoader(pdf)
    # 添加到文档数组中，后面就处理这个
    docs.extend(loader.load())

# 对文档结果做切分，每一块切1000个字符，重叠大约200个，并且设置索引(做编号，标记这个切分结果来自于文档切分的哪一块)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,add_start_index=True)
split_text_list = text_splitter.split_documents(docs)

# 构建向量化组件
embed = OllamaEmbeddings(model="llama3.2:latest")


# 构建es向量存储器
elastic_vector_search = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="langchain_index",
    embedding=embed,
)

documents = []
for text in split_text_list:
    # 向量化，输出的就是向量结果
    # vector = embed.embed_query(text.page_content)
    # 对拆分的文本构建一个文档结构
    document = Document(
        page_content = text.page_content,
        metadata = text.metadata,
    )
    documents.append(document)

uuids = [str(uuid4()) for _ in range(len(documents))]
# 添加到es向量存储中
elastic_vector_search.add_documents(documents=documents, ids=uuids)
