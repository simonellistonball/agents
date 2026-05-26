# Dossier template

Use this as the scaffold for every company dossier. Section inclusion adapts to stage — each section header is annotated with when to include it. Delete the annotations when writing the actual file.

---

## File frontmatter

Every dossier starts with YAML frontmatter:

```yaml
---
tags: [company, <stage-tag>, <additional-tags-as-relevant>]
company-name: "Official Legal Name Ltd"
short-name: "Common name"
stage: startup | scaleup | established-private | subsidiary | public
hq: "City, Country"
founded: YYYY-MM-DD  # or just YYYY if precise date unknown
website: https://example.com
date-researched: YYYY-MM-DD
researcher: Claude (company-research skill)
last-verified: YYYY-MM-DD
---
```

Tags should include: `company` (always), the stage tag (exactly one), any relationship tag if the company is being researched in the context of another (e.g. `competitor-of-unity`), and any topic tags (`ai`, `gaming`, `data-infrastructure`, etc.).

---

## Required section order

```markdown
# [Company Name]

> **One-line summary.** One sentence. What they do, for whom, at what stage.

## At a glance
## Ownership and corporate structure
## History and record
## Product and strategy
## Funding and market potential
## Recent filings                 <!-- PUBLIC ONLY — see stage-public.md -->
## Stock behaviour                <!-- PUBLIC ONLY — see stage-public.md -->
## Analyst coverage               <!-- PUBLIC ONLY — see stage-public.md -->
## Team                           <!-- REQUIRED for startup/scaleup; OPTIONAL otherwise (C-suite only) -->
## Press and research mentions
## Negative sentiment and reputation
## Competitive landscape
## Connections and comparisons
## Research metadata
```

Keep sections in this order. The user will develop muscle memory for where to find each kind of information.

**Public-company additions.** For `#public` stage, insert the three public-only sections (Recent filings, Stock behaviour, Analyst coverage) between "Funding and market potential" and "Team". These sections are mandatory for public companies and replace the generic "Funding and market potential" emphasis — see `stage-public.md` for exact content requirements and the required charts (price trajectory, revenue and margin trajectory).

---

## Section-by-section guidance

### At a glance

A scannable summary box. Use a bullet list, not prose:

```markdown
- **What they do:** One clear sentence, no jargon.
- **Who they serve:** Target customer segment.
- **How they make money:** Business model in one phrase.
- **Stage:** [[Seed]] | [[Series A]] | Private | [[NASDAQ-listed]] etc.
- **Size:** ~X employees (source: LinkedIn, last checked YYYY-MM-DD)
- **Headquarters:** City, country
- **Founded:** YYYY, by [[Founder 1]] and [[Founder 2]]
- **Current CEO:** [[Name]] (since YYYY)
- **Why researched:** One sentence on why the user is looking at this now.
```

### Ownership and corporate structure

Who actually owns and controls the company. Stage-dependent:

- **Startup:** Cap table outline — founders' approximate %, investors' collective %, ESOP pool, any notable angel investors
- **Established private:** Ownership type (founder / family / PE / employee-owned), named controlling parties, any parent company
- **Public:** Top institutional holders, insider %, recent activist positions
- **Subsidiary:** Parent company (wikilinked), acquisition date and price if known

Always include directors / board members with wikilinks.

### History and record

For young companies: short narrative (2–4 paragraphs).
For established or public companies: a dated timeline (see `stage-established.md`).

Include pivots, acquisitions (given and received), major product launches, leadership transitions. Wikilink every named entity.

### Product and strategy

Two sub-parts:

1. **What they actually do** — product description grounded in what customers experience, not in marketing language
2. **Where they're going** — stated strategy from recent communications (earnings calls, founder interviews, investor decks, blog posts), plus your read on whether the product and strategy are aligned

For multi-product companies, enumerate the products with one or two sentences each.

### Funding and market potential

For startups and scaleups: the funding table (see `stage-startup.md`), plus market sizing (state the source — ideally an analyst report, but "founder-claimed TAM of $Xbn" is also valid if labelled).

For established companies: acquisition history, debt facilities, dividend history.

For public companies: the financial snapshot table (see `stage-public.md`) **plus a line chart** of revenue trajectory over the last 5 FYs. The user explicitly requires charts for numerical comparisons over time.

### Team (startup/scaleup required; others C-suite only)

For each person, one paragraph covering career arc, education, prior exits/failures, domain credibility, and any connection to co-founders. See `stage-startup.md` for the full schema.

Wikilink every previous employer and educational institution.

