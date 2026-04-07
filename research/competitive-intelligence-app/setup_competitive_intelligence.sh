#!/bin/bash

echo "Setting up Competitive Intelligence Research Agent..."

# Install Python dependencies
pip install -r requirements.txt

# Download required NLTK data for TextBlob
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"

# Make the main script executable
chmod +x competitive-intelligence-agent.py

echo "Setup complete!"
echo ""
echo "Usage examples:"
echo "  python competitive-intelligence-agent.py 'Slack' 'Microsoft Teams' 'Discord'"
echo "  python competitive-intelligence-agent.py 'Notion' 'Obsidian' --output notion_vs_obsidian.md"
echo "  python competitive-intelligence-agent.py 'Figma' --openai-key YOUR_KEY --max-results 30"
echo ""
echo "The agent will:"
echo "  1. Search the web for competitor information"
echo "  2. Extract content from websites, reviews, and forums"
echo "  3. Analyze features, pricing, and sentiment"
echo "  4. Generate comprehensive comparison reports"
echo "  5. Export both markdown reports and JSON data"