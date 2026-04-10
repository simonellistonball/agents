---
name: competitive-analysis
description: >
  Competitive intelligence skill that researches competitors via web search, stores
  structured profiles locally, and maintains knowledge about your own products for
  comparison. Use when the user asks to analyze a competitor, compare products, research
  a company's features/pricing/positioning, build a competitive landscape, or update
  existing competitor intelligence. Also trigger when the user mentions competitor names
  in the context of strategy, positioning, or market research — even if they don't
  explicitly say "competitive analysis."
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Competitive Analysis Skill

Research competitors, maintain structured intelligence files, and compare against your own products — all persisted locally for use across sessions.

## Critical Workflow Principle

The deliverable is the **analysis**, not the research. Source gathering, web fetching, and archiving are means to an end — the competitor profile, comparison report, or landscape document is what the user needs. Every workflow must end with a complete, written deliverable. If you've gathered sources but haven't yet written the profile/comparison/landscape, you are not done.

Structured data hygiene (YAML frontmatter, source citations, archived pages) is important, but it must serve actionable strategic analysis. Every profile should tell the user something they can act on — not just list facts. The Strengths/Weaknesses sections should explain *why* something is a strength or weakness relative to the user's product. The Strategic Implications and Opportunities sections are where the real value lives.

## Storage Structure

There are two directories: a hidden data store and a visible reports directory.

**Data store** (`.competitive-intel/`) — structured data, source archives, raw profiles:

```
.competitive-intel/
├── my-products/
│   └── <product-name>.md       # Your own product profiles
├── competitors/
│   └── <company-name>.md       # Competitor profiles
├── comparisons/
│   └── <date>-<slug>.md        # Saved comparison reports
├── sources/
│   └── <company-name>/
│       └── <date>-<slug>.md    # Archived source material (fetched pages, filings, etc.)
└── landscape.md                # Current competitive landscape overview
```

**Reports directory** (`competitive-intel-reports/`) — browsable output for non-technical stakeholders:

```
competitive-intel-reports/
├── dashboard.md                # Links to all reports, latest state overview
├── dashboard.html              # Interactive HTML version of dashboard
└── reports/
    ├── <date>-analysis-<company>.md
    ├── <date>-analysis-<company>.html
    ├── <date>-comparison-<x>-vs-<y>.md
    ├── <date>-comparison-<x>-vs-<y>.html
    ├── <date>-landscape.md
    └── <date>-landscape.html
```

Each file in `.competitive-intel/` uses YAML frontmatter for structured metadata and markdown body for narrative detail. This makes them both human-readable and machine-parseable. The `competitive-intel-reports/` directory contains presentation-ready versions designed for sharing.

## Before Every Workflow

Before starting any workflow, check whether you know who the user is and what their product is:

1. **Check for existing product profiles**: Look in `.competitive-intel/my-products/` for any files. If one or more exist, you know who the user is.
2. **If no product profile exists**: Use AskUserQuestion to ask who they are and what their product/company is before proceeding. You need this context to frame the analysis — competitive intelligence is always relative to a position in the market. Ask:
   - What is your company/product?
   - Brief description of what it does
   - Who are your primary customers?
   
   Save their answer to `.competitive-intel/my-products/<name>.md` using the my-product template, then continue with the requested workflow.

This only needs to happen once — after the first run, the product profile persists and you can read it at the start of future sessions.

## Workflows

### 1. Analyze a Competitor

When the user asks to analyze or research a competitor:

**First, ask about depth and focus:**

Use AskUserQuestion to ask two things:

1. **Research depth:**
   - **Quick scan** (~3-5 searches): Positioning, key features, pricing model, target market
   - **Standard analysis** (~8-12 searches): Above + customer reviews, recent news, tech stack hints, integrations
   - **Deep dive** (~15-20 searches): Above + financials/funding, hiring signals, content strategy, partnership ecosystem, executive team

2. **Focus area** (optional): Ask whether they want to focus on a particular feature area, product line, or capability — or do a broad analysis. Examples: "their AI/ML features", "enterprise security posture", "developer experience", "their data pipeline product". If the user specifies a focus, weight research and the resulting profile toward that area. A focused analysis produces more actionable intel than a shallow pass over everything.

**Then research systematically:**

