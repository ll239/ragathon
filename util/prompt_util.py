from llama_index import SimpleDirectoryReader, StorageContext, \
    VectorStoreIndex
import os
from llama_index.vector_stores import AstraDBVectorStore


def summarize(text_content, idx):
    upload_dir = "data"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, str(idx) + '.txt')
    print(file_path)

    with open(file_path, "w") as f:
        f.write(text_content)
    document = SimpleDirectoryReader(input_files=[file_path]).load_data()
    storage_context = StorageContext.from_defaults(persist_dir='./storage')

    index = VectorStoreIndex.from_documents(
        document, storage_context=storage_context
    )

    index.storage_context.persist()
    query_engine = index.as_query_engine()
    summary = query_engine.query(f"Summarize the content  in 100 words")
    theme = get_theme(index)
    trigger = get_trigger(index)
    return summary, theme, trigger


def check_db(url):
    astra_db_store = AstraDBVectorStore(
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        collection_name="search_engine_db",
        embedding_dimension=1536,
    )
    index = VectorStoreIndex.from_vector_store(vector_store=astra_db_store)
    query_engine = index.as_query_engine()
    summary = query_engine.query(f"Return value at summary of id= {url} if id exists else return None")
    theme = query_engine.query(f"Return value at theme of id= {url} if id exists else return None")
    trigger = query_engine.query(f"Return value at trigger of id= {url} if id exists else return None")
    return summary, theme, trigger


def insert_db(text_content, idx, url):
    upload_dir = "data"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, str(idx) + '.txt')
    print(file_path)
    summary, theme, trigger = summarize(text_content, idx)
    with open(file_path, "w") as f:
        f.write(text_content)
    document = SimpleDirectoryReader(input_files=[file_path]).load_data()
    document[0].metadata = {"id": url, "summary": str(summary), "theme": str(theme), "trigger": str(trigger)}
    astra_db_store = AstraDBVectorStore(
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        collection_name="search_engine_db",
        embedding_dimension=1536,
    )
    storage_context = StorageContext.from_defaults(vector_store=astra_db_store)
    index = VectorStoreIndex.from_documents(
        document, storage_context=storage_context
    )

    index.storage_context.persist()
    summary, theme, trigger = summarize(text_content, idx)
    return summary, theme, trigger


def get_summary(index, url):
    query_engine = index.as_query_engine()
    summary = query_engine.query(f"Summarize the doc stored in db in 100 words for metadata URL: {url} .")
    return summary


def get_theme(index):
    query_engine = index.as_query_engine()
    theme = query_engine.query(f"Give  me appropriate one word topic that categorizes the content.")
    return theme


def get_trigger(index):
    query_engine = index.as_query_engine()
    trigger = query_engine.query(
        f"Predict if the content  has any negative or sensitive or depressing content that can affect reader and "
        f"provide a warning")
    return trigger


def insert_trigger():
    document = SimpleDirectoryReader(
        input_files=['/data/trigger/An-Introduction-to-Content-Warnings-and-Trigger-Warnings-Draft.pdf']).load_data()
    document[0].metadata = {"id": 0, "file_name": "trigger.pdf"}

    astra_db_store = AstraDBVectorStore(
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        collection_name="search_engine_db",
        embedding_dimension=1536,
    )

    storage_context = StorageContext.from_defaults(vector_store=astra_db_store)

    index = VectorStoreIndex.from_documents(
        document, storage_context=storage_context
    )

    index.storage_context.persist()