### Press and research mentions

Organise by tier and recency:

```markdown
### Tier-1 business press (last 12 months)
- YYYY-MM-DD — [Headline](url) — Financial Times — one-sentence on angle
- YYYY-MM-DD — [Headline](url) — Bloomberg — one-sentence on angle

### Trade and industry press
- YYYY-MM-DD — [Headline](url) — TechCrunch — one-sentence on angle

### Analyst reports
- YYYY — Gartner Magic Quadrant for [Category] — [position] (note: full report paywalled; coverage [here](url))
- YYYY — Forrester Wave for [Category] — [position]

### Notable podcast / video appearances
- YYYY-MM-DD — [[Founder]] on [Podcast name] — [topic]
```

Paraphrase, don't quote more than once per source (max 15 words per quote — hard copyright limit).

### Negative sentiment and reputation

**This section always exists.** If nothing material turned up in Pass F, say so explicitly:

> No material negative coverage, lawsuits, regulatory actions, or significant employee sentiment concerns identified in research conducted on YYYY-MM-DD. Glassdoor average: X.X/5 based on N reviews.

If there is negative material, organise it:

```markdown
### Litigation and regulatory
- YYYY-MM — [[Company]] sued by [[Plaintiff]] over [brief description]. Status: [settled / ongoing / dismissed]. [source]

### Controversies and public criticism
- YYYY-MM — [brief description]. [source]. Company response: [summary].

### Employee sentiment
- Glassdoor: X.X/5 from N reviews (checked YYYY-MM-DD). Recurring themes in reviews: [theme 1], [theme 2].
- Notable senior departures: [[Name]] (role, YYYY-MM), [[Name]] (role, YYYY-MM)

### Financial or operational concerns
- [Any reported layoffs, down rounds, debt concerns, etc.]
```

State both the facts and the company's public response if there is one. Do not editorialise beyond what the sources support.

### Competitive landscape

Four sub-sections:

```markdown
### Direct competitors
Same product, same customer.
- [[Competitor 1]] — one-line description, stage
- [[Competitor 2]] — one-line description, stage

### Adjacent competitors
Different angle on the same problem.
- [[Company]] — how they approach it differently

### Potential entrants
Large players who could plausibly move into this space.
- [[Hyperscaler / incumbent]] — why they might enter

### Comparable companies
Similar business shape in adjacent markets — useful for analogy.
- [[Company]] — what makes them a useful comparison
```

Link to the visual artefact:

```markdown
📊 **See the full visual landscape:** [[Company Name - landscape]] (market map / ecosystem diagram)
```

### Connections and comparisons

Brief notes on:
- Companies the founders/execs came from (wikilinked)
- Companies in the investor portfolio worth comparing to
- Historical analogues — "this plays out like [[Earlier Company]]'s expansion into X in YYYY"
- Any connection to the user's own work context (e.g. if the user is at Unity, note whether this company is a partner, competitor, or customer — but only if supported by evidence)

### Research metadata

A footer block:

```markdown
---
## Research metadata

- **Research conducted:** YYYY-MM-DD
- **Prior knowledge check:**
  - Vault: [existing page at `Companies/X.md` last updated YYYY-MM-DD — content incorporated / no existing page / N mentions in other notes]
  - Memory: [relevant context surfaced: "..." / no prior context]
  - Past conversations: [N prior sessions on this company — key prior findings: "..." / no prior sessions]
  - Uploaded files: [filename and one-line description / none]
- **External sources checked:** [list — e.g. company website, Companies House, LinkedIn, Crunchbase, 3x tier-1 press, Glassdoor]
- **Sources not accessible:** [list — e.g. paywalled analyst reports, specific legal filings]
- **Discrepancies flagged:** [any points where prior/vault data conflicts with fresh external research]
- **Known gaps:** [bullets — things a human could dig deeper on]
- **Confidence levels:**
  - High: [list of claims with high confidence]
  - Medium: [list of claims with medium confidence]
  - Low: [list of claims the user should independently verify]
- **Stub pages handled:**
  - Created: [[Company A]], [[Company B]]
  - Augmented: [[Company C]] (existing stub from YYYY-MM-DD)
  - Linked to existing full page: [[Company D]]
```

The **prior knowledge check** section exists because the user may have proprietary data in the vault or memory that should be treated as authoritative. Being explicit about what was checked (and what was found) lets the user confirm nothing was missed, and makes it clear which claims come from their own prior work vs. fresh research.

The confidence-level section matters — it maps directly to the user's preference for explicit uncertainty.
