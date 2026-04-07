# Setting Up Competitive Intelligence Agent in Claude Desktop

This guide shows you how to use the Competitive Intelligence Research Agent in Claude Desktop or Claude Code.

## Option 1: Direct Agent Conversation (Easiest)

### Step 1: Copy Agent Instructions
Copy the content from `competitive-research.md` and paste it at the start of a new Claude Desktop conversation:

```
Paste the entire competitive-research.md content here, then ask:

"Please analyze competitors: Slack, Microsoft Teams, and Discord. Focus on features and pricing."
```

### Step 2: Start Research
The agent will systematically research each competitor using web search and provide comprehensive analysis.

## Option 2: Claude Desktop Agent Configuration

### Step 1: Add to Claude Desktop Config
1. Open Claude Desktop settings
2. Go to "Agents" or "Custom Instructions" 
3. Create new agent with these settings:
   - **Name**: Competitive Intelligence Research Agent
   - **Instructions**: Copy content from `competitive-research.md`
   - **Tools**: Enable web search, file editing

### Step 2: Use the Agent
Start conversations with the agent using prompts like:
- "Analyze competitors: [Company A], [Company B], [Company C]"
- "Research pricing strategies for [market/industry]"
- "Find customer sentiment for [product] vs [competitor]"

## Option 3: Claude Code Slash Command

### Step 1: Add Slash Command
1. Save `competitive-analysis.md` to your Claude Code slash commands directory
2. Use in Claude Code with: `/competitive-analysis Company1 Company2 --focus features`

### Step 2: Run Analysis
The command will execute comprehensive competitive research and generate reports.

## Usage Examples

### Basic Competitive Analysis
```
Research these project management tools and provide a feature comparison:
- Notion
- Obsidian  
- Roam Research

Focus on collaboration features and pricing models.
```

### Market Entry Research
```
I'm considering entering the video conferencing market. 
Analyze these key competitors:
- Zoom
- Google Meet
- Microsoft Teams

Provide SWOT analysis and identify market gaps.
```

### Customer Intelligence
```
Research customer sentiment and key customers for:
- Figma
- Sketch
- Adobe XD

Include review analysis and identify promoters/detractors.
```

### Financial Analysis
```
Conduct comprehensive financial analysis on:
- Salesforce
- HubSpot
- Pipedrive

Focus on funding history, revenue growth, profitability, and recent financial performance. For public companies, analyze the last 3 years of financial reports.
```

### Pricing Strategy Analysis
```
Compare pricing strategies across these CRM platforms:
- HubSpot
- Salesforce
- Pipedrive

Focus on pricing models, tiers, and value positioning.
```

## Expected Outputs

The agent will provide structured reports including:

### Executive Summary
- Market landscape overview
- Key competitive findings
- Strategic implications
- Opportunity identification

### Detailed Competitor Profiles  
- Company overview and positioning
- Product features and capabilities
- Pricing and business model
- Customer base and sentiment
- Strengths and weaknesses
- Financial health and funding history
- Public company financial analysis (3-year trends)

### Comparative Analysis
- Feature comparison matrices
- Gap analysis
- Market positioning maps
- Sentiment analysis summaries
- Financial performance comparisons
- Valuation and growth analysis

### Strategic Insights
- Competitive advantages/disadvantages
- Market opportunities
- Threat assessment
- Recommended next steps

## Research Quality

The agent will:
- ✅ Use systematic web search across multiple sources
- ✅ Verify information across multiple sources  
- ✅ Provide balanced analysis (strengths + weaknesses)
- ✅ Include quantitative data where available
- ✅ Focus on recent, current information
- ✅ Present findings in professional report format
- ✅ Offer actionable strategic recommendations

## Tips for Best Results

1. **Be Specific**: Name exact competitors and focus areas
2. **Set Context**: Explain your use case or decision context  
3. **Ask Follow-ups**: Request deeper analysis on specific findings
4. **Verify Critical Info**: Cross-check important competitive claims
5. **Update Regularly**: Competitive landscapes change quickly

## Advanced Usage

### Custom Research Focus
- "Focus research on enterprise customers and pricing"
- "Emphasize technical capabilities and integrations"
- "Prioritize customer satisfaction and support quality"

### Industry-Specific Analysis
- "Research with focus on healthcare compliance requirements"
- "Analyze from enterprise security perspective"
- "Consider SMB budget and ease-of-use factors"

### Strategic Context
- "We're planning market entry in Q2 2024"
- "Looking to differentiate on pricing strategy"
- "Considering acquisition targets in this space"

This agent is designed to provide professional-grade competitive intelligence that enables better strategic decision-making. Start with basic competitor analysis and gradually explore more sophisticated research as you become familiar with the capabilities.