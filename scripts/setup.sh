#!/usr/bin/env bash
set -e

CONFIG_DIR="$HOME/.config/iaedu"
CONFIG_FILE="$CONFIG_DIR/env"

echo "============================================"
echo "  llm-iaedu — Interactive Setup"
echo "============================================"
echo ""
echo "Go to iaedu.pt, open your agent, and copy the"
echo "three values it shows (Endpoint, API Key,"
echo "Channel ID). Paste them below."
echo ""

# --- Endpoint ---
read -p "IAEDU Endpoint URL (paste from iaedu.pt): " endpoint
while [ -z "$endpoint" ]; do
    echo "  Endpoint cannot be empty."
    read -p "IAEDU Endpoint URL: " endpoint
done

# --- API Key ---
read -p "IAEDU API Key (paste from iaedu.pt): " api_key
while [ -z "$api_key" ]; do
    echo "  API Key cannot be empty."
    read -p "IAEDU API Key: " api_key
done

# --- Channel ID ---
read -p "IAEDU Channel ID (paste from iaedu.pt): " channel_id
while [ -z "$channel_id" ]; do
    echo "  Channel ID cannot be empty."
    read -p "IAEDU Channel ID: " channel_id
done

# --- Write global config ---
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_FILE" << EOF
# iaedu global config — used by llm-iaedu from any directory
IAEDU_ENDPOINT=$endpoint
IAEDU_CHANNEL_ID=$channel_id
IAEDU_API_KEY=$api_key
EOF

chmod 600 "$CONFIG_FILE"
echo ""
echo "  [OK] Config written to $CONFIG_FILE"

# --- Install package ---
echo ""
echo "Installing llm-iaedu..."
pip install llm-iaedu 2>/dev/null || pip install . 2>/dev/null || true

echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "  llm -m iaedu \"What is the capital of Portugal?\""
echo "  llm models default iaedu"
echo "  llm \"What is the capital of Portugal?\""
echo ""
