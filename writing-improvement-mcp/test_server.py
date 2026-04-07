#!/usr/bin/env python3
"""
Test script for the Writing Improvement MCP Server.
Tests the tools directly without MCP protocol overhead.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from tools.analyzer import WritingAnalyzer
from tools.improver import WritingImprover
from tools.readability import ReadabilityAnalyzer


def test_analyzer():
    """Test the WritingAnalyzer class."""
    print("=== TESTING WRITING ANALYZER ===\n")
    
    analyzer = WritingAnalyzer()
    
    test_text = """
    The implementation of our innovative methodological framework has potentially resulted in what might be considered a significant enhancement of various operational efficiency metrics across all of the evaluated parameters within the organizational structure. It is generally believed by many stakeholders that this particular approach could possibly address some of the numerous challenges that have been identified through extensive consultation processes.

    Furthermore, the utilization of advanced analytical techniques has facilitated the optimization of resource allocation mechanisms. The data suggests that there might be improvements in productivity, although the exact magnitude of these improvements remains somewhat unclear at this point in time.
    """
    
    result = analyzer.analyze(test_text.strip())
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Analysis completed successfully")
    print(f"📊 Overall Score: {result['overall_score']}/100")
    print(f"📖 Flesch Reading Ease: {result['readability']['flesch_reading_ease']}")
    print(f"🔍 Passive Voice: {result['clarity']['passive_voice_percentage']}%")
    print(f"📚 Unsupported Claims: {result['evidence']['unsupported_claims_count']}")
    print(f"💡 Recommendations: {len(result['recommendations'])}")
    
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    
    print()
    return True


def test_improver():
    """Test the WritingImprover class."""
    print("=== TESTING WRITING IMPROVER ===\n")
    
    improver = WritingImprover()
    
    test_text = """
    The implementation of our innovative methodological framework has potentially resulted in what might be considered a significant enhancement of various operational efficiency metrics. It is generally believed that this approach could possibly address numerous challenges.
    """
    
    result = improver.improve(test_text.strip())
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Improvement completed successfully")
    print(f"🔧 Changes Made: {result['changes_count']}")
    
    metrics = result['metrics']
    print(f"📊 Readability: {metrics['original']['flesch_score']} → {metrics['improved']['flesch_score']} ({metrics['improvements']['flesch_score_change']:+.1f})")
    print(f"📏 Word Count: {metrics['original']['word_count']} → {metrics['improved']['word_count']}")
    print(f"🎯 Overall Score: {metrics['original']['overall_score']} → {metrics['improved']['overall_score']} ({metrics['improvements']['overall_score_change']:+d})")
    
    print("\n📝 ORIGINAL:")
    print(result['original_text'])
    
    print("\n📝 IMPROVED:")
    print(result['improved_text'])
    
    print("\n🔧 CHANGES:")
    for i, change in enumerate(result['changes_made'], 1):
        print(f"  {i}. {change}")
    
    print()
    return True


def test_file_operations():
    """Test file-based operations."""
    print("=== TESTING FILE OPERATIONS ===\n")
    
    # Create a test file
    test_file = "/tmp/test_writing.txt"
    test_content = """
    The utilization of complex methodological frameworks might potentially enhance operational efficiency. It is believed that this approach could address various challenges that have been identified by stakeholders.
    """
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_content.strip())
        
        print(f"✅ Test file created: {test_file}")
        
        # Test analyzer
        analyzer = WritingAnalyzer()
        with open(test_file, 'r') as f:
            content = f.read()
        
        result = analyzer.analyze(content)
        if "error" not in result:
            print(f"✅ File analysis successful (Score: {result['overall_score']}/100)")
        else:
            print(f"❌ File analysis failed: {result['error']}")
            return False
        
        # Test improver
        improver = WritingImprover()
        result = improver.improve(content)
        if "error" not in result:
            print(f"✅ File improvement successful ({result['changes_count']} changes)")
            
            # Save improved version
            improved_file = "/tmp/test_writing_improved.txt"
            with open(improved_file, 'w') as f:
                f.write(result['improved_text'])
            print(f"✅ Improved file saved: {improved_file}")
        else:
            print(f"❌ File improvement failed: {result['error']}")
            return False
        
        # Cleanup
        os.unlink(test_file)
        os.unlink(improved_file)
        print(f"✅ Test files cleaned up")
        
    except Exception as e:
        print(f"❌ File operations failed: {str(e)}")
        return False
    
    print()
    return True


def test_readability_tools():
    """Test the ReadabilityAnalyzer class."""
    print("=== TESTING READABILITY TOOLS ===\n")
    
    readability_analyzer = ReadabilityAnalyzer()
    
    test_text = """
    The implementation of our innovative methodological framework has potentially resulted in what might be considered a significant enhancement of various operational efficiency metrics. This approach addresses numerous challenges that have been identified by stakeholders through extensive consultation processes.
    """
    
    # Test comprehensive readability analysis
    result = readability_analyzer.comprehensive_readability_analysis(test_text.strip())
    if "error" in result:
        print(f"❌ Comprehensive analysis failed: {result['error']}")
        return False
    
    print(f"✅ Comprehensive readability analysis successful")
    print(f"📊 Flesch Score: {result['readability_scores']['flesch_reading_ease']}")
    print(f"📖 Grade Level: {result['readability_scores']['flesch_kincaid_grade']}")
    print(f"⏱️ Reading Time (college): {result['reading_times']['college']['minutes']} min")
    
    # Test Flesch detailed analysis
    flesch_result = readability_analyzer.flesch_reading_ease_detailed(test_text.strip())
    if "error" in flesch_result:
        print(f"❌ Flesch detailed analysis failed: {flesch_result['error']}")
        return False
    
    print(f"✅ Flesch detailed analysis successful")
    print(f"📊 Flesch Score: {flesch_result['flesch_reading_ease']}")
    print(f"📖 Interpretation: {flesch_result['interpretation']['level']}")
    
    # Test grade level analysis
    grade_result = readability_analyzer.grade_level_analysis(test_text.strip())
    if "error" in grade_result:
        print(f"❌ Grade level analysis failed: {grade_result['error']}")
        return False
    
    print(f"✅ Grade level analysis successful")
    print(f"📊 Average Grade: {grade_result['average_grade_level']}")
    
    # Test reading time analysis
    time_result = readability_analyzer.reading_time_analysis(test_text.strip())
    if "error" in time_result:
        print(f"❌ Reading time analysis failed: {time_result['error']}")
        return False
    
    print(f"✅ Reading time analysis successful")
    print(f"📄 Word Count: {time_result['word_count']}")
    print(f"⏱️ Average Time: {time_result['average_reading_time']}")
    
    # Test sentence complexity analysis
    complexity_result = readability_analyzer.sentence_complexity_analysis(test_text.strip())
    if "error" in complexity_result:
        print(f"❌ Sentence complexity analysis failed: {complexity_result['error']}")
        return False
    
    print(f"✅ Sentence complexity analysis successful")
    complexity_metrics = complexity_result['complexity_metrics']
    print(f"📊 Total Sentences: {complexity_metrics['total_sentences']}")
    print(f"📏 Average Length: {complexity_metrics['average_sentence_length']} words")
    
    print()
    return True


def main():
    """Run all tests."""
    print("🧪 WRITING IMPROVEMENT MCP SERVER TESTS\n")
    
    tests = [
        ("Analyzer", test_analyzer),
        ("Improver", test_improver),
        ("File Operations", test_file_operations),
        ("Readability Tools", test_readability_tools)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED\n")
            else:
                failed += 1
                print(f"❌ {test_name} test FAILED\n")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} test FAILED with exception: {str(e)}\n")
    
    print("=" * 50)
    print(f"📊 TEST RESULTS: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! MCP server is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())