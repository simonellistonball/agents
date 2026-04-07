#!/usr/bin/env python3

"""
Example usage of the Competitive Intelligence Research Agent

This script demonstrates various ways to use the agent for competitive research.
"""

import asyncio
import os
from competitive_intelligence_agent import (
    CompetitiveIntelligenceAgent,
    ReportGenerator,
    ResearchConfig
)

async def example_basic_research():
    """Example 1: Basic competitive research"""
    print("=== Example 1: Basic Competitive Research ===")
    
    config = ResearchConfig(
        max_search_results=15,
        search_provider="duckduckgo"
    )
    
    agent = CompetitiveIntelligenceAgent(config)
    report_generator = ReportGenerator()
    
    # Research competitors
    competitors = ["Slack", "Microsoft Teams", "Discord"]
    profiles = []
    
    for competitor in competitors:
        try:
            profile = await agent.research_competitor(competitor)
            profiles.append(profile)
            print(f"✓ Completed research on {competitor}")
        except Exception as e:
            print(f"✗ Error researching {competitor}: {e}")
    
    # Generate report
    if profiles:
        report = report_generator.generate_report(profiles)
        with open("basic_research_report.md", "w") as f:
            f.write(report)
        print("✓ Report saved to basic_research_report.md")

async def example_advanced_research():
    """Example 2: Advanced research with OpenAI integration"""
    print("\n=== Example 2: Advanced Research with AI ===")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("Skipping advanced example - no OpenAI API key found")
        return
    
    config = ResearchConfig(
        max_search_results=25,
        search_provider="duckduckgo",
        openai_model="gpt-4"
    )
    
    agent = CompetitiveIntelligenceAgent(config, openai_key)
    report_generator = ReportGenerator()
    
    # Research design tools
    competitors = ["Figma", "Sketch", "Adobe XD"]
    profiles = []
    
    for competitor in competitors:
        try:
            profile = await agent.research_competitor(competitor)
            profiles.append(profile)
            print(f"✓ Completed advanced research on {competitor}")
        except Exception as e:
            print(f"✗ Error researching {competitor}: {e}")
    
    # Generate enhanced report
    if profiles:
        report = report_generator.generate_report(profiles)
        with open("advanced_research_report.md", "w") as f:
            f.write(report)
        print("✓ Advanced report saved to advanced_research_report.md")

async def example_api_research():
    """Example 3: Research using premium search APIs"""
    print("\n=== Example 3: Premium API Research ===")
    
    # Check for API keys
    serp_key = os.getenv('SERPAPI_KEY')
    bing_key = os.getenv('BING_SEARCH_KEY')
    
    if not (serp_key or bing_key):
        print("Skipping API example - no search API keys found")
        return
    
    # Use SerpAPI if available, otherwise Bing
    search_provider = "serpapi" if serp_key else "bing"
    api_key = serp_key if serp_key else bing_key
    
    config = ResearchConfig(
        max_search_results=30,
        search_provider=search_provider,
        search_api_key=api_key
    )
    
    agent = CompetitiveIntelligenceAgent(config)
    report_generator = ReportGenerator()
    
    # Research project management tools
    competitors = ["Notion", "Obsidian", "Roam Research"]
    profiles = []
    
    for competitor in competitors:
        try:
            profile = await agent.research_competitor(competitor)
            profiles.append(profile)
            print(f"✓ Completed API-powered research on {competitor}")
        except Exception as e:
            print(f"✗ Error researching {competitor}: {e}")
    
    # Generate comprehensive report
    if profiles:
        report = report_generator.generate_report(profiles)
        with open("api_research_report.md", "w") as f:
            f.write(report)
        print(f"✓ API-powered report saved using {search_provider}")

async def example_focused_analysis():
    """Example 4: Focused analysis on specific aspects"""
    print("\n=== Example 4: Focused Competitive Analysis ===")
    
    config = ResearchConfig(
        max_search_results=20,
        search_provider="duckduckgo"
    )
    
    agent = CompetitiveIntelligenceAgent(config)
    
    # Focus on one competitor for detailed analysis
    competitor_name = "Zoom"
    print(f"Conducting focused analysis on {competitor_name}...")
    
    try:
        profile = await agent.research_competitor(competitor_name)
        
        # Print detailed analysis
        print(f"\n=== {competitor_name} Analysis ===")
        print(f"Website: {profile.website}")
        print(f"Market Position: {profile.market_position}")
        print(f"Sentiment Score: {profile.sentiment_score:.3f}")
        print(f"Business Model: {profile.business_model}")
        print(f"Pricing Model: {profile.pricing_model}")
        
        print(f"\nTop Features ({len(profile.features)}):")
        for i, feature in enumerate(profile.features[:10], 1):
            print(f"  {i}. {feature}")
        
        print(f"\nKey Customers ({len(profile.key_customers)}):")
        for customer in profile.key_customers[:5]:
            print(f"  - {customer}")
        
        print(f"\nStrengths ({len(profile.strengths)}):")
        for strength in profile.strengths[:3]:
            print(f"  + {strength}")
        
        print(f"\nWeaknesses ({len(profile.weaknesses)}):")
        for weakness in profile.weaknesses[:3]:
            print(f"  - {weakness}")
        
        print(f"\nReview Summary:")
        print(f"  Overall Sentiment: {profile.reviews_summary.get('overall_sentiment')}")
        print(f"  Review Count: {profile.reviews_summary.get('review_count')}")
        
    except Exception as e:
        print(f"Error in focused analysis: {e}")

def setup_environment():
    """Setup environment and display configuration info"""
    print("=== Competitive Intelligence Research Agent ===")
    print("Environment Configuration:")
    
    # Check for API keys
    api_keys = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'SerpAPI': os.getenv('SERPAPI_KEY'),
        'Bing Search': os.getenv('BING_SEARCH_KEY'),
        'NewsAPI': os.getenv('NEWSAPI_KEY')
    }
    
    for service, key in api_keys.items():
        status = "✓ Available" if key else "✗ Not configured"
        print(f"  {service}: {status}")
    
    print(f"\nFree search providers: DuckDuckGo (no API key required)")
    print(f"Premium search providers: {', '.join([k for k, v in api_keys.items() if k != 'OpenAI' and v])}")
    print()

async def main():
    """Run all examples"""
    setup_environment()
    
    # Run examples
    await example_basic_research()
    await example_focused_analysis()
    await example_advanced_research()
    await example_api_research()
    
    print("\n=== All Examples Complete ===")
    print("Check the generated report files:")
    print("  - basic_research_report.md")
    print("  - advanced_research_report.md (if OpenAI key available)")
    print("  - api_research_report.md (if search API keys available)")

if __name__ == "__main__":
    asyncio.run(main())