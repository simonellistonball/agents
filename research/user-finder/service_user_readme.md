# Service User Finder Agent

A specialized agent that searches the web to find companies and organizations using a particular service or product.

## Features

- **Real Web Search**: Uses DuckDuckGo API and HTML scraping to find actual results
- **Pattern Recognition**: Identifies usage indicators and company names using regex patterns
- **Multi-source Targeting**: Searches news sites, developer blogs, company sites, and business publications
- **Confidence Scoring**: Rates findings as high, medium, or low confidence based on evidence strength
- **Multiple Export Formats**: JSON, CSV, and Markdown output options
- **Analysis Tools**: Provides insights and breakdowns of findings

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Find users of Docker
python service_user_finder.py "Docker"

# Find users with custom result limit
python service_user_finder.py "Kubernetes" --max-results 25

# Export to specific format
python service_user_finder.py "AWS Lambda" --format markdown

# Save to file with analysis
python service_user_finder.py "Redis" --output redis_users.json --analyze
```

### Example Output

```json
[
  {
    "company": "Netflix",
    "source": "https://netflixtechblog.com/our-migration-story",
    "evidence": "Netflix successfully migrated to Kubernetes for container orchestration...",
    "confidence": "high",
    "type": "blog_post"
  }
]
```

## Search Strategy

The agent uses multiple search patterns to identify service usage:

### Usage Indicators
- Case studies and success stories
- Implementation announcements
- Migration stories
- "Powered by" mentions
- Integration guides
- Customer testimonials

### Target Sources
- **News Sites**: TechCrunch, VentureBeat, Ars Technica, ZDNet
- **Developer Blogs**: Medium, Dev.to, HashNode, HackerNoon
- **Business Sites**: Forbes, Business Insider, CNBC, Bloomberg
- **Company Sites**: Direct mentions on corporate websites

### Confidence Levels
- **High**: Case studies, customer stories, implementation details
- **Medium**: Integration mentions, adoption announcements
- **Low**: General mentions without clear usage context

## API Usage

```python
from service_user_finder import ServiceUserFinder
import asyncio

async def main():
    finder = ServiceUserFinder()
    findings = await finder.find_users("Docker", max_results=20)
    
    for finding in findings:
        print(f"{finding.company_name}: {finding.confidence_level}")

asyncio.run(main())
```

## Limitations

- Rate limited to prevent overwhelming search services
- Depends on public web content availability
- Company name extraction may have false positives
- Some results may require manual verification

## Contributing

To add new search patterns or target domains, modify the `search_patterns` and `target_domains` dictionaries in the `ServiceUserFinder` class.