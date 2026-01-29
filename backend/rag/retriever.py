"""Hybrid search retrieval - no LLM calls."""
from typing import List, Dict
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever


class KnowledgeRetriever:
    """Retrieve relevant documents using hybrid search."""

    def __init__(self, index: VectorStoreIndex):
        self.index = index
        self.retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=10  # Return top 10 most relevant chunks
        )

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search knowledge base.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of dicts with text, metadata, score
        """
        # Update retriever top_k if different
        if top_k != self.retriever.similarity_top_k:
            self.retriever = VectorIndexRetriever(
                index=self.index,
                similarity_top_k=top_k
            )

        # Retrieve nodes (NO LLM calls - just vector similarity)
        nodes = self.retriever.retrieve(query)

        # Format results
        results = []
        for node in nodes:
            results.append({
                "text": node.node.get_content(),
                "score": node.score,
                "metadata": {
                    "file_name": node.node.metadata.get("file_name", "unknown"),
                    "page": node.node.metadata.get("page_label", "N/A"),
                    "source": node.node.metadata.get("file_path", "unknown")
                }
            })

        return results

    def search_with_context(self, query: str, top_k: int = 5) -> Dict:
        """Search and return formatted context for Claude.ai.

        Returns:
            Dict with query, results, and citation-ready format
        """
        results = self.search(query, top_k)

        # Format for Claude.ai consumption
        context_blocks = []
        for i, result in enumerate(results, 1):
            context_blocks.append({
                "chunk_id": i,
                "text": result["text"],
                "source": f"{result['metadata']['file_name']}, p. {result['metadata']['page']}",
                "relevance_score": round(result["score"], 3)
            })

        return {
            "query": query,
            "num_results": len(results),
            "results": context_blocks,
            "citation_format": "Use format: [Source: {file_name}, p. {page}]"
        }
