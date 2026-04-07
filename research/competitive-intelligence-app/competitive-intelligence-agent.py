#!/usr/bin/env python3

import asyncio
import json
import re
import requests
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from textblob import TextBlob
import openai
from datetime import datetime
from search_providers import SearchProviderFactory, ReviewSearcher, ForumSearcher, CompetitorSearcher

@dataclass
class CompetitorProfile:
    name: str
    website: str
    description: str
    features: List[str]
    pricing_model: str
    target_market: str
    key_customers: List[str]
    sentiment_score: float
    strengths: List[str]
    weaknesses: List[str]
    reviews_summary: Dict[str, any]
    business_model: str
    funding_status: str
    market_position: str

@dataclass
class ResearchConfig:
    max_search_results: int = 20
    sentiment_threshold: float = 0.1
    min_content_length: int = 100
    search_delay: float = 1.0
    openai_model: str = "gpt-4"
    search_provider: str = "duckduckgo"
    search_api_key: Optional[str] = None

class WebSearcher:
    def __init__(self, config: ResearchConfig):
        self.config = config
        self.search_provider = SearchProviderFactory.create_provider(
            config.search_provider, 
            config.search_api_key
        )
        self.review_searcher = ReviewSearcher(self.search_provider)
        self.forum_searcher = ForumSearcher(self.search_provider)
        self.competitor_searcher = CompetitorSearcher(self.search_provider)
        
    async def search_web(self, query: str) -> List[Dict]:
        """Search web for competitor information"""
        try:
            results = self.search_provider.search(query, self.config.max_search_results)
            return results
        except Exception as e:
            print(f"Search error for '{query}': {e}")
            return []
    
    async def search_competitor_comprehensive(self, competitor_name: str) -> Dict[str, List[Dict]]:
        """Comprehensive competitor search using specialized searchers"""
        try:
            # Get comprehensive competitor information
            competitor_info = self.competitor_searcher.search_competitor_info(
                competitor_name, 
                self.config.max_search_results
            )
            
            # Add reviews and forum discussions
            reviews = self.review_searcher.search_reviews(competitor_name, 10)
            forums = self.forum_searcher.search_forums(competitor_name, 10)
            
            competitor_info['reviews'] = reviews
            competitor_info['forums'] = forums
            
            return competitor_info
            
        except Exception as e:
            print(f"Comprehensive search error for '{competitor_name}': {e}")
            return {}

class ContentExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CompetitiveIntelligenceBot/1.0)'
        })
    
    def extract_content(self, url: str) -> Dict[str, str]:
        """Extract and clean content from a webpage"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract key content sections
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Get main content (prioritize article, main, or content divs)
            content_selectors = [
                'article', 'main', '[role="main"]', 
                '.content', '#content', '.post-content',
                '.entry-content', '.article-content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join([elem.get_text().strip() for elem in elements])
                    break
            
            if not content:
                content = soup.get_text()
            
            # Clean and normalize content
            content = re.sub(r'\s+', ' ', content).strip()
            
            return {
                "title": title_text,
                "content": content,
                "url": url,
                "word_count": len(content.split())
            }
            
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return {"title": "", "content": "", "url": url, "word_count": 0}

class SentimentAnalyzer:
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text content"""
        try:
            blob = TextBlob(text)
            return {
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity,
                "classification": self._classify_sentiment(blob.sentiment.polarity)
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"polarity": 0.0, "subjectivity": 0.0, "classification": "neutral"}
    
    def _classify_sentiment(self, polarity: float) -> str:
        """Classify sentiment based on polarity score"""
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"

