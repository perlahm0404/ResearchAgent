# Testing Guide

Complete testing workflow to verify your Personal Knowledge Platform is working.

## Pre-Flight Checklist

Before running tests, ensure:

- [ ] Docker Desktop is running
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] PostgreSQL container running (`docker-compose up -d`)
- [ ] At least one test document in `data/documents/`
- [ ] Claude Desktop installed and running

## Test Sequence

### Test 1: PostgreSQL Connection

```bash
# Verify PostgreSQL is running
docker ps | grep knowledge-postgres

# Test connection
docker exec knowledge-postgres psql -U kb_user -d knowledge_base -c "SELECT 1;"

# Should output: "1" (row)
```

**Expected**: Connection successful, returns 1.

---

### Test 2: Local Embeddings

```bash
cd backend
python -c "
from rag.embeddings import setup_embeddings
embed_model = setup_embeddings()
test_text = ['This is a test sentence']
embeddings = embed_model.get_text_embedding_batch(test_text)
print(f'Embedding dimension: {len(embeddings[0])}')
print('✓ Embeddings working')
"
```

**Expected**: `Embedding dimension: 384`

---

### Test 3: Document Indexing

```bash
# Create test document
cat > ../data/documents/test.txt <<EOF
Personal Knowledge Management

Personal Knowledge Management (PKM) is a process of collecting information that a person uses to gather, classify, store, search, retrieve and share knowledge in their daily activities.

Key Benefits:
1. Better information retention
2. Faster retrieval of relevant information
3. Improved decision making
4. Enhanced creativity through connection discovery

Best Practices:
- Use consistent tagging systems
- Regular review and curation
- Link related concepts
- Export and backup regularly
EOF

# Index the document
python -c "
from rag.indexer import DocumentIndexer
import os

db_url = os.getenv('DATABASE_URL', 'postgresql://kb_user:kb_pass@localhost:5432/knowledge_base')
indexer = DocumentIndexer(db_url, '../data/storage')
result = indexer.index_documents('../data/documents')
print(result)
"
```

**Expected**: `{"indexed": 1, "status": "success", "files": ["test.txt"]}`

---

### Test 4: Search Retrieval

```bash
python -c "
from rag.indexer import DocumentIndexer
from rag.retriever import KnowledgeRetriever
import os
import json

db_url = os.getenv('DATABASE_URL', 'postgresql://kb_user:kb_pass@localhost:5432/knowledge_base')
indexer = DocumentIndexer(db_url, '../data/storage')
index = indexer.get_index()
retriever = KnowledgeRetriever(index)

results = retriever.search_with_context('benefits of knowledge management')
print(json.dumps(results, indent=2))
"
```

**Expected**: Returns JSON with relevant chunks from test.txt, citing "test.txt" as source.

---

### Test 5: Web Search

```bash
python -c "
import asyncio
from web.search import WebSearcher
import json

async def test():
    searcher = WebSearcher()
    results = await searcher.search_with_context('Python programming 2026', 3)
    print(json.dumps(results, indent=2))

asyncio.run(test())
"
```

**Expected**: Returns 3 web search results with titles, URLs, snippets.

---

### Test 6: SEO Tools

```bash
python -c "
from seo.analyzer import SEOAnalyzer
import json

analyzer = SEOAnalyzer()

# Test keyword extraction
keywords = analyzer.extract_keywords('Personal knowledge management helps organize information and improve productivity')
print('Keywords:', keywords)

# Test SEO outline
outline = analyzer.generate_seo_outline('Personal Knowledge Management')
print(json.dumps(outline, indent=2))
"
```

**Expected**: Returns keyword list and structured SEO outline.

---

### Test 7: MCP Server Startup

```bash
cd backend

# Start MCP server (should initialize without errors)
timeout 10 python mcp_server.py 2>&1 | head -20

# Expected output:
# "Initializing Personal Knowledge Platform MCP Server..."
# "MCP Server ready!"
```

**Expected**: Server starts, no errors, shows "MCP Server ready!"

---

### Test 8: Claude Desktop Integration

1. **Check Claude Desktop config**:
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   Should contain `personal-knowledge` server entry.

2. **Restart Claude Desktop**:
   - Fully quit Claude Desktop (Cmd+Q)
   - Reopen Claude Desktop

3. **Test in Claude.ai chat**:

   **Test 8a: List Tools**

   You: `What tools do you have?`

   **Expected**: I should list 9 tools including `search_knowledge_base`, `web_search`, etc.

   ---

   **Test 8b: List Documents**

   You: `List all indexed documents`

   **Expected**: I call `list_indexed_documents` tool and show test.txt

   ---

   **Test 8c: Search Knowledge Base**

   You: `Search my knowledge base for "benefits of PKM"`

   **Expected**: I call `search_knowledge_base` and return relevant excerpts from test.txt with citations

   ---

   **Test 8d: Web Search**

   You: `Search the web for latest trends in personal knowledge management 2026`

   **Expected**: I call `web_search` and return current web results with URLs

   ---

   **Test 8e: Combined Search**

   You: `What are the benefits of personal knowledge management? Use both my documents and web search.`

   **Expected**: I call BOTH tools and synthesize an answer citing both sources

   ---

   **Test 8f: SEO Outline**

   You: `Generate an SEO outline for an article about "Building a Personal Knowledge System"`

   **Expected**: I call `generate_seo_outline` and return structured outline with H1/H2s, keyword placement, checklist

   ---

   **Test 8g: Upload Document**

   You: `Upload this document: /Users/YOUR_USERNAME/Desktop/sample.pdf`

   (Replace with actual file path)

   **Expected**: I call `upload_document`, copy file to data/documents/, index it, confirm success

   ---

   **Test 8h: Reindex**

   You: `Reindex all my documents`

   **Expected**: I call `reindex_documents`, rebuild index, report number of files indexed