1. **Company basics**: Search for official website, about page, product pages
2. **Product & features**: Search for feature lists, documentation, product pages
3. **Pricing**: Search for pricing page, pricing model discussions, comparison sites
4. **Positioning**: How they describe themselves, taglines, messaging on homepage
5. **Press releases & statements** (all depths): Search for recent press releases, CEO/exec statements, company blog announcements. These are primary sources — prioritize them over third-party summaries
6. **Leadership & people moves** (all depths): Search for recent executive hires, departures, board changes, and C-suite appointments. New hires signal strategic direction (e.g., a new Chief AI Officer means an AI push; a new CRO from enterprise suggests upmarket motion). Board additions often foreshadow funding rounds or IPO prep. Search patterns:
   - `"<Company>" "joins as" OR "appointed" OR "named" OR "welcomes"`
   - `"<Company>" board OR "board of directors" appointment`
   - `"<Company>" CEO OR CTO OR CPO OR CFO OR CRO`
   - `site:linkedin.com "<Company>" "excited to announce" OR "thrilled to join"`
7. **Customer sentiment** (standard+): Search G2, Capterra, Reddit for reviews
8. **Recent developments** (standard+): News, blog posts, product launches
9. **Funding & financial signals** (standard+): Applies differently by company type:
   - **Private companies**: Search for funding rounds, valuations, lead investors, runway estimates. Sources: Crunchbase, PitchBook, TechCrunch, press releases. Funding announcements often include strategic context about what the money will be used for — capture that.
     - `"<Company>" "series" OR "funding" OR "raised" OR "valuation"`
     - `"<Company>" site:crunchbase.com OR site:techcrunch.com`
     - `"<Company>" investors OR "led by" OR "participated"`
   - **Public companies**: Search for 10-K, 10-Q, earnings call transcripts, investor presentations. SEC EDGAR is the authoritative source. Earnings calls often reveal strategic direction, competitive positioning, and product roadmap hints that aren't published anywhere else
     - `site:sec.gov "<Company>" 10-K OR 10-Q`
     - `"<Company>" earnings call transcript <year>`
10. **Industry analyst coverage** (standard+): Search for analyst reports, market maps, and vendor evaluations from firms covering this company's space. These provide third-party validation of positioning and often reveal market share estimates and competitive rankings not available elsewhere.
    - **Major firms**: Gartner (Magic Quadrant, Hype Cycle), IDC (MarketScape), Forrester (Wave), G2 Grid
    - **Sector-specific analysts**: Identify analysts who specialize in the relevant industry — every market has its recognized voices (e.g., Redmonk for developer tools, CB Insights for fintech, Pitchbook for VC-backed companies)
    - Search for the company in the context of these reports, not just the reports themselves — summaries, commentary, and vendor responses often surface even when the full report is paywalled
    - `"<Company>" Gartner OR "Magic Quadrant" OR Forrester OR "Wave" OR IDC` — major analyst mentions
    - `"<Company>" "market leader" OR "leader quadrant" OR "strong performer"` — positioning in analyst frameworks
    - `"<Company>" analyst OR "industry report" OR "market landscape" <industry>` — broader analyst coverage
    - `"<Company>" "<industry>" market share OR ranking OR comparison` — competitive ranking data
    - When reports are paywalled, capture: which report, which firm, the company's placement/ranking, date published, and any publicly available summary or vendor response
11. **Deep financials** (deep dive): Revenue estimates, growth projections, market share analysis, analyst ratings
12. **Hiring patterns** (deep dive): Job postings for tech stack, strategic bets, and geographic expansion signals

**Archive sources as you go** — when you fetch a page with WebFetch, immediately save the relevant content to `.competitive-intel/sources/<company-name>/`. Don't batch this for later.

**Then write the competitor profile** to `.competitive-intel/competitors/<company-name>.md` using the competitor profile template below. This is the primary deliverable — do not finish without writing it. The profile should synthesize your research into actionable intelligence, not just list facts. Strengths and weaknesses should be framed relative to the user's own product. Include strategic interpretation: what does this competitor's positioning mean for us?

**If a profile already exists**, read it first and update it rather than replacing it. Note what changed with a dated entry in the "Update History" section.

**Finally, generate reports**: Create the per-run report (markdown + HTML) in `competitive-intel-reports/reports/` and update the dashboard. See "Presenting Results" section for details.

### 2. Compare Products

When the user asks to compare a competitor with their product, this workflow must produce **two deliverables**: a competitor profile AND a comparison report. Both are required.

