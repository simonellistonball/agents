# Writing Improvement MCP Server

A Model Context Protocol (MCP) server that provides writing analysis and improvement tools directly to Claude Code. This server offers comprehensive writing quality assessment and automated improvements based on principles of clarity, accuracy, and readability.

## Features

### 🔧 Available Tools

1. **`analyze_writing`** - Comprehensive text analysis
   - Readability metrics (Flesch Reading Ease, grade level)
   - Clarity analysis (passive voice, vague phrases, jargon)
   - Structure assessment (paragraphs, transitions)
   - Evidence validation (unsupported claims, citations)
   - Overall quality score and recommendations

2. **`improve_writing`** - Automated text improvement
   - Language simplification (complex → simple words)
   - Vague phrase removal
   - Passive-to-active voice conversion
   - Sentence structure optimization
   - Citation need marking
   - Before/after metrics comparison

3. **`analyze_file_writing`** - File-based analysis
   - Read and analyze text files
   - Same comprehensive analysis as `analyze_writing`
   - File metadata included in report

4. **`improve_file_writing`** - File-based improvement
   - Read, improve, and optionally save improved text
   - All improvement features from `improve_writing`
   - Optional output file specification

5. **`compare_writing_versions`** - Version comparison
   - Side-by-side metrics comparison
   - Quality improvement tracking
   - Change analysis

### 📊 Reading Quality Metrics Tools

6. **`comprehensive_readability_analysis`** - Complete readability assessment
   - Multiple readability formulas (Flesch, Gunning Fog, SMOG, etc.)
   - Reading time estimates for different skill levels
   - Vocabulary complexity analysis
   - Sentence complexity patterns
   - Overall readability assessment

7. **`flesch_reading_ease_detailed`** - In-depth Flesch analysis
   - Detailed score breakdown and calculation
   - Score interpretation with audience recommendations
   - Contributing factor analysis
   - Specific improvement recommendations

8. **`grade_level_analysis`** - Multi-formula grade level assessment
   - Flesch-Kincaid Grade Level
   - Gunning Fog Index
   - SMOG Index
   - Automated Readability Index
   - Coleman-Liau Index
   - Average grade level with interpretation

9. **`reading_time_analysis`** - Reading time estimation
   - Time estimates for elementary through professional levels
   - Words-per-minute calculations by skill level
   - Difficulty impact on reading speed
   - Recommendations for optimal reading time

10. **`sentence_complexity_analysis`** - Sentence structure analysis
    - Complexity distribution (simple, moderate, complex, very complex)
    - Structural patterns (questions, compound sentences, punctuation usage)
    - Average, minimum, and maximum sentence lengths
    - Complexity assessment and recommendations

## Installation

### Prerequisites
- Python 3.8+
- Claude Code with MCP support

### Setup

1. **Clone or create the MCP server directory:**
   ```bash
   mkdir writing-improvement-mcp
   cd writing-improvement-mcp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Claude Code to use this MCP server:**
   Add to your Claude Code MCP configuration:
   ```json
   {
     "mcpServers": {
       "writing-improvement": {
         "command": "python",
         "args": ["/path/to/writing-improvement-mcp/server.py"]
       }
     }
   }
   ```

## Usage Examples

### Basic Text Analysis
```
User: Please analyze this text for writing quality:
"The implementation of our innovative methodological framework has potentially resulted in what might be considered a significant enhancement of various operational efficiency metrics."

Claude: I'll analyze this text for writing quality using the analyze_writing tool.

[Tool results show readability scores, clarity issues, recommendations]
```

### Text Improvement
```
User: Can you improve this paragraph for better readability?

Claude: I'll use the improve_writing tool to enhance your text.

[Tool results show improved version with change tracking]
```

### File Analysis
```
User: Analyze the writing quality of my report.txt file.

Claude: I'll analyze your report file using analyze_file_writing.

[Tool results show comprehensive file analysis]
```

### Reading Quality Analysis
```
User: Give me a detailed readability analysis of this text with multiple metrics.

Claude: I'll use the comprehensive_readability_analysis tool for a complete assessment.

[Tool results show Flesch scores, grade levels, reading times, complexity analysis]
```

### Flesch Score Analysis
```
User: I need a detailed breakdown of the Flesch Reading Ease score for this paragraph.

