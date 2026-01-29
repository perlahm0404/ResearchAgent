"""Document indexing without LLM calls."""
import os
from pathlib import Path
from typing import List
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url
from .embeddings import setup_embeddings, get_embedding_dimension


class DocumentIndexer:
    """Index documents into pgvector using local embeddings."""

    def __init__(self, db_url: str, storage_dir: str):
        self.db_url = db_url
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Setup local embeddings
        setup_embeddings()

        # Setup vector store
        self.vector_store = PGVectorStore.from_params(
            database=make_url(db_url).database,
            host=make_url(db_url).host,
            password=make_url(db_url).password,
            port=make_url(db_url).port,
            user=make_url(db_url).username,
            table_name="knowledge_embeddings",
            embed_dim=get_embedding_dimension()
        )

        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        self.index = None

    def index_documents(self, documents_dir: str) -> dict:
        """Index all documents in directory.

        Returns:
            dict with indexed file count and status
        """
        docs_path = Path(documents_dir)

        if not docs_path.exists():
            return {"error": "Documents directory not found", "indexed": 0}

        # Load documents (supports PDF, DOCX, TXT, MD)
        reader = SimpleDirectoryReader(
            input_dir=str(docs_path),
            recursive=True,
            required_exts=[".pdf", ".txt", ".md", ".docx"]
        )

        documents = reader.load_data()

        if not documents:
            return {"error": "No documents found", "indexed": 0}

        # Create index (embeddings computed locally, NO LLM calls)
        self.index = VectorStoreIndex.from_documents(
            documents,
            storage_context=self.storage_context,
            show_progress=True
        )

        return {
            "indexed": len(documents),
            "status": "success",
            "files": [doc.metadata.get("file_name", "unknown") for doc in documents]
        }

    def add_document(self, file_path: str) -> dict:
        """Add single document to index.

        Args:
            file_path: Path to document file

        Returns:
            dict with status
        """
        if not Path(file_path).exists():
            return {"error": "File not found", "status": "failed"}

        # Load single document
        reader = SimpleDirectoryReader(input_files=[file_path])
        documents = reader.load_data()

        if not documents:
            return {"error": "Could not read document", "status": "failed"}

        # Add to existing index or create new
        if self.index is None:
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=self.storage_context
            )
        else:
            for doc in documents:
                self.index.insert(doc)

        return {
            "status": "success",
            "file": Path(file_path).name,
            "indexed": len(documents)
        }

    def get_index(self):
        """Get or load existing index."""
        if self.index is None:
            # Try to load from vector store
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                storage_context=self.storage_context
            )
        return self.index
