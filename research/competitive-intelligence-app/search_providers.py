#!/usr/bin/env python3

import requests
import json
from typing import List, Dict, Optional
from urllib.parse import quote
import os

class SearchProvider:
    """Base class for search providers"""
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        raise NotImplementedError

class SerpAPIProvider(SearchProvider):
    """SerpAPI provider for Google search results"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        params = {
            'q': query,
            'api_key': self.api_key,
            'engine': 'google',
            'num': min(max_results, 100),
            'hl': 'en',
            'gl': 'us'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if 'organic_results' in data:
                for result in data['organic_results']:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('link', ''),
                        'snippet': result.get('snippet', ''),
                        'domain': result.get('displayed_link', '').split('/')[0]
                    })
            
            return results
            
        except Exception as e:
            print(f"SerpAPI search error: {e}")
            return []

class BingSearchProvider(SearchProvider):
    """Microsoft Bing Search API provider"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        
        params = {
            'q': query,
            'count': min(max_results, 50),
            'mkt': 'en-US',
            'responseFilter': 'Webpages'
        }
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if 'webPages' in data and 'value' in data['webPages']:
                for result in data['webPages']['value']:
                    results.append({
                        'title': result.get('name', ''),
                        'url': result.get('url', ''),
                        'snippet': result.get('snippet', ''),
                        'domain': result.get('displayUrl', '').split('/')[0]
                    })
            
            return results
            
        except Exception as e:
            print(f"Bing search error: {e}")
            return []

