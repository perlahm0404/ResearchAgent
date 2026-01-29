# Personal Knowledge Platform

A personal research and knowledge management system powered by **Claude.ai + MCP + LlamaIndex**.

## Features

- **Perplexity-style search** - Search your docs AND the web with citations
- **NotebookLM-style summaries** - Multi-doc synthesis and podcast scripts
- **SEO/AEO content generation** - Optimized outlines and snippets
- **$0/month LLM costs** - Uses your existing Claude.ai subscription
- **100% local & private** - All data stays on your Mac

## Architecture

```
Claude.ai (You) ← MCP Protocol → Local Backend (LlamaIndex + FastAPI)
                                        ↓
                                  PostgreSQL + pgvector
```

**Key Insight**: Local backend is "dumb" (search/index only). Claude.ai is the intelligent layer.

## Quick Start

### 1. Start PostgreSQL

```bash
docker-compose up -d
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Upload Documents

```bash
# Copy your PDFs, notes, etc. to:
cp ~/Documents/*.pdf data/documents/
```

### 4. Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "personal-knowledge": {
      "command": "python",
      "args": [
        "/Users/YOUR_USERNAME/personal-knowledge-platform/backend/mcp_server.py"
      ],
      "env": {
        "SEARXNG_URL": "https://searx.be"
      }
    }
  }
}
```

**Replace `YOUR_USERNAME` with your actual username!**

### 5. Restart Claude Desktop

Quit and restart Claude Desktop app.

### 6. Test

Ask me in Claude.ai:
- "What tools do you have?" (should list 9 tools)
- "Upload this document: /path/to/file.pdf"
- "Search my knowledge base for X"
- "Search the web for Y and cite sources"

## Available Tools (9)

| Tool | Purpose |
|------|---------|
| `search_knowledge_base` | RAG search your documents |
| `web_search` | Search web (SearxNG/Tavily) |
| `upload_document` | Add new documents |
| `generate_seo_outline` | SEO content structure |
| `generate_aeo_snippets` | Answer Engine Optimization |
| `extract_keywords` | SEO keyword extraction |
| `analyze_content_seo` | Content quality analysis |
| `reindex_documents` | Rebuild search index |
| `list_indexed_documents` | Show indexed files |

## Usage Examples

### Example 1: Research with Citations

**You**: "What are the benefits of intermittent fasting? Search my docs and web."

**I do automatically**:
1. Call `search_knowledge_base(query="intermittent fasting")`
2. Call `web_search(query="intermittent fasting 2026")`
3. Synthesize with citations

**I respond**: Cited answer with sources from your docs + web.

### Example 2: SEO Article

**You**: "Write SEO article about 'Personal Knowledge Management' using my notes."

**I do automatically**:
1. `generate_seo_outline(topic="Personal Knowledge Management")`
2. `search_knowledge_base(query="knowledge management")`
3. `web_search(query="PKM best practices 2026")`
4. Write 2000-word optimized article

### Example 3: Multi-Doc Summary

**You**: "Summarize my 5 research papers as a podcast script."

**I do automatically**:
1. `search_knowledge_base()` for each paper
2. Synthesize into conversational dialogue

## Configuration

### Environment Variables

Edit `.env` file:

```bash
# Database
DATABASE_URL=postgresql://kb_user:kb_pass@localhost:5432/knowledge_base

# Web Search (choose one)
SEARXNG_URL=https://searx.be
# TAVILY_API_KEY=your_key_here  # Optional premium search ($29/mo)

# Storage
DOCUMENTS_DIR=../data/documents
STORAGE_DIR=../data/storage

# Embedding Model (local, no API costs)
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
EMBEDDING_DEVICE=cpu
```

### Supported Document Types

- PDF (`.pdf`)
- Word (`.docx`)
- Text (`.txt`)
- Markdown (`.md`)

## Cost Analysis

| Component | Monthly Cost |
|-----------|-------------|
| LLM (Claude.ai) | $0 (existing subscription) |
| Embeddings (local) | $0 |
| Web Search (SearxNG) | $0 |
| Web Search (Tavily - optional) | $29 |
| Infrastructure (Mac) | $0 |
| **Total** | **$0-29/mo** |

**vs. Commercial Alternatives**:
- Perplexity Pro: $20/mo
- NotebookLM Plus: $20/mo (future)
- API costs: $50-200/mo
- **This solution**: $0/mo

## Troubleshooting

### "No documents indexed yet"

```bash
# Manually reindex
cd backend
python -c "
from mcp_server import initialize_components, indexer
initialize_components()
result = indexer.index_documents('../data/documents')
print(result)
"
```

Or ask me in Claude.ai: "Reindex all documents"

### "Module not found"

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### PostgreSQL not running

```bash
docker-compose up -d
docker ps  # Verify container is running
```

### MCP server not visible in Claude Desktop

1. Check config file path: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Verify Python path in config is correct
3. Restart Claude Desktop (fully quit and reopen)
4. Check MCP server logs in Claude Desktop developer tools

## Development

### Run MCP Server Manually (for debugging)

```bash
cd backend
python mcp_server.py
```

### Test Components Directly

```python
# Test indexer
from rag.indexer import DocumentIndexer
indexer = DocumentIndexer(
    "postgresql://kb_user:kb_pass@localhost:5432/knowledge_base",
    "../data/storage"
)
result = indexer.index_documents("../data/documents")
print(result)

# Test retriever
from rag.retriever import KnowledgeRetriever
retriever = KnowledgeRetriever(indexer.get_index())
results = retriever.search("your query")
print(results)

# Test web search
import asyncio
from web.search import WebSearcher
searcher = WebSearcher()
results = asyncio.run(searcher.search("test query"))
print(results)
```

## Roadmap

- [ ] Add support for more document types (EPUB, HTML)
- [ ] Implement conversation history tracking
- [ ] Add automated web scraping
- [ ] Build citation graph visualization
- [ ] Add notebook export (Obsidian, Notion)
- [ ] Multi-language support
- [ ] Audio/video transcription integration

## Architecture Details

### Why No LLM in Local Backend?

**Critical Design Decision**: The local backend uses LlamaIndex WITHOUT any LLM configured.

```python
from llama_index.core import Settings
Settings.embed_model = HuggingFaceEmbedding(...)
# Settings.llm is NEVER set - Claude.ai is the LLM
```

**Why**:
- Avoids API costs (embeddings are local)
- Claude.ai (via MCP) does all reasoning/generation
- Backend only does retrieval/search/indexing
- Keeps architecture simple and cost-effective

### Data Flow

1. **User** asks question in Claude.ai
2. **Claude.ai** calls MCP tool (e.g., `search_knowledge_base()`)
3. **MCP Server** receives request via stdio
4. **Backend** executes search (vector similarity, no LLM)
5. **Results** returned to Claude.ai as JSON
6. **Claude.ai** synthesizes answer with citations
7. **User** gets intelligent response

## License

MIT

## Support

For issues or questions, open a GitHub issue or check the documentation.