1. **Check for existing data**: Read the competitor profile from `.competitive-intel/competitors/` and the user's product from `.competitive-intel/my-products/`
2. **If no "my product" file exists**: Ask the user to describe their product — what it does, key features, target market, pricing model, key differentiators. Save to `.competitive-intel/my-products/<name>.md`
3. **Fill gaps**: If the competitor profile is missing or thin, run the Analyze workflow first (ask about depth/focus, research, archive sources, write the full profile to `.competitive-intel/competitors/`)
4. **Generate the comparison report** using the comparison template below. This is the second required deliverable. The comparison should be analytical and opinionated — not just a neutral feature matrix. Tell the user where they win, where they lose, and what to do about it. Include:
   - A feature comparison table with clear "Edge" column
   - Strategic implications: what does this mean for product roadmap, sales positioning, pricing?
   - Specific opportunities: concrete actions the user can take based on the competitor's weaknesses
5. **Save** to `.competitive-intel/comparisons/<date>-<competitor>-vs-<product>.md`

Do not finish this workflow without writing both the competitor profile AND the comparison report. If the user asked to compare, they expect a comparison document — a profile alone is not enough.

**Finally, generate reports**: Create the per-run report (markdown + HTML) in `competitive-intel-reports/reports/` and update the dashboard. The comparison report is the primary content for the per-run report.

### 3. Update Competitor Info

When the user asks to update or refresh competitor data:

1. Read the existing profile
2. Search for recent news, product updates, pricing changes
3. Update the profile in place, adding a dated entry to "Update History"
4. Summarize what changed
5. Update the dashboard to reflect new last-updated dates

### 4. Show Competitive Landscape

When the user asks for an overview or landscape view, the deliverable is a **landscape.md synthesis document** — not just a collection of individual profiles. The landscape document should tell the user: who are all the players, how do they position, where do we stand, what's changing, and what should we do about it.

1. Read all competitor profiles from `.competitive-intel/competitors/`
2. Read the user's product profiles from `.competitive-intel/my-products/`
3. **Actively discover competitors beyond the obvious ones**. Search broadly for the market category:
   - `"<industry>" competitors OR alternatives OR landscape` — market overviews
   - `"<industry>" emerging OR "up and coming" OR "to watch"` — emerging players
   - `"<industry>" open source OR free alternative` — open source threats
   - `"<industry>" market share OR market map` — analyst landscape views
   - Think in tiers: Tier 1 (direct competitors), Tier 2 (niche/segment competitors), Tier 3 (emerging/watch-list). Also consider adjacent threats — platforms, tools, or trends that could disrupt the category entirely.
   - Aim for 8-12+ competitors across all tiers. If you only find 3-4, you haven't searched broadly enough.
4. For each newly discovered competitor, create a profile in `.competitive-intel/competitors/` with proper citations and archived sources — the same source archival discipline applies here as in individual analyses. Archive fetched pages to `.competitive-intel/sources/<company-name>/`.
5. **Generate or update `.competitive-intel/landscape.md`** — this is the primary deliverable and must include:
   - Executive summary (2-3 paragraphs)
   - Market map: who competes where, organized by tiers and threat level
   - Positioning matrix: how each player positions (text-based visual if possible)
   - Where we win / where we lose / where we're vulnerable
   - Key trends across competitors (5-7 trends with implications for our product)
   - Gaps and opportunities: specific, actionable things we could do based on competitive gaps
   - Competitive blind spots to monitor
   - Sources section with numbered references

Do not finish without writing landscape.md. Individual profiles are supporting material; the landscape synthesis is the deliverable.

**Finally, generate reports**: Create the per-run report (markdown + HTML) in `competitive-intel-reports/reports/` and update the dashboard. The landscape synthesis is the primary content for the per-run report. The dashboard should include cards for all discovered competitors.

### 5. Define My Product

When the user wants to add or update their own product info:

1. If creating new: ask what the product does, key features, target market, pricing, differentiators
2. Save to `.competitive-intel/my-products/<product-name>.md` using the my-product template
3. If updating: read existing file and update specific sections

## Presenting Results

Every workflow (analyze, compare, landscape) must end by generating browsable reports in `competitive-intel-reports/`. The `.competitive-intel/` directory is the data layer; the reports directory is the presentation layer for non-technical stakeholders.

### Per-Run Reports

