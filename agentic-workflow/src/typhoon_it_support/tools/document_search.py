"""Document search tools for IT policies and troubleshooting guides."""

import os
from pathlib import Path
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

# Initialize paths
DOCUMENTS_DIR = Path(__file__).parent.parent.parent.parent / "documents"
VECTOR_STORE_PATH = Path(__file__).parent.parent.parent.parent / "vector_store"

# Global vector store instance
_vector_store = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    """Get HuggingFace embeddings model.
    
    Returns:
        HuggingFaceEmbeddings instance.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def _get_vector_store() -> FAISS:
    """Get or create the vector store for documents.
    
    Returns:
        FAISS vector store instance.
    """
    global _vector_store
    
    if _vector_store is not None:
        return _vector_store
    
    # Check if vector store exists
    if VECTOR_STORE_PATH.exists():
        embeddings = _get_embeddings()
        _vector_store = FAISS.load_local(
            str(VECTOR_STORE_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )
        return _vector_store
    
    # Create new vector store
    return _initialize_vector_store()


def _initialize_vector_store() -> FAISS:
    """Initialize vector store from documents.
    
    Returns:
        Newly created FAISS vector store.
    """
    global _vector_store
    
    # Load documents
    loader = DirectoryLoader(
        str(DOCUMENTS_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings
    embeddings = _get_embeddings()
    
    # Create vector store
    _vector_store = FAISS.from_documents(splits, embeddings)
    
    # Save for future use
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
    _vector_store.save_local(str(VECTOR_STORE_PATH))
    
    return _vector_store


@tool
def search_it_policy(query: str) -> str:
    """Search IT policy documents for relevant information.
    
    Use this tool to find information about:
    - Password policies and requirements
    - VPN access procedures
    - Email policies and quotas
    - Software installation guidelines
    - Device management rules
    - Network access procedures
    - Data security policies
    - Incident reporting procedures
    
    Args:
        query: The search query describing what policy information is needed.
    
    Returns:
        Relevant policy information from the documents.
    """
    vector_store = _get_vector_store()
    
    # Search for relevant documents
    docs = vector_store.similarity_search(
        query,
        k=3,
        filter=lambda metadata: "it_policy" in metadata.get("source", "")
    )
    
    if not docs:
        # Fallback: search without filter
        docs = vector_store.similarity_search(query, k=3)
    
    if not docs:
        return "No relevant policy information found. Please rephrase your query or contact IT helpdesk for specific policy questions."
    
    # Format results
    results = []
    for i, doc in enumerate(docs, 1):
        source = Path(doc.metadata.get("source", "Unknown")).name
        results.append(f"**Source {i}: {source}**\n{doc.page_content}\n")
    
    return "\n---\n".join(results)


@tool
def search_troubleshooting_guide(query: str) -> str:
    """Search troubleshooting guides for solutions to technical problems.
    
    Use this tool to find solutions for:
    - Login issues
    - Slow computer performance
    - Internet/network connectivity problems
    - Shared drive access issues
    - Email problems (sending, receiving, Outlook issues)
    - Printer issues
    - Software crashes or won't open
    - Video conferencing problems (Zoom, Teams, camera, microphone)
    
    Args:
        query: Description of the technical problem to troubleshoot.
    
    Returns:
        Step-by-step troubleshooting instructions and solutions.
    """
    vector_store = _get_vector_store()
    
    # Search for relevant documents
    docs = vector_store.similarity_search(
        query,
        k=3,
        filter=lambda metadata: "troubleshooting" in metadata.get("source", "")
    )
    
    if not docs:
        # Fallback: search without filter
        docs = vector_store.similarity_search(query, k=3)
    
    if not docs:
        return "No relevant troubleshooting information found. Please provide more details about the issue or contact IT helpdesk for assistance."
    
    # Format results
    results = []
    for i, doc in enumerate(docs, 1):
        source = Path(doc.metadata.get("source", "Unknown")).name
        results.append(f"**Troubleshooting Step {i}** (from {source}):\n{doc.page_content}\n")
    
    return "\n---\n".join(results)


@tool
def search_all_documents(query: str) -> str:
    """Search across all IT documentation including policies and troubleshooting guides.
    
    Use this tool when you need to search broadly across all documentation,
    or when you're not sure if the information is in policy or troubleshooting docs.
    
    Args:
        query: The search query.
    
    Returns:
        Relevant information from all IT documents.
    """
    vector_store = _get_vector_store()
    
    # Search for relevant documents
    docs = vector_store.similarity_search(query, k=4)
    
    if not docs:
        return "No relevant information found in IT documentation. Please contact IT helpdesk for assistance."
    
    # Format results
    results = []
    for i, doc in enumerate(docs, 1):
        source = Path(doc.metadata.get("source", "Unknown")).name
        results.append(f"**Result {i}** (from {source}):\n{doc.page_content}\n")
    
    return "\n---\n".join(results)


def rebuild_vector_store() -> str:
    """Rebuild the vector store from scratch.
    
    Call this function when documents are updated.
    
    Returns:
        Status message.
    """
    global _vector_store
    _vector_store = None
    
    # Remove existing vector store
    if VECTOR_STORE_PATH.exists():
        import shutil
        shutil.rmtree(VECTOR_STORE_PATH)
    
    # Rebuild
    _initialize_vector_store()
    return "Vector store rebuilt successfully"