Claude: I'll use flesch_reading_ease_detailed to provide an in-depth analysis.

[Tool results show score calculation, interpretation, and recommendations]
```

## Quality Targets

- **Flesch Reading Ease**: 50-70 (suitable for general adult audience)
- **Passive Voice**: Less than 20% of sentences
- **Evidence**: All major claims supported by data or citations
- **Sentence Length**: Average 15-20 words
- **Paragraph Length**: 3-5 sentences

## Writing Principles

### 1. Clarity
- Remove ambiguous language and vague assertions
- Replace jargon with plain language where possible
- Use active voice over passive voice when appropriate

### 2. Accuracy
- Verify quantitative claims have proper context
- Ensure statements are properly qualified
- Maintain precision in numerical data

### 3. Evidence-Based Writing
- Every assertion supported by evidence
- Clear distinction between correlation and causation
- Proper citation of sources

### 4. Narrative Flow
- Clear thesis statements
- Logical progression of ideas
- Effective transitions between paragraphs

### 5. Readability
- Target appropriate reading level
- Break up complex information
- Never sacrifice accuracy for readability scores

## Technical Details

### Dependencies
- `mcp`: Model Context Protocol framework
- `textstat`: Readability and text statistics (optional fallback available)

### Architecture
```
writing-improvement-mcp/
├── server.py              # Main MCP server with 10 tools
├── tools/
│   ├── __init__.py
│   ├── analyzer.py        # WritingAnalyzer class
│   ├── improver.py        # WritingImprover class
│   └── readability.py     # ReadabilityAnalyzer class
├── requirements.txt       # Dependencies
├── test_server.py         # Test suite
└── README.md             # This file
```

### Error Handling
- Graceful fallback when textstat is unavailable
- Comprehensive error messages for file operations
- Input validation for all tools

## Example Output

### Analysis Report
```
=== WRITING ANALYSIS REPORT ===

📊 OVERALL SCORE: 72/100

📖 READABILITY METRICS:
  • Flesch Reading Ease: 45.2 (target: 50-70)
  • Grade Level: 12.3
  • Average Sentence Length: 18.5 words
  • Reading Time: 45 seconds

🔍 CLARITY ANALYSIS:
  • Passive Voice: 35% (4 sentences)
  • Vague Phrases: 8 (12.3%)
  • Jargon: 6 instances
  • Complex Sentences: 2

💡 RECOMMENDATIONS:
  1. Reduce passive voice usage (currently 35%)
  2. Replace vague phrases with specific language
  3. Add evidence to support 3 unsupported claims
```

### Comprehensive Readability Report
```
=== COMPREHENSIVE READABILITY ANALYSIS ===

📊 BASIC STATISTICS:
  • Words: 245
  • Sentences: 12
  • Syllables: 398
  • Average sentence length: 20.4 words
  • Average word length: 4.8 characters
  • Average syllables per word: 1.62

📖 READABILITY SCORES:
  • Flesch Reading Ease: 45.2
  • Flesch Kincaid Grade: 12.3
  • Gunning Fog: 14.8
  • SMOG Index: 13.1
  • Automated Readability Index: 12.7

⏱️ READING TIME ESTIMATES:
  • Elementary: 1.6 min (150 WPM)
  • College: 1.0 min (250 WPM)
  • Professional: 0.7 min (350 WPM)

🎯 OVERALL ASSESSMENT:
  • Level: Needs Improvement
  • Target met: ✗
```

### Improvement Report
```
=== WRITING IMPROVEMENT REPORT ===

📊 METRICS COMPARISON:
  • Readability Score: 45.2 → 62.1 (+16.9)
  • Grade Level: 12.3 → 9.8 (-2.5)
  • Passive Voice: 35% → 15% (-20%)
  • Overall Score: 72 → 85 (+13)

🔧 CHANGES MADE (7):
  1. Simplified 'utilize' → 'use' (3 instances)
  2. Vague phrase 'might potentially' replaced with 'may'
  3. Converted passive to active voice: 'was implemented by team'
  4. Split long sentence (42 words) at 'however'
  5. Marked unsupported claim: 'significantly improves...'
```

## Contributing

This MCP server follows defensive security practices:
- Input validation and sanitization
- Error handling for all file operations
- No execution of arbitrary code
- Read-only file access where possible

## License

This project is designed for educational and professional writing improvement purposes.