After completing any workflow, generate **both** a markdown and HTML report:

1. **Markdown report**: Save to `competitive-intel-reports/reports/<date>-<type>-<name>.md`
   - `<type>` is one of: `analysis`, `comparison`, `landscape`
   - This is a clean, readable summary — not a copy of the raw profile. It should:
     - Lead with an executive summary (3-5 bullet points of the most important findings)
     - Include the key strategic takeaways, framed for decision-makers
     - Include the most important data (feature tables, pricing comparisons) inline
     - End with recommended next steps or actions
     - Not include raw YAML frontmatter, archive paths, or other technical details
     - Include a "Sources" section, but simplified: just numbered descriptions with URLs — no archive paths

2. **HTML report**: Save to `competitive-intel-reports/reports/<date>-<type>-<name>.html`
   - A self-contained, single-file HTML page (all CSS inline) that looks professional
   - Use the HTML report template below
   - Should be directly shareable — someone can open it in a browser with no dependencies

### Dashboard

After generating a per-run report, update the dashboard files:

1. **`competitive-intel-reports/dashboard.md`**: A markdown index listing:
   - Your product(s) (name + one-liner from my-products)
   - All tracked competitors with last-updated date and one-line summary
   - Links to all reports, newest first
   - Latest landscape summary (if one exists)

2. **`competitive-intel-reports/dashboard.html`**: An HTML version of the dashboard with:
   - Clean navigation to all reports
   - Competitor cards showing name, category, threat level, last updated
   - Links to individual report HTML files
   - Use the HTML dashboard template below

### HTML Report Template

