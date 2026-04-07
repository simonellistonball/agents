# Competitive Intelligence Research Agent

A comprehensive Python-based agent for automated competitive intelligence research. This tool searches the web, analyzes documentation, reviews, and forum posts to produce detailed competitive analysis reports.

## Features

### 🔍 Multi-Source Research
- **Web Search**: Supports multiple search providers (DuckDuckGo, SerpAPI, Bing, NewsAPI)
- **Content Extraction**: Intelligent content extraction from websites and documentation
- **Review Analysis**: Specialized review and forum post scraping
- **Sentiment Analysis**: Automated sentiment scoring using TextBlob

### 📊 Comprehensive Analysis
- **Feature Comparison**: Automatic feature extraction and comparison matrices
- **Gap Analysis**: Identifies market gaps and opportunities
- **Business Intelligence**: Analyzes business models, funding, and market position
- **Customer Intelligence**: Identifies key customers, users, and stakeholders

### 📈 Advanced AI Integration
- **OpenAI Integration**: Enhanced feature extraction using GPT-4
- **Sentiment Classification**: Positive/negative/neutral sentiment analysis
- **Automated Insights**: AI-powered competitive insights and recommendations

### 📋 Professional Reporting
- **Markdown Reports**: Clean, professional competitive analysis reports
- **JSON Export**: Raw data export for further analysis
- **Executive Summaries**: High-level insights for decision makers
- **Feature Matrices**: Visual comparison tables

## Installation

1. **Clone/Download the Agent**
   ```bash
   cd research/
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Setup Script**
   ```bash
   ./setup_competitive_intelligence.sh
   ```

4. **Download NLTK Data** (if not done by setup script)
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('brown')
   ```

## Usage

### Basic Usage (Free)

Research competitors using DuckDuckGo (no API key required):

```bash
python competitive-intelligence-agent.py "Slack" "Microsoft Teams" "Discord"
```

### Advanced Usage with APIs

Using premium search APIs for better results:

```bash
# Using SerpAPI
python competitive-intelligence-agent.py "Figma" "Sketch" "Adobe XD" \
  --search-provider serpapi --search-api-key YOUR_SERPAPI_KEY

# Using Bing Search API
python competitive-intelligence-agent.py "Notion" "Obsidian" \
  --search-provider bing --search-api-key YOUR_BING_KEY \
  --max-results 30

# With OpenAI for enhanced analysis
python competitive-intelligence-agent.py "Zoom" "Google Meet" \
  --openai-key YOUR_OPENAI_KEY \
  --output video_conferencing_analysis.md
```

### Command Line Options

```bash
python competitive-intelligence-agent.py [competitors] [options]

Arguments:
  competitors              List of competitor names to research

Options:
  --output, -o            Output report filename (default: competitive_report.md)
  --search-provider       Search provider: duckduckgo, serpapi, bing, newsapi
  --search-api-key        API key for search provider (if required)
  --openai-key           OpenAI API key for enhanced analysis
  --max-results          Maximum search results per query (default: 20)
```

## API Keys Setup

### Free Option
- **DuckDuckGo**: No API key required (default)

