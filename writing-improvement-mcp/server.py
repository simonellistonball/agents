#!/usr/bin/env python3
"""
MCP Server for Writing Improvement Tools.

Provides writing analysis and improvement capabilities as MCP tools.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

from tools.analyzer import WritingAnalyzer
from tools.improver import WritingImprover
from tools.readability import ReadabilityAnalyzer

# Initialize the MCP server
server = Server("writing-improvement")

# Initialize our tools
analyzer = WritingAnalyzer()
improver = WritingImprover()
readability_analyzer = ReadabilityAnalyzer()


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available writing improvement tools."""
    return [
        types.Tool(
            name="analyze_writing",
            description="Analyze text for readability, clarity, structure, and evidence quality. Returns detailed metrics and recommendations for improvement.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="improve_writing",
            description="Automatically improve text for better readability, clarity, and structure while preserving meaning. Returns improved text with change summary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to improve"
                    },
                    "target_flesch_score": {
                        "type": "integer",
                        "description": "Target Flesch Reading Ease score (default: 60)",
                        "default": 60,
                        "minimum": 0,
                        "maximum": 100
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="compare_writing_versions",
            description="Compare two versions of text to show writing improvements and changes in quality metrics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "original_text": {
                        "type": "string",
                        "description": "The original text"
                    },
                    "revised_text": {
                        "type": "string",
                        "description": "The revised text"
                    }
                },
                "required": ["original_text", "revised_text"]
            }
        ),
        types.Tool(
            name="comprehensive_readability_analysis",
            description="Perform detailed readability analysis with multiple metrics, reading times, and complexity assessment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze for readability"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="flesch_reading_ease_detailed",
            description="Detailed Flesch Reading Ease analysis with score breakdown, interpretation, and specific recommendations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze for Flesch Reading Ease"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="grade_level_analysis",
            description="Comprehensive grade level analysis using multiple formulas (Flesch-Kincaid, Gunning Fog, SMOG, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze for grade level"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="reading_time_analysis",
            description="Calculate reading times for different skill levels (elementary through professional) with difficulty assessment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze for reading time"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="sentence_complexity_analysis",
            description="Detailed analysis of sentence complexity, structure, and distribution patterns.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze for sentence complexity"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    
    if name == "analyze_writing":
        text = arguments.get("text", "")
        result = analyzer.analyze(text)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        # Format the analysis results nicely
        output = []
        output.append("=== WRITING ANALYSIS REPORT ===\n")
        
        # Overall Score
        output.append(f"📊 OVERALL SCORE: {result['overall_score']}/100\n")
        
        # Readability Metrics
        output.append("📖 READABILITY METRICS:")
        readability = result['readability']
        output.append(f"  • Flesch Reading Ease: {readability['flesch_reading_ease']} (target: 50-70)")
        output.append(f"  • Grade Level: {readability['flesch_kincaid_grade']}")
        output.append(f"  • Average Sentence Length: {readability['avg_sentence_length']} words")
        output.append(f"  • Reading Time: {readability['reading_time_seconds']:.0f} seconds")
        if not readability.get('textstat_available', True):
            output.append("  ⚠️  Using fallback metrics (install textstat for full analysis)")
        output.append("")
        
        # Clarity Analysis
        output.append("🔍 CLARITY ANALYSIS:")
        clarity = result['clarity']
        output.append(f"  • Passive Voice: {clarity['passive_voice_percentage']}% ({clarity['passive_voice_count']} sentences)")
        output.append(f"  • Vague Phrases: {clarity['vague_phrases_count']} ({clarity['vague_phrases_percentage']}%)")
        output.append(f"  • Jargon: {clarity['jargon_count']} instances")
        output.append(f"  • Complex Sentences: {clarity['complex_sentences_count']}")
        output.append("")
        
        # Structure Analysis
        output.append("🏗️ STRUCTURE ANALYSIS:")
        structure = result['structure']
        output.append(f"  • Paragraphs: {structure['paragraph_count']}")
        output.append(f"  • Sentences per Paragraph: {structure['avg_sentences_per_paragraph']}")
        output.append(f"  • Transition Words: {structure['transition_words_count']}")
        output.append(f"  • Clear Introduction: {'✓' if structure['has_clear_introduction'] else '✗'}")
        output.append(f"  • Clear Conclusion: {'✓' if structure['has_clear_conclusion'] else '✗'}")
        output.append("")
        
        # Evidence Analysis
        output.append("📚 EVIDENCE ANALYSIS:")
        evidence = result['evidence']
        output.append(f"  • Evidence-backed Sentences: {evidence['evidence_sentences_count']}")
        output.append(f"  • Unsupported Claims: {evidence['unsupported_claims_count']}")
        output.append(f"  • Contains Statistics: {'✓' if evidence['contains_statistics'] else '✗'}")
        output.append(f"  • Contains Citations: {'✓' if evidence['contains_citations'] else '✗'}")
        output.append("")
        
        # Recommendations
        if result['recommendations']:
            output.append("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(result['recommendations'], 1):
                output.append(f"  {i}. {rec}")
            output.append("")
        
        # Examples of issues found
        if clarity['passive_sentences']:
            output.append("📝 PASSIVE VOICE EXAMPLES:")
            for example in clarity['passive_sentences'][:3]:
                output.append(f"  • {example}")
            output.append("")
        
        if evidence['unsupported_claims_examples']:
            output.append("❓ UNSUPPORTED CLAIMS:")
            for example in evidence['unsupported_claims_examples'][:3]:
                output.append(f"  • {example}")
            output.append("")
        
        return [types.TextContent(type="text", text="\n".join(output))]
    
    elif name == "improve_writing":
        text = arguments.get("text", "")
        target_flesch = arguments.get("target_flesch_score", 60)
        
        result = improver.improve(text, target_flesch)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        # Format the improvement results
        output = []
        output.append("=== WRITING IMPROVEMENT REPORT ===\n")
        
        # Metrics comparison
        output.append("📊 METRICS COMPARISON:")
        metrics = result['metrics']
        output.append(f"  • Readability Score: {metrics['original']['flesch_score']} → {metrics['improved']['flesch_score']} ({metrics['improvements']['flesch_score_change']:+.1f})")
        output.append(f"  • Grade Level: {metrics['original']['grade_level']} → {metrics['improved']['grade_level']} ({metrics['improvements']['grade_level_change']:+.1f})")
        output.append(f"  • Word Count: {metrics['original']['word_count']} → {metrics['improved']['word_count']}")
        output.append(f"  • Passive Voice: {metrics['original']['passive_voice_percentage']}% → {metrics['improved']['passive_voice_percentage']}% ({metrics['improvements']['passive_voice_reduction']:+.1f}%)")
        output.append(f"  • Overall Score: {metrics['original']['overall_score']} → {metrics['improved']['overall_score']} ({metrics['improvements']['overall_score_change']:+d})")
        output.append("")
        
        # Changes made
        if result['changes_made']:
            output.append(f"🔧 CHANGES MADE ({result['changes_count']}):")
            for i, change in enumerate(result['changes_made'], 1):
                output.append(f"  {i}. {change}")
            output.append("")
        
        # Improved text
        output.append("📝 IMPROVED TEXT:")
        output.append("-" * 50)
        output.append(result['improved_text'])
        output.append("-" * 50)
        
        return [types.TextContent(type="text", text="\n".join(output))]
        
    elif name == "compare_writing_versions":
        original_text = arguments.get("original_text", "")
        revised_text = arguments.get("revised_text", "")
        
        # Analyze both versions
        original_analysis = analyzer.analyze(original_text)
        revised_analysis = analyzer.analyze(revised_text)
        
        if "error" in original_analysis:
            return [types.TextContent(type="text", text=f"Error analyzing original text: {original_analysis['error']}")]
        if "error" in revised_analysis:
            return [types.TextContent(type="text", text=f"Error analyzing revised text: {revised_analysis['error']}")]
        
        # Compare metrics
        output = []
        output.append("=== WRITING VERSION COMPARISON ===\n")
        
        output.append("📊 METRICS COMPARISON:")
        output.append(f"  • Readability Score: {original_analysis['readability']['flesch_reading_ease']} → {revised_analysis['readability']['flesch_reading_ease']} ({revised_analysis['readability']['flesch_reading_ease'] - original_analysis['readability']['flesch_reading_ease']:+.1f})")
        output.append(f"  • Grade Level: {original_analysis['readability']['flesch_kincaid_grade']} → {revised_analysis['readability']['flesch_kincaid_grade']} ({revised_analysis['readability']['flesch_kincaid_grade'] - original_analysis['readability']['flesch_kincaid_grade']:+.1f})")
        output.append(f"  • Word Count: {len(original_text.split())} → {len(revised_text.split())} ({len(revised_text.split()) - len(original_text.split()):+d})")
        output.append(f"  • Passive Voice: {original_analysis['clarity']['passive_voice_percentage']}% → {revised_analysis['clarity']['passive_voice_percentage']}% ({revised_analysis['clarity']['passive_voice_percentage'] - original_analysis['clarity']['passive_voice_percentage']:+.1f}%)")
        output.append(f"  • Overall Score: {original_analysis['overall_score']} → {revised_analysis['overall_score']} ({revised_analysis['overall_score'] - original_analysis['overall_score']:+d})")
        output.append("")
        
        # Quality improvements
        output.append("📈 QUALITY IMPROVEMENTS:")
        if revised_analysis['clarity']['vague_phrases_count'] < original_analysis['clarity']['vague_phrases_count']:
            output.append(f"  ✓ Reduced vague phrases: {original_analysis['clarity']['vague_phrases_count']} → {revised_analysis['clarity']['vague_phrases_count']}")
        if revised_analysis['clarity']['jargon_count'] < original_analysis['clarity']['jargon_count']:
            output.append(f"  ✓ Reduced jargon: {original_analysis['clarity']['jargon_count']} → {revised_analysis['clarity']['jargon_count']}")
        if revised_analysis['evidence']['unsupported_claims_count'] < original_analysis['evidence']['unsupported_claims_count']:
            output.append(f"  ✓ Fewer unsupported claims: {original_analysis['evidence']['unsupported_claims_count']} → {revised_analysis['evidence']['unsupported_claims_count']}")
        output.append("")
        
        return [types.TextContent(type="text", text="\n".join(output))]
    
    elif name == "comprehensive_readability_analysis":
        text = arguments.get("text", "")
        result = readability_analyzer.comprehensive_readability_analysis(text)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        # Format comprehensive readability report
        output = []
        output.append("=== COMPREHENSIVE READABILITY ANALYSIS ===\n")
        
        # Basic statistics
        stats = result["basic_stats"]
        output.append("📊 BASIC STATISTICS:")
        output.append(f"  • Words: {stats['word_count']}")
        output.append(f"  • Sentences: {stats['sentence_count']}")
        output.append(f"  • Syllables: {stats['syllable_count']}")
        output.append(f"  • Average sentence length: {stats['avg_sentence_length']} words")
        output.append(f"  • Average word length: {stats['avg_word_length']} characters")
        output.append(f"  • Average syllables per word: {stats['avg_syllables_per_word']}")
        output.append("")
        
        # Readability scores
        scores = result["readability_scores"]
        output.append("📖 READABILITY SCORES:")
        for metric, score in scores.items():
            output.append(f"  • {metric.replace('_', ' ').title()}: {score}")
        output.append("")
        
        # Reading times
        times = result["reading_times"]
        output.append("⏱️ READING TIME ESTIMATES:")
        for level, time_data in times.items():
            output.append(f"  • {level.replace('_', ' ').title()}: {time_data['minutes']} min ({time_data['seconds']} sec)")
        output.append("")
        
        # Complexity analysis
        complexity = result["complexity_analysis"]
        output.append("🔍 COMPLEXITY ANALYSIS:")
        output.append(f"  • Average complexity score: {complexity['average_complexity']}")
        output.append(f"  • Maximum complexity: {complexity['max_complexity']}")
        output.append(f"  • Complexity variance: {complexity['complexity_variance']}")
        output.append("")
        
        # Vocabulary analysis
        vocab = result["vocabulary_analysis"]
        output.append("📚 VOCABULARY ANALYSIS:")
        output.append(f"  • Total words: {vocab['total_words']}")
        output.append(f"  • Unique words: {vocab['unique_words']}")
        output.append(f"  • Vocabulary diversity: {vocab['vocabulary_diversity']}")
        output.append(f"  • Complex words: {vocab['complex_words']} ({vocab['complex_word_percentage']}%)")
        output.append("")
        
        # Overall assessment
        assessment = result["overall_assessment"]
        output.append("🎯 OVERALL ASSESSMENT:")
        output.append(f"  • Level: {assessment['overall_level']}")
        output.append(f"  • Primary score: {assessment['primary_score']}")
        output.append(f"  • Target met: {'✓' if assessment['target_met'] else '✗'}")
        
        return [types.TextContent(type="text", text="\n".join(output))]
    
    elif name == "flesch_reading_ease_detailed":
        text = arguments.get("text", "")
        result = readability_analyzer.flesch_reading_ease_detailed(text)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        # Format detailed Flesch analysis
        output = []
        output.append("=== FLESCH READING EASE DETAILED ANALYSIS ===\n")
        
        output.append(f"📊 FLESCH READING EASE SCORE: {result['flesch_reading_ease']}")
        output.append(f"🎯 TARGET RANGE: {result['target_range']}")
        output.append("")
        
        # Interpretation
        interp = result["interpretation"]
        output.append("📖 INTERPRETATION:")
        output.append(f"  • Level: {interp['level']}")
        output.append(f"  • Grade: {interp['description']}")
        output.append(f"  • Audience: {interp['audience']}")
        output.append("")
        
        # Score breakdown
        breakdown = result["score_breakdown"]
        output.append("🔢 SCORE BREAKDOWN:")
        output.append(f"  • Base score: {breakdown['base_score']}")
        output.append(f"  • Sentence length penalty: -{breakdown['sentence_length_penalty']}")
        output.append(f"  • Syllable complexity penalty: -{breakdown['syllable_complexity_penalty']}")
        output.append("")
        
        # Basic stats
        stats = result["basic_stats"]
        output.append("📈 CONTRIBUTING FACTORS:")
        output.append(f"  • Average sentence length: {stats['avg_sentence_length']} words")
        output.append(f"  • Average syllables per word: {stats['avg_syllables_per_word']}")
        output.append("")
        
        # Recommendations
        if result["recommendations"]:
            output.append("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(result["recommendations"], 1):
                output.append(f"  {i}. {rec}")
        
        return [types.TextContent(type="text", text="\n".join(output))]
    
    elif name == "grade_level_analysis":
        text = arguments.get("text", "")
        result = readability_analyzer.grade_level_analysis(text)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        # Format grade level analysis
        output = []
        output.append("=== GRADE LEVEL ANALYSIS ===\n")
        
        output.append(f"📊 AVERAGE GRADE LEVEL: {result['average_grade_level']}")
        output.append(f"🎯 TARGET: {result['target_grade_level']}")
        output.append("")
        
        # Individual metrics
        levels = result["grade_levels"]
        output.append("📈 GRADE LEVEL METRICS:")
        for metric, level in levels.items():
            output.append(f"  • {metric.replace('_', ' ').title()}: {level}")
        output.append("")
        
        # Interpretation
        interp = result["interpretation"]
        output.append("📖 INTERPRETATION:")
        output.append(f"  • Level: {interp['level']}")
        output.append(f"  • Description: {interp['description']}")
        output.append("")
        
        # Recommendations
        if result["recommendations"]:
            output.append("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(result["recommendations"], 1):
                output.append(f"  {i}. {rec}")
        
        return [types.TextContent(type="text", text="\n".join(output))]
    
    elif name == "reading_time_analysis":
        text = arguments.get("text", "")
        result = readability_analyzer.reading_time_analysis(text)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        # Format reading time analysis
        output = []
        output.append("=== READING TIME ANALYSIS ===\n")
        
        output.append(f"📄 WORD COUNT: {result['word_count']}")
        output.append(f"⏱️ AVERAGE READING TIME: {result['average_reading_time']}")
        output.append("")
        
        # Reading times by level
        times = result["reading_times_by_level"]
        output.append("📊 READING TIMES BY SKILL LEVEL:")
        for level, time_data in times.items():
            wpm = time_data['words_per_minute']
            minutes = time_data['minutes']
            output.append(f"  • {level.replace('_', ' ').title()}: {minutes} min ({wpm} WPM)")
        output.append("")
        
        # Difficulty assessment
        difficulty = result["difficulty_assessment"]
        output.append("🎯 DIFFICULTY ASSESSMENT:")
        output.append(f"  • Level: {difficulty['level'].title()}")
        output.append(f"  • Description: {difficulty['description']}")
        output.append("")
        
        # Recommendations
        if result["recommendations"]:
            output.append("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(result["recommendations"], 1):
                output.append(f"  {i}. {rec}")
        
        return [types.TextContent(type="text", text="\n".join(output))]
    
    elif name == "sentence_complexity_analysis":
        text = arguments.get("text", "")
        result = readability_analyzer.sentence_complexity_analysis(text)
        
        if "error" in result:
            return [types.TextContent(type="text", text=f"Error: {result['error']}")]
        
        # Format sentence complexity analysis
        output = []
        output.append("=== SENTENCE COMPLEXITY ANALYSIS ===\n")
        
        metrics = result["complexity_metrics"]
        output.append("📊 COMPLEXITY METRICS:")
        output.append(f"  • Total sentences: {metrics['total_sentences']}")
        output.append(f"  • Average length: {metrics['average_sentence_length']} words")
        output.append(f"  • Shortest sentence: {metrics['min_sentence_length']} words")
        output.append(f"  • Longest sentence: {metrics['max_sentence_length']} words")
        output.append("")
        
        # Complexity distribution
        distribution = metrics["complexity_distribution"]
        output.append("📈 COMPLEXITY DISTRIBUTION:")
        for category, data in distribution.items():
            output.append(f"  • {category.replace('_', ' ').title()}: {data['count']} ({data['percentage']}%)")
        output.append("")
        
        # Structural analysis
        structural = metrics["structural_analysis"]
        output.append("🔍 STRUCTURAL ANALYSIS:")
        output.append(f"  • Questions: {structural['questions']}")
        output.append(f"  • Exclamations: {structural['exclamations']}")
        output.append(f"  • Compound sentences: {structural['compound_sentences']}")
        output.append(f"  • Sentences with commas: {structural['sentences_with_commas']}")
        output.append(f"  • Sentences with semicolons: {structural['sentences_with_semicolons']}")
        output.append("")
        
        # Assessment
        assessment = result["assessment"]
        output.append("🎯 COMPLEXITY ASSESSMENT:")
        output.append(f"  • Level: {assessment['level'].title()}")
        output.append(f"  • Description: {assessment['description']}")
        output.append("")
        
        # Recommendations
        if result["recommendations"]:
            output.append("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(result["recommendations"], 1):
                output.append(f"  {i}. {rec}")
        
        return [types.TextContent(type="text", text="\n".join(output))]
    
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    # Import here to avoid issues if mcp is not available
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="writing-improvement",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())