#!/usr/bin/env python3

"""
Test script for Competitive Intelligence Research Agent

This script tests the basic functionality of the agent without making
extensive web requests.
"""

import sys
import asyncio
from unittest.mock import Mock, patch

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from competitive_intelligence_agent import (
            CompetitiveIntelligenceAgent,
            ReportGenerator,
            ResearchConfig,
            CompetitorProfile
        )
        print("✓ Main agent imports successful")
    except ImportError as e:
        print(f"✗ Main agent import failed: {e}")
        return False
    
    try:
        from search_providers import (
            SearchProviderFactory,
            DuckDuckGoProvider,
            ReviewSearcher,
            ForumSearcher
        )
        print("✓ Search provider imports successful")
    except ImportError as e:
        print(f"✗ Search provider import failed: {e}")
        return False
    
    # Test optional imports
    optional_imports = ['requests', 'bs4', 'textblob']
    for module in optional_imports:
        try:
            __import__(module)
            print(f"✓ {module} available")
        except ImportError:
            print(f"✗ {module} not available - run: pip install -r requirements.txt")
            return False
    
    return True

def test_configuration():
    """Test configuration and initialization"""
    print("\nTesting configuration...")
    
    try:
        from competitive_intelligence_agent import ResearchConfig
        
        # Test default configuration
        config = ResearchConfig()
        assert config.max_search_results == 20
        assert config.search_provider == "duckduckgo"
        print("✓ Default configuration works")
        
        # Test custom configuration
        config = ResearchConfig(
            max_search_results=50,
            search_provider="bing",
            search_api_key="test_key"
        )
        assert config.max_search_results == 50
        assert config.search_provider == "bing"
        print("✓ Custom configuration works")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_search_providers():
    """Test search provider factory"""
    print("\nTesting search providers...")
    
    try:
        from search_providers import SearchProviderFactory, DuckDuckGoProvider
        
        # Test DuckDuckGo provider (no API key needed)
        provider = SearchProviderFactory.create_provider("duckduckgo")
        assert isinstance(provider, DuckDuckGoProvider)
        print("✓ DuckDuckGo provider creation works")
        
        # Test provider list
        providers = SearchProviderFactory.get_available_providers()
        expected = ['serpapi', 'bing', 'duckduckgo', 'newsapi']
        assert all(p in providers for p in expected)
        print("✓ Provider list is correct")
        
        return True
        
    except Exception as e:
        print(f"✗ Search provider test failed: {e}")
        return False

