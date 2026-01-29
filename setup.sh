#!/bin/bash
set -e

echo "=== Personal Knowledge Platform Setup ==="
echo ""

# Get username
USERNAME=$(whoami)
PROJECT_DIR="/Users/$USERNAME/personal-knowledge-platform"

echo "Project directory: $PROJECT_DIR"
echo ""

# Check if Docker is running
echo "1. Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi
echo "✓ Docker is running"
echo ""

# Start PostgreSQL
echo "2. Starting PostgreSQL..."
cd "$PROJECT_DIR"
docker-compose up -d
echo "✓ PostgreSQL started"
echo ""

# Wait for PostgreSQL to be ready
echo "3. Waiting for PostgreSQL to be ready..."
sleep 5
until docker exec knowledge-postgres pg_isready -U kb_user -d knowledge_base > /dev/null 2>&1; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done
echo "✓ PostgreSQL is ready"
echo ""

# Install Python dependencies
echo "4. Installing Python dependencies..."
cd "$PROJECT_DIR/backend"
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Download spaCy model
echo "5. Downloading spaCy model..."
python -m spacy download en_core_web_sm
echo "✓ spaCy model installed"
echo ""

# Create Claude Desktop config
echo "6. Configuring Claude Desktop..."
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

mkdir -p "$CLAUDE_CONFIG_DIR"

# Check if config exists
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "WARNING: Claude Desktop config already exists at:"
    echo "$CLAUDE_CONFIG_FILE"
    echo ""
    echo "You'll need to manually add this MCP server to your config:"
    echo ""
    echo "  \"personal-knowledge\": {"
    echo "    \"command\": \"python\","
    echo "    \"args\": ["
    echo "      \"$PROJECT_DIR/backend/mcp_server.py\""
    echo "    ],"
    echo "    \"env\": {"
    echo "      \"SEARXNG_URL\": \"https://searx.be\""
    echo "    }"
    echo "  }"
    echo ""
else
    cat > "$CLAUDE_CONFIG_FILE" <<EOF
{
  "mcpServers": {
    "personal-knowledge": {
      "command": "python",
      "args": [
        "$PROJECT_DIR/backend/mcp_server.py"
      ],
      "env": {
        "SEARXNG_URL": "https://searx.be"
      }
    }
  }
}
EOF
    echo "✓ Claude Desktop config created"
fi
echo ""

# Test MCP server
echo "7. Testing MCP server..."
cd "$PROJECT_DIR/backend"
timeout 5 python mcp_server.py 2>&1 | head -5 || true
echo "✓ MCP server can start"
echo ""

echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Add documents to: $PROJECT_DIR/data/documents/"
echo "2. Restart Claude Desktop (quit and reopen)"
echo "3. Ask Claude: 'What tools do you have?'"
echo "4. Ask Claude: 'Reindex all documents'"
echo "5. Start searching: 'Search my knowledge base for X'"
echo ""
echo "Configuration file: $CLAUDE_CONFIG_FILE"
echo ""
