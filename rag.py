import os
from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from prompt import PROMPT, EXAMPLE_PROMPT

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Access keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Constants
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

llm = None
vector_store = None

def initialize_components():
    global llm, vector_store

    if GROQ_API_KEY is None:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set it in the .env file.")
    
    if llm is None:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500, api_key=GROQ_API_KEY)

    if HUGGINGFACEHUB_API_TOKEN is None:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable not set. Please set it in the .env file.")

    if vector_store is None:
        embedding_fun = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_fun,
            persist_directory=str(VECTORSTORE_DIR),
            client_settings=None  # optional
)


# Documnet Loading from URL and Vector Store Creation | Indexing (Loading, Splitting, Embedding, Storing)
def process_urls(urls):
    """
    This function scraps data from a url and stores it in a vector db
    :param urls: input urls
    :return:
    """
    yield "Initializing Components"
    initialize_components()

    yield "Resetting vector store...✅"
    try:
        vector_store._collection.drop()  # drops the collection if it exists
    except Exception:
        print("Collection does not exist yet, skipping drop step.")
        pass  # collection may not exist yet

    # step 1a: Indexing - Loading Data
    yield "Loading data...✅"
    loader = PlaywrightURLLoader(urls=urls, headless=True)
    data = loader.load()

    # step 1b: Indexing (Text Splitting)
    yield f"Splitting data into chunks of {CHUNK_SIZE}...✅"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        separators=["\n\n", "\n", ".", " "], 
        chunk_overlap=100
    )
    docs = text_splitter.split_documents(data)
 

    # step 1c & 1d - Indexing (Embedding Generation and Storing in Vector Store)
    yield f"Creating embeddings using {EMBEDDING_MODEL} model and adding to vector database...✅"
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)

    yield "All done! You can now ask questions related to the processed URLs. ✅"

# Querying the Vector Store and Generating Answers with Sources
def generate_answer(query):
    if not vector_store:
        raise RuntimeError("Vector database is not initialized. Please process URLs first.")    
    
   
    # step 2 and 3: Retrieval and Augmentation
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": PROMPT,
            "document_prompt": EXAMPLE_PROMPT
        },
        return_source_documents=True
    )
    
    # Step 4 - Generation
    result = chain.invoke({"query": query})
    sources_docs = [doc.metadata['source'] for doc in result.get('source_documents', [])]
    
    # Remove duplicates while preserving order
    unique_sources = list(dict.fromkeys(sources_docs))

    return result['result'], unique_sources

if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
    ]

    for _ in process_urls(urls):
        pass

    # Generate answer
    result, sources = generate_answer("Tell me what was the 30 year fixed mortagate rate along with the date?")
    print(f"Answer: {result}")
    print(f"Sources: {sources}")