Generate self-contained HTML reports using this structure. Adapt the content sections based on report type (analysis/comparison/landscape).

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{REPORT_TITLE}}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a2e; background: #f8f9fa; padding: 2rem; max-width: 960px; margin: 0 auto; }
  h1 { font-size: 1.8rem; margin-bottom: 0.5rem; color: #1a1a2e; }
  h2 { font-size: 1.3rem; margin-top: 2rem; margin-bottom: 0.75rem; color: #2d3748; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.3rem; }
  h3 { font-size: 1.1rem; margin-top: 1.5rem; margin-bottom: 0.5rem; color: #4a5568; }
  .meta { color: #718096; font-size: 0.9rem; margin-bottom: 2rem; }
  .executive-summary { background: #edf2f7; border-left: 4px solid #4299e1; padding: 1rem 1.5rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0; }
  .executive-summary ul { margin-left: 1.2rem; }
  .executive-summary li { margin-bottom: 0.4rem; }
  .win { color: #276749; font-weight: 600; }
  .lose { color: #9b2c2c; font-weight: 600; }
  .tie { color: #975a16; font-weight: 600; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9rem; }
  th { background: #2d3748; color: white; padding: 0.6rem 0.8rem; text-align: left; }
  td { padding: 0.5rem 0.8rem; border-bottom: 1px solid #e2e8f0; }
  tr:hover { background: #f7fafc; }
  .opportunity { background: #f0fff4; border-left: 3px solid #48bb78; padding: 0.8rem 1rem; margin: 0.8rem 0; border-radius: 0 4px 4px 0; }
  .threat { background: #fff5f5; border-left: 3px solid #fc8181; padding: 0.8rem 1rem; margin: 0.8rem 0; border-radius: 0 4px 4px 0; }
  .sources { font-size: 0.85rem; color: #718096; margin-top: 2rem; }
  .sources a { color: #4299e1; }
  .back-link { display: inline-block; margin-bottom: 1rem; color: #4299e1; text-decoration: none; font-size: 0.9rem; }
  .back-link:hover { text-decoration: underline; }
  @media print { body { padding: 1rem; } .back-link { display: none; } }
</style>
</head>
<body>
<a href="dashboard.html" class="back-link">← Back to Dashboard</a>
<h1>{{REPORT_TITLE}}</h1>
<div class="meta">{{DATE}} · {{REPORT_TYPE}} · Prepared for {{USER_PRODUCT}}</div>

<div class="executive-summary">
<h3>Executive Summary</h3>
<ul>
{{EXECUTIVE_SUMMARY_BULLETS}}
</ul>
</div>

{{REPORT_BODY_SECTIONS}}

<div class="sources">
<h2>Sources</h2>
{{SOURCES_LIST}}
</div>
</body>
</html>
```

### HTML Dashboard Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Competitive Intelligence Dashboard</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1a1a2e; background: #f8f9fa; padding: 2rem; max-width: 1100px; margin: 0 auto; }
  h1 { font-size: 1.8rem; margin-bottom: 0.3rem; }
  .subtitle { color: #718096; margin-bottom: 2rem; }
  h2 { font-size: 1.3rem; margin-top: 2rem; margin-bottom: 0.75rem; color: #2d3748; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.3rem; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin: 1rem 0; }
  .card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.2rem; }
  .card h3 { font-size: 1rem; margin-bottom: 0.3rem; }
  .card .category { font-size: 0.8rem; color: #718096; }
  .card .updated { font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem; }
  .threat-high { border-left: 4px solid #fc8181; }
  .threat-medium { border-left: 4px solid #f6ad55; }
  .threat-low { border-left: 4px solid #68d391; }
  .report-list { list-style: none; }
  .report-list li { padding: 0.6rem 0; border-bottom: 1px solid #edf2f7; }
  .report-list a { color: #4299e1; text-decoration: none; font-weight: 500; }
  .report-list a:hover { text-decoration: underline; }
  .report-list .date { color: #a0aec0; font-size: 0.85rem; margin-left: 0.5rem; }
  .report-list .type { display: inline-block; font-size: 0.75rem; padding: 0.1rem 0.5rem; border-radius: 3px; margin-left: 0.5rem; }
  .type-analysis { background: #ebf8ff; color: #2b6cb0; }
  .type-comparison { background: #fefcbf; color: #975a16; }
  .type-landscape { background: #f0fff4; color: #276749; }
  .my-product { background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1.5rem; }
</style>
</head>
<body>
<h1>Competitive Intelligence Dashboard</h1>
<p class="subtitle">Last updated: {{DATE}}</p>

<div class="my-product">
<h3>Our Product: {{PRODUCT_NAME}}</h3>
<p>{{PRODUCT_DESCRIPTION}}</p>
</div>

<h2>Tracked Competitors</h2>
<div class="card-grid">
{{COMPETITOR_CARDS}}
<!-- Example card:
<div class="card threat-high">
  <h3>Competitor Name</h3>
  <div class="category">Category · Stage</div>
  <p style="font-size:0.9rem; margin-top:0.5rem;">One-line competitive summary</p>
  <div class="updated">Last updated: 2026-04-10</div>
</div>
-->
</div>

<h2>Reports</h2>
<ul class="report-list">
{{REPORT_LINKS}}
<!-- Example:
<li>
  <a href="reports/2026-04-10-analysis-unreal-engine.html">Unreal Engine Analysis</a>
  <span class="type type-analysis">Analysis</span>
  <span class="date">2026-04-10</span>
</li>
-->
</ul>
</body>
</html>
```

When populating these templates:
- Read the competitor profiles to extract name, category, stage, and a one-line positioning summary for the dashboard cards
- Set threat level classes based on competitive threat (Tier 1 = high, Tier 2 = medium, Tier 3 = low)
- List reports newest-first
- For report body sections, convert markdown headings and tables to HTML equivalents (h2/h3 for headings, proper table elements)
- Use the `.opportunity` and `.threat` CSS classes to highlight key findings visually
- Use `.win`, `.lose`, `.tie` classes in feature comparison table Edge columns

## Templates

### Competitor Profile Template

```markdown
---
name: "<Company Name>"
url: "<website>"
ticker: "<stock ticker, if public>"
last_updated: "<YYYY-MM-DD>"
category: "<market category>"
stage: "<startup/growth/enterprise/public>"
funding: "<total funding or 'public'>"
employees: "<estimate or range>"
focus_area: "<specific focus if requested, or 'broad'>"
---

# <Company Name>

## Positioning
<!-- How they describe themselves, their tagline, core value prop [cite source] -->

## Product Overview
<!-- What they sell, core capabilities [cite source] -->

## Key Features
<!-- Bulleted list of notable features [cite sources] -->

## Pricing
<!-- Pricing model, tiers, notable details [cite source] -->

## Target Market
<!-- Who they sell to, segments, personas [cite source] -->

## Strengths
<!-- What they do well, competitive advantages [cite sources] -->

## Weaknesses
<!-- Known limitations, common complaints, gaps [cite sources] -->

## Customer Sentiment
<!-- Summary of reviews, NPS signals, common praise/complaints [cite sources] -->

## Leadership & Key People
<!-- CEO, CTO, CPO, and other key execs. Note recent hires/departures 
     and what they signal strategically. Board composition and recent 
     changes. [cite sources] -->

## Recent Developments
<!-- Latest news, launches, pivots, acquisitions [cite sources] -->

## Press Releases & Official Statements
<!-- Key recent press releases, exec quotes, official announcements [cite sources] -->

## Analyst Coverage
<!-- Mentions in Gartner Magic Quadrant, Forrester Wave, IDC MarketScape, G2 Grid,
     or sector-specific analyst reports. Note: placement/ranking, report name, date,
     and any publicly available summary. If paywalled, record what's known from 
     public commentary or vendor response. [cite sources] -->

## Financial Overview
<!-- For public companies: key metrics from latest filings/earnings.
     For private: funding rounds (amount, date, lead investor, valuation 
     if known), total funding, last known valuation, known revenue estimates.
     Always cite the specific filing or source. [cite sources] -->

## Sources
<!-- Numbered list of all sources cited in this profile -->
[1] <Description> — fetched <YYYY-MM-DD>
    URL: <url>
    Archived: <path to archived copy, if saved>

## Update History
<!-- Dated entries tracking when this profile was researched/updated -->
- <YYYY-MM-DD>: Initial research (<depth>, focus: <area or 'broad'>)
```

### My Product Template

```markdown
---
name: "<Product Name>"
url: "<website>"
last_updated: "<YYYY-MM-DD>"
category: "<market category>"
stage: "<stage>"
---

# <Product Name>

## What It Does
<!-- Core product description -->

## Key Features
<!-- Your main features and capabilities -->

## Pricing
<!-- Your pricing model -->

## Target Market
<!-- Who you sell to -->

## Key Differentiators
<!-- What makes you different/better -->

## Known Gaps
<!-- Areas where you know you're behind -->
```

### Comparison Template

```markdown
---
date: "<YYYY-MM-DD>"
my_product: "<your product>"
competitor: "<competitor name>"
---

# <Your Product> vs <Competitor>

## Summary
<!-- 2-3 sentence bottom line -->

## Feature Comparison

| Category | <Your Product> | <Competitor> | Edge |
|----------|---------------|--------------|------|
| ... | ... | ... | Us/Them/Tie |

## Where We Win
<!-- Areas of clear advantage -->

## Where They Win
<!-- Areas where competitor is stronger -->

## Pricing Comparison
<!-- Side-by-side pricing analysis -->

## Strategic Implications
<!-- What this means for positioning, roadmap, sales -->

## Opportunities
<!-- Gaps we could exploit, weaknesses to target -->

## Sources
<!-- Numbered references for any new research done for this comparison -->
```

## Source Citation & Archival

Every claim in a competitor profile or comparison must trace back to a source. This is non-negotiable — competitive intelligence without provenance is just opinion.

### Inline Citation

Every factual claim in a profile should cite its source inline using footnote-style references:

```markdown
Revenue grew 34% YoY to $1.2B in FY2025 [1].
They launched their AI copilot feature in Q3 2025 [2].

## Sources
[1] FY2025 10-K Annual Report, filed 2025-03-15 — fetched 2026-04-10
    URL: https://sec.gov/...
    Archived: .competitive-intel/sources/acme-corp/2026-04-10-10k-fy2025.md
[2] Acme Corp Blog, "Introducing Acme AI Copilot" — fetched 2026-04-10
    URL: https://blog.acme.com/ai-copilot-launch
    Archived: .competitive-intel/sources/acme-corp/2026-04-10-ai-copilot-announcement.md
```

### Source Archival

When you fetch a page using WebFetch during research, save the key content to `.competitive-intel/sources/<company-name>/<date>-<slug>.md`. This serves as backup material — URLs go stale, pages get updated, pricing pages change. The archived version is your evidence.

Each archived source file should have this structure:

```markdown
---
url: "<original URL>"
fetched: "<YYYY-MM-DD>"
type: "<webpage|filing|earnings-call|press-release|review-site|blog-post>"
company: "<company name>"
---

# <Page Title>

<!-- Key extracted content from the page. Not a full mirror — just the relevant 
     facts, quotes, data points, and context that support claims in the profile. -->
```

Don't archive every page you glance at — archive the ones you actually cite or that contain substantive data you'd want to reference later.

### Source Log

Every competitor profile, comparison, and landscape document must end with a **Sources** section listing all references with:
- Source number (matching inline citations)
- Description of what it is
- URL
- Date fetched — always use the format `fetched YYYY-MM-DD` with today's date, even if web tools are unavailable. Never use "knowledge as of" or other variant formats. Consistency matters for programmatic parsing.
- Path to archived copy (if archived)

## Research Guidelines

### Web Search Strategies

Use varied search patterns to get comprehensive coverage:
- `"<Company>" features pricing` — official product info
- `"<Company>" vs` — find natural comparison content
- `site:g2.com "<Company>" OR site:capterra.com "<Company>"` — review sites
- `site:reddit.com "<Company>" review OR experience` — community sentiment
- `"<Company>" press release OR announcement` — official statements
- `"<Company>" "<CEO name>" interview OR keynote OR statement` — executive positioning

**People & leadership:**
- `"<Company>" "joins as" OR "appointed" OR "named" CEO OR CTO OR CPO` — exec changes
- `"<Company>" board OR "board of directors" appointment OR "new member"` — board moves
- `"<Company>" "new hire" OR "welcomes" VP OR "head of"` — senior hires
- `site:linkedin.com "<Company>" "excited to announce" OR "thrilled to join"` — people moves

**Funding & financials (private):**
- `"<Company>" "series" OR "raised" OR "funding round" OR "valuation"` — funding events
- `"<Company>" site:crunchbase.com OR site:techcrunch.com` — funding databases
- `"<Company>" investors OR "led by" OR "participated in"` — investor details

**Public company filings:**
- `site:sec.gov "<Company>" 10-K OR 10-Q` — SEC filings
- `"<Company>" earnings call transcript <year>` — earnings transcripts
- `"<Company>" investor presentation OR investor day` — strategy materials

**Industry analysts:**
- `"<Company>" Gartner OR "Magic Quadrant" OR Forrester OR "Wave" OR IDC` — major analyst reports
- `"<Company>" "market leader" OR "leader quadrant" OR "strong performer"` — analyst rankings
- `"<Company>" "<industry>" market share OR ranking` — competitive positioning data
- `"<Company>" analyst report OR "market landscape" OR "vendor evaluation"` — broader coverage

**Hiring patterns:**
- `"<Company>" "we're hiring" OR careers` — hiring signals for strategy
- `site:linkedin.com/jobs "<Company>"` — current openings

### Public Company Research

For publicly traded companies, these are high-value primary sources — they contain verified numbers and executive statements under legal obligation:

1. **SEC filings (10-K, 10-Q)**: Revenue, margins, segment breakdowns, risk factors, competitive landscape disclosures. Search SEC EDGAR directly.
2. **Earnings call transcripts**: Executives discuss strategy, competitive positioning, product roadmap, and market dynamics. Analyst Q&A sections are especially revealing.
3. **Investor presentations**: Often contain product strategy slides, market sizing, and competitive positioning that doesn't appear elsewhere.
4. **Press releases**: Official announcements of product launches, partnerships, acquisitions, and leadership changes.

When researching a public company at standard depth or above, always search for the most recent earnings call and the latest annual filing. These two sources alone often contain more actionable intel than a dozen blog posts.

### Quality Guidelines

- **Always cite sources** — every factual claim needs a reference. If you can't source it, say so explicitly
- **Cross-reference** claims across multiple sources
- **Date everything** — always use `fetched YYYY-MM-DD` format in source entries
- **Be honest about gaps** — mark sections as "Not found" rather than guessing
- **Distinguish facts from inference** — use "appears to" or "suggests" for interpretations
- **Prefer primary sources** — a company's own filings and press releases over third-party summaries
- **Archive key pages** — save fetched content that backs important claims to the sources directory
- **Be strategic, not just descriptive** — every profile, comparison, and landscape should tell the user what the information *means* for their competitive position, not just what the facts are. "They have feature X" is data; "They have feature X, which threatens our position in segment Y because Z" is intelligence

### First Run Setup

The first time this skill runs in a project:

1. Create the `.competitive-intel/` directory structure
2. If the user is doing a comparison, ask them to describe their product and save it
3. Proceed with the requested analysis

Check for `.competitive-intel/` existence at the start of every run. If it exists, read what's already there before searching — existing profiles save research time.
