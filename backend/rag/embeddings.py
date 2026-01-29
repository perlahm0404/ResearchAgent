"""Local embedding model setup - no LLM API calls."""
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings


def setup_embeddings():
    """Configure local embedding model (no API costs)."""
    model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    device = os.getenv("EMBEDDING_DEVICE", "cpu")

    embed_model = HuggingFaceEmbedding(
        model_name=model_name,
        device=device
    )

    # CRITICAL: Do NOT set Settings.llm
    # Claude.ai is the LLM - local backend only does retrieval
    Settings.embed_model = embed_model

    return embed_model


def get_embedding_dimension():
    """Get embedding dimension for vector store setup."""
    # BGE-small-en-v1.5 uses 384 dimensions
    return 384
