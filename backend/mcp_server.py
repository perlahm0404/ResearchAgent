#!/usr/bin/env python3
"""
MCP Server for Personal Knowledge Platform
Exposes 9 tools to Claude.ai for research, search, and content generation.
"""
import os
import sys
import asyncio
import json
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp import types

# Import local modules
from rag.indexer import DocumentIndexer
from rag.retriever import KnowledgeRetriever
from web.search import WebSearcher
from seo.analyzer import SEOAnalyzer

# Initialize components
DB_URL = os.getenv("DATABASE_URL", "postgresql://kb_user:kb_pass@localhost:5432/knowledge_base")
DOCUMENTS_DIR = os.getenv("DOCUMENTS_DIR", "../data/documents")
STORAGE_DIR = os.getenv("STORAGE_DIR", "../data/storage")

# Global state
indexer = None
retriever = None
web_searcher = None
seo_analyzer = None


def initialize_components():
    """Initialize RAG and search components."""
    global indexer, retriever, web_searcher, seo_analyzer

    try:
        # Initialize indexer
        indexer = DocumentIndexer(DB_URL, STORAGE_DIR)

        # Try to load existing index
        try:
            index = indexer.get_index()
            retriever = KnowledgeRetriever(index)
        except Exception:
            # No index yet - will be created on first upload
            retriever = None

        # Initialize web search
        web_searcher = WebSearcher()

        # Initialize SEO analyzer
        seo_analyzer = SEOAnalyzer()

        return True
    except Exception as e:
        print(f"Initialization error: {e}", file=sys.stderr)
        return False


# Create MCP server
app = Server("personal-knowledge")


@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available tools."""
    return [
        types.Tool(
            name="search_knowledge_base",
            description="Search your personal knowledge base (documents, notes, PDFs). Returns relevant excerpts with citations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "top_k": {
                        "type": "number",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="web_search",
            description="Search the web for fresh, up-to-date information. Returns titles, URLs, and snippets.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "num_results": {
                        "type": "number",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="upload_document",
            description="Upload a new document (PDF, DOCX, TXT, MD) to the knowledge base and index it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Full path to document file"
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="generate_seo_outline",
            description="Generate SEO-optimized content outline with heading structure, keyword placement, and checklist.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Main topic for the article"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional target keywords"
                    }
                },
                "required": ["topic"]
            }
        ),
        types.Tool(
            name="generate_aeo_snippets",
            description="Generate Answer Engine Optimization snippets for AI assistants, voice search, and featured snippets.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Main topic"
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional context from knowledge base"
                    }
                },
                "required": ["topic"]
            }
        ),
        types.Tool(
            name="extract_keywords",
            description="Extract SEO keywords from text using KeyBERT.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to extract keywords from"
                    },
                    "top_n": {
                        "type": "number",
                        "description": "Number of keywords to extract (default: 10)",
                        "default": 10
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="analyze_content_seo",
            description="Analyze content for SEO quality (keyword density, structure, readability).",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Content to analyze"
                    },
                    "target_keyword": {
                        "type": "string",
                        "description": "Primary keyword to check"
                    }
                },
                "required": ["content", "target_keyword"]
            }
        ),
        types.Tool(
            name="reindex_documents",
            description="Rebuild the knowledge base index from all documents in the documents directory.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="list_indexed_documents",
            description="List all documents currently in the knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool execution."""
    global indexer, retriever, web_searcher, seo_analyzer

    # Ensure components are initialized
    if indexer is None:
        initialize_components()

    try:
        if name == "search_knowledge_base":
            if retriever is None:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "No documents indexed yet. Use upload_document or reindex_documents first."
                    })
                )]

            query = arguments.get("query", "")
            top_k = arguments.get("top_k", 5)

            result = retriever.search_with_context(query, top_k)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "web_search":
            query = arguments.get("query", "")
            num_results = arguments.get("num_results", 5)

            result = await web_searcher.search_with_context(query, num_results)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "upload_document":
            file_path = arguments.get("file_path", "")

            # Copy file to documents directory if not already there
            src_path = Path(file_path)
            if not src_path.exists():
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": f"File not found: {file_path}"})
                )]

            docs_dir = Path(DOCUMENTS_DIR)
            docs_dir.mkdir(parents=True, exist_ok=True)

            # Copy to documents directory
            import shutil
            dest_path = docs_dir / src_path.name
            shutil.copy2(src_path, dest_path)

            # Index the document
            result = indexer.add_document(str(dest_path))

            # Update retriever with new index
            if result.get("status") == "success":
                index = indexer.get_index()
                retriever = KnowledgeRetriever(index)

            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "generate_seo_outline":
            topic = arguments.get("topic", "")
            keywords = arguments.get("keywords", [])

            result = seo_analyzer.generate_seo_outline(topic, keywords)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "generate_aeo_snippets":
            topic = arguments.get("topic", "")
            context = arguments.get("context", "")

            result = seo_analyzer.generate_aeo_snippets(topic, context)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "extract_keywords":
            text = arguments.get("text", "")
            top_n = arguments.get("top_n", 10)

            result = seo_analyzer.extract_keywords(text, top_n)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "analyze_content_seo":
            content = arguments.get("content", "")
            target_keyword = arguments.get("target_keyword", "")

            result = seo_analyzer.analyze_content_seo(content, target_keyword)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "reindex_documents":
            result = indexer.index_documents(DOCUMENTS_DIR)

            # Update retriever with new index
            if result.get("status") == "success" or result.get("indexed", 0) > 0:
                index = indexer.get_index()
                retriever = KnowledgeRetriever(index)

            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "list_indexed_documents":
            # This is a placeholder - would need to track indexed docs in DB
            docs_path = Path(DOCUMENTS_DIR)
            if docs_path.exists():
                files = [f.name for f in docs_path.rglob("*") if f.is_file()]
                result = {"documents": files, "count": len(files)}
            else:
                result = {"documents": [], "count": 0}

            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"})
            )]

    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": str(e)})
        )]


async def main():
    """Run MCP server."""
    # Initialize components on startup
    print("Initializing Personal Knowledge Platform MCP Server...", file=sys.stderr)
    success = initialize_components()

    if not success:
        print("Warning: Some components failed to initialize. Some features may not work.", file=sys.stderr)

    print("MCP Server ready!", file=sys.stderr)

    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="personal-knowledge",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