---

## Test 9: End-to-End Workflow (Perplexity-style)

**Complete research task with citations:**

You:
```
I want to research "LlamaIndex vs LangChain for RAG applications".

1. First search my knowledge base for any notes I have
2. Then search the web for latest comparisons
3. Write a comprehensive comparison with citations from both sources
```

**Expected**:
1. I call `search_knowledge_base(query="LlamaIndex LangChain RAG")`
2. I call `web_search(query="LlamaIndex vs LangChain 2026 comparison")`
3. I synthesize a comprehensive answer like:

> **LlamaIndex vs LangChain for RAG Applications**
>
> **Architecture**:
> - LlamaIndex specializes in data indexing and retrieval [Source: test.txt, p. 1]
> - LangChain focuses on chains and agents [Web: python.langchain.com]
>
> **Use Cases**:
> - LlamaIndex: Better for pure RAG and semantic search [Web: docs.llamaindex.ai]
> - LangChain: Better for complex multi-step workflows [Source: your-notes.txt]
>
> [... full comparison with 5-10 citations mixed from both sources ...]

---

## Test 10: SEO Article Generation

**Complete SEO workflow:**

You:
```
Write an SEO-optimized article about "How to Build a Personal Knowledge Base in 2026" using my notes.

1. Generate SEO outline first
2. Extract keywords from my notes
3. Search web for latest trends
4. Write 1500-word article with proper structure
5. Analyze the final content for SEO quality
```

**Expected**:
1. I call `generate_seo_outline(topic="...")`
2. I call `search_knowledge_base(query="knowledge base")`
3. I call `extract_keywords(text="[combined context]")`
4. I call `web_search(query="personal knowledge base 2026")`
5. I write full article with H1/H2 structure, keywords, citations
6. I call `analyze_content_seo(content="[article]", target_keyword="personal knowledge base")`
7. I report SEO scores and recommendations

---

## Troubleshooting Tests

### Test fails: "No module named X"

```bash
cd backend
pip install -r requirements.txt
```

### Test fails: "Connection refused" (PostgreSQL)

```bash
docker-compose up -d
docker ps  # Verify container running
docker logs knowledge-postgres  # Check for errors
```

### Test fails: "No documents indexed"

```bash
# Reindex manually
python -c "
from rag.indexer import DocumentIndexer
indexer = DocumentIndexer(
    'postgresql://kb_user:kb_pass@localhost:5432/knowledge_base',
    '../data/storage'
)
result = indexer.index_documents('../data/documents')
print(result)
"
```

### MCP tools not visible in Claude Desktop

1. Check config path: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Verify absolute path to mcp_server.py is correct
3. Restart Claude Desktop (full quit + reopen)
4. Check Claude Desktop logs (Help → Show Logs)
5. Test MCP server manually: `cd backend && python mcp_server.py`

### Web search returns empty results

```bash
# Test SearxNG instance
curl "https://searx.be/search?q=test&format=json" | jq '.results[0]'

# If SearxNG is down, try different instance in .env:
# SEARXNG_URL=https://searx.info
```

---

## Success Criteria

All tests should pass:

- [x] PostgreSQL connection works
- [x] Embeddings generate 384-dim vectors
- [x] Documents index successfully
- [x] Search returns relevant results
- [x] Web search returns current info
- [x] SEO tools generate outlines/keywords
- [x] MCP server starts without errors
- [x] 9 tools visible in Claude.ai
- [x] Can search knowledge base with citations
- [x] Can search web with URLs
- [x] Can upload new documents
- [x] Can generate SEO content
- [x] End-to-end research workflow completes

---

## Performance Benchmarks

Expected performance on typical hardware:

| Operation | Time | Notes |
|-----------|------|-------|
| Index 10 PDFs (100 pages) | 30-60s | First run (downloads embedding model) |
| Index 10 PDFs (cached) | 10-20s | Subsequent runs |
| Search query | 200-500ms | Local vector search |
| Web search | 1-3s | Depends on network |
| Generate embeddings (1 page) | 100-200ms | CPU-based |

If significantly slower:
- Check if using GPU instead of CPU (slower for small batches)
- Verify PostgreSQL is running locally (not remote)
- Check Docker resource limits

---

## Next Steps After Testing

Once all tests pass:

1. Add your real documents to `data/documents/`
2. Run reindex: Ask me "Reindex all documents"
3. Start using! Examples:
   - "Search my notes for X"
   - "Research Y using my docs and web"
   - "Write SEO article about Z"
   - "Summarize my papers on topic A"

Happy researching! 🚀