class DuckDuckGoProvider(SearchProvider):
    """DuckDuckGo search provider (free, no API key required)"""
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        params = {
            'q': query,
            'format': 'json',
            'no_redirect': '1',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # DuckDuckGo returns results in different formats
            if 'Results' in data:
                for result in data['Results'][:max_results]:
                    results.append({
                        'title': result.get('Text', ''),
                        'url': result.get('FirstURL', ''),
                        'snippet': result.get('Text', ''),
                        'domain': result.get('FirstURL', '').split('/')[2] if result.get('FirstURL') else ''
                    })
            
            # Also check RelatedTopics for additional results
            if 'RelatedTopics' in data:
                for topic in data['RelatedTopics'][:max_results - len(results)]:
                    if isinstance(topic, dict) and 'FirstURL' in topic:
                        results.append({
                            'title': topic.get('Text', ''),
                            'url': topic.get('FirstURL', ''),
                            'snippet': topic.get('Text', ''),
                            'domain': topic.get('FirstURL', '').split('/')[2] if topic.get('FirstURL') else ''
                        })
            
            return results
            
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []

class NewsAPIProvider(SearchProvider):
    """NewsAPI provider for news articles"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        params = {
            'q': query,
            'apiKey': self.api_key,
            'pageSize': min(max_results, 100),
            'language': 'en',
            'sortBy': 'relevancy'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if 'articles' in data:
                for article in data['articles']:
                    results.append({
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'snippet': article.get('description', ''),
                        'domain': article.get('source', {}).get('name', ''),
                        'published_at': article.get('publishedAt', ''),
                        'author': article.get('author', '')
                    })
            
            return results
            
        except Exception as e:
            print(f"NewsAPI search error: {e}")
            return []

class SearchProviderFactory:
    """Factory for creating search providers"""
    
    @staticmethod
    def create_provider(provider_type: str, api_key: Optional[str] = None) -> SearchProvider:
        """Create a search provider instance"""
        
        if provider_type.lower() == 'serpapi':
            if not api_key:
                raise ValueError("SerpAPI requires an API key")
            return SerpAPIProvider(api_key)
        
        elif provider_type.lower() == 'bing':
            if not api_key:
                raise ValueError("Bing Search requires an API key")
            return BingSearchProvider(api_key)
        
        elif provider_type.lower() == 'duckduckgo':
            return DuckDuckGoProvider()
        
        elif provider_type.lower() == 'newsapi':
            if not api_key:
                raise ValueError("NewsAPI requires an API key")
            return NewsAPIProvider(api_key)
        
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """Get list of available search providers"""
        return ['serpapi', 'bing', 'duckduckgo', 'newsapi']

# Specialized search classes for different content types
class ReviewSearcher:
    """Specialized searcher for product reviews"""
    
    def __init__(self, search_provider: SearchProvider):
        self.provider = search_provider
    
    def search_reviews(self, product_name: str, max_results: int = 20) -> List[Dict]:
        """Search for product reviews"""
        review_queries = [
            f"{product_name} reviews",
            f"{product_name} user feedback",
            f"{product_name} pros and cons",
            f"{product_name} rating",
            f"'{product_name}' review site:trustpilot.com OR site:g2.com OR site:capterra.com"
        ]
        
        all_results = []
        for query in review_queries:
            results = self.provider.search(query, max_results // len(review_queries))
            all_results.extend(results)
        
        return all_results

class ForumSearcher:
    """Specialized searcher for forum discussions"""
    
    def __init__(self, search_provider: SearchProvider):
        self.provider = search_provider
    
    def search_forums(self, topic: str, max_results: int = 20) -> List[Dict]:
        """Search for forum discussions"""
        forum_queries = [
            f"{topic} site:reddit.com",
            f"{topic} site:stackoverflow.com",
            f"{topic} site:producthunt.com",
            f"{topic} forum discussion",
            f"{topic} community feedback"
        ]
        
        all_results = []
        for query in forum_queries:
            results = self.provider.search(query, max_results // len(forum_queries))
            all_results.extend(results)
        
        return all_results

class CompetitorSearcher:
    """Specialized searcher for competitor information"""
    
    def __init__(self, search_provider: SearchProvider):
        self.provider = search_provider
    
    def search_competitor_info(self, competitor_name: str, max_results: int = 20) -> Dict[str, List[Dict]]:
        """Search for comprehensive competitor information"""
        
        search_categories = {
            'company_info': [
                f"{competitor_name} company about",
                f"{competitor_name} pricing plans",
                f"{competitor_name} features"
            ],
            'reviews': [
                f"{competitor_name} reviews",
                f"{competitor_name} customer feedback"
            ],
            'comparisons': [
                f"{competitor_name} vs competitors",
                f"{competitor_name} alternative",
                f"best {competitor_name} competitors"
            ],
            'business': [
                f"{competitor_name} funding",
                f"{competitor_name} revenue",
                f"{competitor_name} customers"
            ],
            'news': [
                f"{competitor_name} news",
                f"{competitor_name} updates",
                f"{competitor_name} announcement"
            ]
        }
        
        results = {}
        for category, queries in search_categories.items():
            category_results = []
            for query in queries:
                search_results = self.provider.search(query, max_results // len(queries))
                category_results.extend(search_results)
            results[category] = category_results
        
        return results

# Example usage and testing
def test_search_providers():
    """Test different search providers"""
    
    # Test DuckDuckGo (free)
    print("Testing DuckDuckGo...")
    ddg = DuckDuckGoProvider()
    results = ddg.search("Slack vs Teams", 5)
    print(f"DuckDuckGo results: {len(results)}")
    for result in results[:2]:
        print(f"  - {result['title']}")
    
    # Test SerpAPI (requires API key)
    serp_key = os.getenv('SERPAPI_KEY')
    if serp_key:
        print("\nTesting SerpAPI...")
        serp = SerpAPIProvider(serp_key)
        results = serp.search("Notion pricing", 5)
        print(f"SerpAPI results: {len(results)}")
        for result in results[:2]:
            print(f"  - {result['title']}")
    
    # Test specialized searchers
    print("\nTesting specialized searchers...")
    review_searcher = ReviewSearcher(ddg)
    forum_searcher = ForumSearcher(ddg)
    
    review_results = review_searcher.search_reviews("Figma", 3)
    forum_results = forum_searcher.search_forums("Figma vs Sketch", 3)
    
    print(f"Review results: {len(review_results)}")
    print(f"Forum results: {len(forum_results)}")

if __name__ == "__main__":
    test_search_providers()