class FeatureExtractor:
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
    
    def extract_features(self, content: str, company_name: str) -> List[str]:
        """Extract product features using AI analysis"""
        if not self.openai_client:
            return self._extract_features_basic(content, company_name)
        
        try:
            prompt = f"""
            Analyze the following content about {company_name} and extract their key product features.
            Return only a JSON list of features, no other text.
            
            Content: {content[:3000]}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            features_text = response.choices[0].message.content
            features = json.loads(features_text)
            return features if isinstance(features, list) else []
            
        except Exception as e:
            print(f"AI feature extraction error: {e}")
            return self._extract_features_basic(content, company_name)
    
    def _extract_features_basic(self, content: str, company_name: str) -> List[str]:
        """Basic feature extraction using keywords"""
        feature_keywords = [
            'features', 'capabilities', 'functionality', 'tools', 
            'integrations', 'api', 'dashboard', 'analytics', 
            'reporting', 'automation', 'workflow', 'collaboration'
        ]
        
        features = []
        sentences = content.split('.')
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in feature_keywords):
                features.append(sentence.strip())
        
        return features[:10]  # Limit to top 10

class CompetitiveIntelligenceAgent:
    def __init__(self, config: ResearchConfig, openai_api_key: Optional[str] = None):
        self.config = config
        self.searcher = WebSearcher(config)
        self.extractor = ContentExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # Initialize OpenAI client if API key provided
        self.openai_client = None
        if openai_api_key:
            openai.api_key = openai_api_key
            self.openai_client = openai
        
        self.feature_extractor = FeatureExtractor(self.openai_client)
    
    async def research_competitor(self, competitor_name: str) -> CompetitorProfile:
        """Comprehensive research on a single competitor"""
        print(f"Researching {competitor_name}...")
        
        # Use comprehensive search to get categorized information
        search_results = await self.searcher.search_competitor_comprehensive(competitor_name)
        
        all_content = []
        website_url = ""
        
        # Process all search result categories
        for category, results in search_results.items():
            print(f"  Processing {category} ({len(results)} results)...")
            
            for result in results:
                if 'url' in result and result['url']:
                    content = self.extractor.extract_content(result['url'])
                    if content['word_count'] >= self.config.min_content_length:
                        content['category'] = category  # Tag content with category
                        all_content.append(content)
                        
                        # Try to identify main website
                        if not website_url and competitor_name.lower() in result['url'].lower():
                            website_url = result['url']
            
            await asyncio.sleep(self.config.search_delay)
        
        # Analyze collected content
        combined_content = ' '.join([c['content'] for c in all_content])
        
        # Extract various components
        features = self.feature_extractor.extract_features(combined_content, competitor_name)
        sentiment = self.sentiment_analyzer.analyze_sentiment(combined_content)
        
        # Create competitor profile
        profile = CompetitorProfile(
            name=competitor_name,
            website=website_url,
            description=self._extract_description(combined_content, competitor_name),
            features=features,
            pricing_model=self._extract_pricing_info(combined_content),
            target_market=self._extract_target_market(combined_content),
            key_customers=self._extract_customers(combined_content),
            sentiment_score=sentiment['polarity'],
            strengths=self._extract_strengths(combined_content),
            weaknesses=self._extract_weaknesses(combined_content),
            reviews_summary=self._summarize_reviews(combined_content),
            business_model=self._extract_business_model(combined_content),
            funding_status=self._extract_funding_info(combined_content),
            market_position=self._assess_market_position(combined_content)
        )
        
        return profile
    
    def _extract_description(self, content: str, company_name: str) -> str:
        """Extract company description"""
        sentences = content.split('.')
        for sentence in sentences[:10]:  # Check first 10 sentences
            if company_name.lower() in sentence.lower() and len(sentence.strip()) > 20:
                return sentence.strip()
        return f"{company_name} - competitive analysis based on available data"
    
    def _extract_pricing_info(self, content: str) -> str:
        """Extract pricing model information"""
        pricing_keywords = ['free', 'subscription', 'per user', 'enterprise', 'pricing', 'cost']
        sentences = content.lower().split('.')
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in pricing_keywords):
                return sentence.strip()
        
        return "Pricing information not clearly available"
    
    def _extract_target_market(self, content: str) -> str:
        """Extract target market information"""
        market_keywords = ['enterprise', 'small business', 'startup', 'b2b', 'b2c', 'industry']
        sentences = content.lower().split('.')
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in market_keywords):
                return sentence.strip()
        
        return "Target market not clearly defined"
    
    def _extract_customers(self, content: str) -> List[str]:
        """Extract key customer names"""
        # Look for common customer mention patterns
        customer_patterns = [
            r'customers include ([^.]+)',
            r'used by ([^.]+)',
            r'clients such as ([^.]+)',
            r'companies like ([^.]+)'
        ]
        
        customers = []
        for pattern in customer_patterns:
            matches = re.finditer(pattern, content.lower())
            for match in matches:
                customer_text = match.group(1)
                # Split and clean customer names
                names = [name.strip() for name in customer_text.split(',')]
                customers.extend(names[:3])  # Limit to 3 per pattern
        
        return customers[:10]  # Overall limit
    
    def _extract_strengths(self, content: str) -> List[str]:
        """Extract competitive strengths"""
        positive_keywords = [
            'best', 'leading', 'innovative', 'powerful', 'easy',
            'fast', 'reliable', 'secure', 'scalable', 'comprehensive'
        ]
        
        strengths = []
        sentences = content.split('.')
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in positive_keywords):
                if len(sentence.strip()) > 20:
                    strengths.append(sentence.strip())
        
        return strengths[:5]
    
    def _extract_weaknesses(self, content: str) -> List[str]:
        """Extract competitive weaknesses"""
        negative_keywords = [
            'lacks', 'missing', 'limited', 'expensive', 'slow',
            'complex', 'difficult', 'issues', 'problems', 'complaints'
        ]
        
        weaknesses = []
        sentences = content.split('.')
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in negative_keywords):
                if len(sentence.strip()) > 20:
                    weaknesses.append(sentence.strip())
        
        return weaknesses[:5]
    
    def _summarize_reviews(self, content: str) -> Dict[str, any]:
        """Summarize review information"""
        review_keywords = ['review', 'rating', 'stars', 'feedback']
        review_content = []
        
        sentences = content.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in review_keywords):
                review_content.append(sentence.strip())
        
        combined_reviews = ' '.join(review_content)
        sentiment = self.sentiment_analyzer.analyze_sentiment(combined_reviews)
        
        return {
            "overall_sentiment": sentiment['classification'],
            "sentiment_score": sentiment['polarity'],
            "review_count": len(review_content),
            "summary": combined_reviews[:300] + "..." if len(combined_reviews) > 300 else combined_reviews
        }
    
    def _extract_business_model(self, content: str) -> str:
        """Extract business model information"""
        model_keywords = ['saas', 'subscription', 'freemium', 'enterprise', 'marketplace']
        sentences = content.lower().split('.')
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in model_keywords):
                return sentence.strip()
        
        return "Business model not clearly identified"
    
    def _extract_funding_info(self, content: str) -> str:
        """Extract funding and investment information"""
        funding_keywords = ['funding', 'investment', 'series', 'million', 'billion', 'vc', 'venture']
        sentences = content.lower().split('.')
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in funding_keywords):
                return sentence.strip()
        
        return "Funding information not available"
    
    def _assess_market_position(self, content: str) -> str:
        """Assess market position"""
        position_keywords = {
            'leader': ['leader', 'leading', 'market leader', 'dominant'],
            'challenger': ['challenger', 'competitive', 'growing', 'emerging'],
            'niche': ['niche', 'specialized', 'focused', 'specific'],
            'startup': ['startup', 'new', 'founded', 'early stage']
        }
        
        content_lower = content.lower()
        scores = {}
        
        for position, keywords in position_keywords.items():
            score = sum(content_lower.count(keyword) for keyword in keywords)
            scores[position] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return "Market position unclear"

class ReportGenerator:
    def __init__(self):
        self.template = """