### Premium Options
- **SerpAPI**: Sign up at [serpapi.com](https://serpapi.com) - $50/month for 5,000 searches
- **Bing Search API**: Microsoft Cognitive Services - Free tier: 1,000 calls/month
- **NewsAPI**: Sign up at [newsapi.org](https://newsapi.org) - Free tier: 1,000 requests/day
- **OpenAI**: For enhanced AI analysis - Pay per use

### Environment Variables
```bash
export SERPAPI_KEY="your_serpapi_key"
export BING_SEARCH_KEY="your_bing_key"  
export NEWSAPI_KEY="your_newsapi_key"
export OPENAI_API_KEY="your_openai_key"
```

## Example Outputs

### Report Structure
```markdown
# Competitive Intelligence Report
Generated on: 2024-01-15 14:30:00

## Executive Summary
Analyzed 3 competitors with an average market sentiment of 0.15.

## Competitor Analysis
### Slack
- **Market Position**: leader
- **Sentiment Score**: 0.25
- **Top Features**: Real-time messaging, File sharing, App integrations...

## Feature Comparison Matrix
| Feature | Slack | Microsoft Teams | Discord |
|---------|-------|-----------------|---------|
| Video calling | ✓ | ✓ | ✓ |
| Screen sharing | ✓ | ✓ | ✓ |

## Gap Analysis
**Market Standard Features (60%+ adoption):**
- Real-time messaging
- File sharing
- Video calling

## Key Insights
1. **Sentiment Leader**: Slack has the highest market sentiment (0.25)
2. **Feature Leader**: Microsoft Teams offers the most features (45 identified)

## Recommendations
Based on the competitive analysis, consider the following strategic recommendations...
```

### JSON Data Export
```json
[
  {
    "name": "Slack",
    "website": "https://slack.com",
    "market_position": "leader",
    "sentiment_score": 0.25,
    "features": ["Real-time messaging", "File sharing", ...],
    "key_customers": ["IBM", "Shopify", "Target"],
    "strengths": ["Easy to use", "Great integrations"],
    "weaknesses": ["Can be expensive", "Limited video features"]
  }
]
```

## Use Cases

### 🏢 Business Strategy
- **Market Entry**: Research competitors before entering new markets
- **Product Planning**: Identify feature gaps and opportunities
- **Competitive Positioning**: Understand market landscape and positioning
- **Investment Research**: Due diligence on competitive landscape

### 📊 Product Management
- **Feature Benchmarking**: Compare product features across competitors
- **Pricing Analysis**: Understand competitive pricing strategies  
- **User Research**: Analyze customer sentiment and feedback
- **Roadmap Planning**: Prioritize features based on competitive analysis

### 💼 Sales & Marketing
- **Battle Cards**: Create competitive battle cards for sales teams
- **Positioning**: Develop competitive positioning and messaging
- **Content Strategy**: Understand competitor content and messaging
- **Customer Research**: Identify competitor customers and case studies

## Advanced Features

### Custom Search Providers
Extend the agent with custom search providers:

```python
from search_providers import SearchProvider

class CustomSearchProvider(SearchProvider):
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        # Implement your custom search logic
        return results
```

### Custom Content Analysis
Add custom analysis modules:

```python
class CustomAnalyzer:
    def analyze_content(self, content: str) -> Dict:
        # Implement custom analysis
        return analysis_results
```

## Limitations

### Search Limitations
- **Rate Limits**: API providers have rate limits and usage quotas
- **Content Access**: Some sites block automated scraping
- **Data Quality**: Search result quality varies by provider and query
- **Geographic Bias**: Results may be biased toward specific regions

### Analysis Limitations
- **Language**: Currently optimized for English content
- **Context**: May miss nuanced competitive dynamics
- **Real-time**: Data reflects point-in-time information
- **Accuracy**: Automated analysis may miss important context

## Contributing

### Adding Search Providers
1. Create a new provider class in `search_providers.py`
2. Implement the `SearchProvider` interface
3. Add to `SearchProviderFactory`
4. Update CLI options

### Improving Analysis
1. Enhance content extraction in `ContentExtractor`
2. Add new analysis modules for specific use cases
3. Improve sentiment analysis accuracy
4. Add industry-specific analysis templates

## Troubleshooting

### Common Issues

**"No search results found"**
- Check internet connectivity
- Verify API keys are correct
- Try different search providers
- Adjust search queries

**"Content extraction failed"**
- Some sites block automated scraping
- Try using different user agents
- Consider using proxy services
- Check for CAPTCHA requirements

**"API rate limit exceeded"**
- Wait for rate limit reset
- Reduce `max_results` parameter
- Upgrade to higher API tier
- Use multiple API keys with rotation

**"Poor analysis quality"**
- Add OpenAI API key for enhanced analysis
- Increase `max_results` for more data
- Try different search providers
- Manually verify competitor names

### Support

For issues and feature requests:
1. Check existing GitHub issues
2. Create detailed bug reports
3. Include example commands and error messages
4. Provide sample data when possible

## License

This competitive intelligence research agent is provided as-is for educational and business research purposes. Users are responsible for complying with all applicable terms of service for search providers and websites being analyzed.

**Ethical Usage**: Always respect robots.txt, rate limits, and terms of service. Use responsibly for legitimate competitive research purposes only.