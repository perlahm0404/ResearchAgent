# Quick Start Guide (5 Minutes)

Get your Personal Knowledge Platform running in 5 minutes.

## Prerequisites

- Docker Desktop installed and running
- Python 3.8+
- Claude Desktop app installed

## Step 1: Run Setup Script (2 min)

```bash
cd ~/personal-knowledge-platform
./setup.sh
```

This will:
- ✅ Start PostgreSQL
- ✅ Install Python dependencies
- ✅ Download spaCy model
- ✅ Configure Claude Desktop
- ✅ Test MCP server

## Step 2: Add Test Document (30 sec)

```bash
cat > data/documents/test.txt <<EOF
# Personal Knowledge Management

PKM helps you organize information effectively.

## Key Benefits
- Better retention
- Faster retrieval
- Improved decision making

## Best Practices
- Use tags consistently
- Review regularly
- Link related concepts
EOF
```

## Step 3: Restart Claude Desktop (30 sec)

1. Quit Claude Desktop completely (Cmd+Q)
2. Reopen Claude Desktop

## Step 4: Test in Claude.ai (2 min)

Open a new chat in Claude Desktop and try these:

### Test 1: Verify Tools
**You**: `What tools do you have?`

**Expected**: I list 9 tools including search_knowledge_base, web_search, etc.

---

### Test 2: Index Documents
**You**: `Reindex all my documents`

**Expected**: I report "Successfully indexed 1 document: test.txt"

---

### Test 3: Search Knowledge Base
**You**: `Search my knowledge base for "benefits of PKM"`

**Expected**: I return results from test.txt with citations like:
> Found in test.txt:
> "Better retention, Faster retrieval, Improved decision making"

---

### Test 4: Web Search
**You**: `Search the web for "personal knowledge management 2026"`

**Expected**: I return current web results with URLs

---

### Test 5: Combined Research
**You**: `What are the benefits of personal knowledge management? Use my documents AND web search.`

**Expected**: I call BOTH tools and synthesize an answer citing both sources:
> **Benefits of Personal Knowledge Management**:
>
> According to your notes [Source: test.txt]:
> - Better retention
> - Faster retrieval
> - Improved decision making
>
> Recent research also shows [Web: example.com]:
> - Enhanced creativity
> - Reduced information overload
> ...

---

## Step 5: Upload Your Real Documents (ongoing)

```bash
# Add your PDFs, notes, etc.
cp ~/Documents/*.pdf data/documents/

# Ask me to reindex
```

Then in Claude: `Reindex all my documents`

---

## Common First Commands

### Research with Citations
```
Research [topic] using my documents and web search. Include citations.
```

### Generate SEO Article
```
Write an SEO-optimized article about [topic] using my notes.
```

### Upload New Document
```
Upload this document: /path/to/file.pdf
```

### Analyze Content
```
Extract keywords from this text: [paste text]
```

### Generate Content Outline
```
Generate an SEO outline for an article about [topic]
```

---

## Troubleshooting (1 min)

### "No documents indexed yet"
```bash
# In Claude.ai
Reindex all my documents
```

### "MCP tools not visible"
1. Check config exists: `cat ~/Library/Application\ Support/Claude/claude_desktop_config.json`
2. Restart Claude Desktop (full quit + reopen)
3. Look for "personal-knowledge" server in settings

### "PostgreSQL connection error"
```bash
docker-compose up -d
docker ps  # Verify container running
```

---

## You're Ready!

Your Personal Knowledge Platform is now running. Try these workflows:

1. **Daily Research**: Ask me to research topics using your docs + web
2. **SEO Writing**: Generate optimized articles from your notes
3. **Knowledge Synthesis**: Summarize multiple documents
4. **Continuous Learning**: Upload new documents, reindex, search

---

## Next Steps

- Read [TESTING.md](TESTING.md) for comprehensive test suite
- Read [README.md](README.md) for full documentation
- Read [IMPLEMENTATION_LOG.md](IMPLEMENTATION_LOG.md) for technical details

**Happy researching!** 🚀