# Competitive Intelligence Report
Generated on: {date}

## Executive Summary
{executive_summary}

## Competitor Analysis
{competitor_analysis}

## Feature Comparison Matrix
{feature_matrix}

## Gap Analysis
{gap_analysis}

## Market Positioning
{market_positioning}

## Key Insights
{key_insights}

## Recommendations
{recommendations}
"""
    
    def generate_report(self, competitors: List[CompetitorProfile], focus_areas: Optional[List[str]] = None) -> str:
        """Generate comprehensive competitive intelligence report"""
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate each section
        executive_summary = self._generate_executive_summary(competitors)
        competitor_analysis = self._generate_competitor_analysis(competitors)
        feature_matrix = self._generate_feature_matrix(competitors)
        gap_analysis = self._generate_gap_analysis(competitors)
        market_positioning = self._generate_market_positioning(competitors)
        key_insights = self._generate_key_insights(competitors)
        recommendations = self._generate_recommendations(competitors)
        
        return self.template.format(
            date=date,
            executive_summary=executive_summary,
            competitor_analysis=competitor_analysis,
            feature_matrix=feature_matrix,
            gap_analysis=gap_analysis,
            market_positioning=market_positioning,
            key_insights=key_insights,
            recommendations=recommendations
        )
    
    def _generate_executive_summary(self, competitors: List[CompetitorProfile]) -> str:
        """Generate executive summary"""
        total_competitors = len(competitors)
        avg_sentiment = sum(c.sentiment_score for c in competitors) / total_competitors if competitors else 0
        
        summary = f"""