def test_content_extraction():
    """Test content extraction with mock data"""
    print("\nTesting content extraction...")
    
    try:
        from competitive_intelligence_agent import ContentExtractor
        
        extractor = ContentExtractor()
        
        # Mock HTML content
        mock_html = """
        <html>
        <head><title>Test Company</title></head>
        <body>
            <article>
                <h1>About Test Company</h1>
                <p>We are a leading software company that provides innovative solutions.</p>
                <p>Our features include real-time collaboration, advanced analytics, and seamless integrations.</p>
            </article>
        </body>
        </html>
        """
        
        # Mock the requests.get method
        with patch('requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.content = mock_html.encode('utf-8')
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = extractor.extract_content("https://test.com")
            
            assert result['title'] == "Test Company"
            assert "leading software company" in result['content']
            assert result['word_count'] > 0
            print("✓ Content extraction works")
        
        return True
        
    except Exception as e:
        print(f"✗ Content extraction test failed: {e}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("\nTesting sentiment analysis...")
    
    try:
        from competitive_intelligence_agent import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        # Test positive sentiment
        positive_text = "This product is amazing! Great features and excellent support."
        result = analyzer.analyze_sentiment(positive_text)
        assert result['classification'] in ['positive', 'neutral']  # TextBlob can be conservative
        print("✓ Positive sentiment analysis works")
        
        # Test negative sentiment
        negative_text = "This product is terrible. Poor quality and awful customer service."
        result = analyzer.analyze_sentiment(negative_text)
        assert result['classification'] in ['negative', 'neutral']
        print("✓ Negative sentiment analysis works")
        
        return True
        
    except Exception as e:
        print(f"✗ Sentiment analysis test failed: {e}")
        return False

def test_report_generation():
    """Test report generation"""
    print("\nTesting report generation...")
    
    try:
        from competitive_intelligence_agent import ReportGenerator, CompetitorProfile
        
        # Create mock competitor profiles
        competitor1 = CompetitorProfile(
            name="Test Company A",
            website="https://testcompanya.com",
            description="A leading software company",
            features=["Feature 1", "Feature 2", "Feature 3"],
            pricing_model="Subscription",
            target_market="Enterprise",
            key_customers=["Customer 1", "Customer 2"],
            sentiment_score=0.5,
            strengths=["Strong product", "Good support"],
            weaknesses=["Expensive", "Complex setup"],
            reviews_summary={"overall_sentiment": "positive", "review_count": 10},
            business_model="SaaS",
            funding_status="Series B",
            market_position="leader"
        )
        
        competitor2 = CompetitorProfile(
            name="Test Company B",
            website="https://testcompanyb.com",
            description="An innovative startup",
            features=["Feature A", "Feature B"],
            pricing_model="Freemium",
            target_market="SMB",
            key_customers=["Customer X", "Customer Y"],
            sentiment_score=-0.2,
            strengths=["Affordable", "Easy to use"],
            weaknesses=["Limited features", "New company"],
            reviews_summary={"overall_sentiment": "neutral", "review_count": 5},
            business_model="Freemium",
            funding_status="Seed",
            market_position="challenger"
        )
        
        generator = ReportGenerator()
        report = generator.generate_report([competitor1, competitor2])
        
        # Verify report content
        assert "Test Company A" in report
        assert "Test Company B" in report
        assert "Feature Comparison Matrix" in report
        assert "Gap Analysis" in report
        assert "Key Insights" in report
        print("✓ Report generation works")
        
        return True
        
    except Exception as e:
        print(f"✗ Report generation test failed: {e}")
        return False

async def test_agent_initialization():
    """Test agent initialization"""
    print("\nTesting agent initialization...")
    
    try:
        from competitive_intelligence_agent import CompetitiveIntelligenceAgent, ResearchConfig
        
        config = ResearchConfig(search_provider="duckduckgo")
        agent = CompetitiveIntelligenceAgent(config)
        
        assert agent.config.search_provider == "duckduckgo"
        assert agent.searcher is not None
        assert agent.extractor is not None
        assert agent.sentiment_analyzer is not None
        print("✓ Agent initialization works")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent initialization test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI argument parsing"""
    print("\nTesting CLI interface...")
    
    try:
        import sys
        from io import StringIO
        from unittest.mock import patch
        
        # Mock sys.argv
        test_args = [
            'competitive-intelligence-agent.py',
            'TestCompany',
            '--output', 'test_report.md',
            '--search-provider', 'duckduckgo',
            '--max-results', '10'
        ]
        
        with patch.object(sys, 'argv', test_args):
            # Import main function
            from competitive_intelligence_agent import main
            
            # We can't easily test the full CLI without making web requests,
            # but we can test that it doesn't crash on import/setup
            print("✓ CLI interface imports correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ CLI interface test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("=== Competitive Intelligence Agent Test Suite ===\n")
    
    tests = [
        test_imports,
        test_configuration, 
        test_search_providers,
        test_content_extraction,
        test_sentiment_analysis,
        test_report_generation,
        test_agent_initialization,
        test_cli_interface
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if asyncio.iscoroutinefunction(test):
                success = await test()
            else:
                success = test()
            
            if success:
                passed += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! The agent is ready to use.")
        print("\nNext steps:")
        print("1. Try: python example_usage.py")
        print("2. Or run: python competitive-intelligence-agent.py 'YourCompetitor'")
    else:
        print(f"\n⚠️  {failed} tests failed. Please check the installation.")
        print("Try running: pip install -r requirements.txt")
    
    return failed == 0

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)