Analyzed {total_competitors} competitors with an average market sentiment of {avg_sentiment:.2f}.

Key Findings:
- Market leaders: {', '.join([c.name for c in competitors if c.market_position == 'leader'])}
- Emerging challengers: {', '.join([c.name for c in competitors if c.market_position == 'challenger'])}
- Average feature count: {sum(len(c.features) for c in competitors) // total_competitors if competitors else 0}
"""
        return summary.strip()
    
    def _generate_competitor_analysis(self, competitors: List[CompetitorProfile]) -> str:
        """Generate detailed competitor analysis"""
        analysis = []
        
        for competitor in competitors:
            section = f"""
### {competitor.name}
- **Website**: {competitor.website}
- **Description**: {competitor.description}
- **Market Position**: {competitor.market_position}
- **Pricing Model**: {competitor.pricing_model}
- **Target Market**: {competitor.target_market}
- **Sentiment Score**: {competitor.sentiment_score:.2f}
- **Key Customers**: {', '.join(competitor.key_customers[:5])}

**Strengths:**
{chr(10).join([f"- {s}" for s in competitor.strengths[:3]])}

**Weaknesses:**
{chr(10).join([f"- {w}" for w in competitor.weaknesses[:3]])}

**Top Features:**
{chr(10).join([f"- {f}" for f in competitor.features[:5]])}
"""
            analysis.append(section)
        
        return '\n'.join(analysis)
    
    def _generate_feature_matrix(self, competitors: List[CompetitorProfile]) -> str:
        """Generate feature comparison matrix"""
        if not competitors:
            return "No competitors to compare"
        
        # Collect all unique features
        all_features = set()
        for competitor in competitors:
            all_features.update(competitor.features)
        
        # Create matrix header
        matrix = "| Feature | " + " | ".join([c.name for c in competitors]) + " |\n"
        matrix += "|---------|" + "|".join(["--------" for _ in competitors]) + "|\n"
        
        # Add feature rows
        for feature in sorted(list(all_features))[:20]:  # Limit to top 20 features
            row = f"| {feature} |"
            for competitor in competitors:
                has_feature = "✓" if feature in competitor.features else "✗"
                row += f" {has_feature} |"
            matrix += row + "\n"
        
        return matrix
    
    def _generate_gap_analysis(self, competitors: List[CompetitorProfile]) -> str:
        """Generate gap analysis"""
        if not competitors:
            return "No competitors to analyze"
        
        # Find common features
        feature_counts = {}
        for competitor in competitors:
            for feature in competitor.features:
                feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        common_features = [f for f, count in feature_counts.items() if count >= len(competitors) * 0.6]
        unique_features = [f for f, count in feature_counts.items() if count == 1]
        
        analysis = f"""
**Market Standard Features (60%+ adoption):**
{chr(10).join([f"- {f}" for f in common_features[:10]])}

**Unique/Differentiating Features:**
{chr(10).join([f"- {f}" for f in unique_features[:10]])}

**Feature Coverage Analysis:**
- Total unique features identified: {len(feature_counts)}
- Average features per competitor: {sum(len(c.features) for c in competitors) // len(competitors)}
- Most feature-rich: {max(competitors, key=lambda c: len(c.features)).name} ({len(max(competitors, key=lambda c: len(c.features)).features)} features)
"""
        return analysis.strip()
    
    def _generate_market_positioning(self, competitors: List[CompetitorProfile]) -> str:
        """Generate market positioning analysis"""
        positions = {}
        for competitor in competitors:
            pos = competitor.market_position
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(competitor.name)
        
        positioning = "**Market Position Distribution:**\n"
        for position, companies in positions.items():
            positioning += f"- {position.title()}: {', '.join(companies)}\n"
        
        sentiment_analysis = "\n**Sentiment Analysis:**\n"
        for competitor in sorted(competitors, key=lambda c: c.sentiment_score, reverse=True):
            sentiment_desc = "Positive" if competitor.sentiment_score > 0.1 else "Negative" if competitor.sentiment_score < -0.1 else "Neutral"
            sentiment_analysis += f"- {competitor.name}: {sentiment_desc} ({competitor.sentiment_score:.2f})\n"
        
        return positioning + sentiment_analysis
    
    def _generate_key_insights(self, competitors: List[CompetitorProfile]) -> str:
        """Generate key insights"""
        if not competitors:
            return "No insights available"
        
        # Calculate insights
        highest_sentiment = max(competitors, key=lambda c: c.sentiment_score)
        lowest_sentiment = min(competitors, key=lambda c: c.sentiment_score)
        most_features = max(competitors, key=lambda c: len(c.features))
        
        insights = f"""
1. **Sentiment Leader**: {highest_sentiment.name} has the highest market sentiment ({highest_sentiment.sentiment_score:.2f})
2. **Feature Leader**: {most_features.name} offers the most features ({len(most_features.features)} identified)
3. **Market Sentiment**: Overall market sentiment is {'positive' if sum(c.sentiment_score for c in competitors) > 0 else 'negative'}
4. **Competitive Density**: {len(competitors)} active competitors identified
5. **Pricing Models**: {len(set(c.pricing_model for c in competitors))} different pricing approaches observed
"""
        return insights.strip()
    
    def _generate_recommendations(self, competitors: List[CompetitorProfile]) -> str:
        """Generate strategic recommendations"""
        recommendations = """
Based on the competitive analysis, consider the following strategic recommendations:

1. **Feature Gaps**: Focus on developing features that competitors lack
2. **Market Positioning**: Identify underserved market segments
3. **Pricing Strategy**: Analyze competitor pricing to find optimal positioning
4. **Customer Acquisition**: Learn from competitors' customer success stories
5. **Differentiation**: Leverage unique strengths while addressing weaknesses
"""
        return recommendations.strip()

# CLI Interface
def main():
    """Main CLI interface for competitive intelligence agent"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Competitive Intelligence Research Agent")
    parser.add_argument("competitors", nargs="+", help="Competitor names to research")
    parser.add_argument("--output", "-o", default="competitive_report.md", help="Output report file")
    parser.add_argument("--openai-key", help="OpenAI API key for enhanced analysis")
    parser.add_argument("--max-results", type=int, default=20, help="Max search results per query")
    parser.add_argument("--search-provider", 
                       choices=['duckduckgo', 'serpapi', 'bing', 'newsapi'],
                       default='duckduckgo',
                       help="Search provider to use")
    parser.add_argument("--search-api-key", help="API key for search provider (if required)")
    
    args = parser.parse_args()
    
    # Configuration
    config = ResearchConfig(
        max_search_results=args.max_results,
        openai_model="gpt-4",
        search_provider=args.search_provider,
        search_api_key=args.search_api_key
    )
    
    # Initialize agent
    agent = CompetitiveIntelligenceAgent(config, args.openai_key)
    report_generator = ReportGenerator()
    
    async def run_research():
        print(f"Starting competitive intelligence research on: {', '.join(args.competitors)}")
        
        competitor_profiles = []
        for competitor in args.competitors:
            try:
                profile = await agent.research_competitor(competitor)
                competitor_profiles.append(profile)
                print(f"✓ Completed research on {competitor}")
            except Exception as e:
                print(f"✗ Error researching {competitor}: {e}")
        
        if competitor_profiles:
            print(f"\nGenerating report for {len(competitor_profiles)} competitors...")
            report = report_generator.generate_report(competitor_profiles)
            
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✓ Report saved to {args.output}")
            
            # Also save JSON data
            json_output = args.output.replace('.md', '.json')
            with open(json_output, 'w', encoding='utf-8') as f:
                json.dump([asdict(profile) for profile in competitor_profiles], f, indent=2)
            
            print(f"✓ Raw data saved to {json_output}")
        else:
            print("No competitor data collected")
    
    # Run the research
    asyncio.run(run_research())

if __name__ == "__main__":
    main()