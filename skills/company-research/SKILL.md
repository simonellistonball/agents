---
name: company-research
description: >
  Produce a rigorous, stage-adapted research dossier on a company — ownership,
  history, product, strategy, funding, market potential, press coverage, a
  dedicated negative-sentiment / reputation section, founder and core-team
  backgrounds (for early-stage), and a competitive landscape with a visual
  artefact. Writes the output as a page in the user's Obsidian vault and creates
  stub pages for any other companies uncovered during the research. Use this
  skill whenever the user asks to "research", "look into", "do a deep-dive on",
  "profile", "diligence", or "write up" a company, or asks who the founders,
  competitors, or investors of a company are — even if they don't use the word
  "research". Also use when the user says "what's the story with [company]",
  "tell me about [company]", or asks for a competitive landscape of a market.
---

# Company Research

Produce a structured, evidence-backed research dossier on a company. The depth and emphasis of each section depends on the company's stage (startup / scaleup / established-private / public / subsidiary). Output is a single markdown file written to the user's Obsidian vault under `Companies/`, plus stub pages for other companies uncovered along the way, plus a visual competitive landscape as a separate artefact.

## Core principles

1. **Evidence first.** Every factual claim must be traceable to a source. If a fact is uncertain, say so and explain the reasoning. The user's preferences explicitly require this — never paper over gaps.
2. **Stage-adapted.** A three-person seed-stage startup and a FTSE-listed enterprise need very different research. Detect the stage first, then branch.
3. **Negative sentiment is a first-class section.** Do not fold scandals, lawsuits, controversies, layoffs, or reputational issues into the general narrative. They get their own section so the user can scan the risks at a glance.
4. **Uncover the adjacent graph.** Every company research session produces stub pages for competitors, investors, acquirers, and comparable companies mentioned. This builds the user's knowledge graph over time.
5. **Obsidian-native output.** Use `[[wikilinks]]`, ISO 8601 dates (`YYYY-MM-DD`), and tags (`#startup`, `#public`, `#competitor`, etc.) for querying.

## Workflow

Follow these phases in order. Don't skip ahead — later phases depend on decisions made earlier.

### Phase 1 — Identify and classify

Before researching, pin down exactly *which* company and what stage it's at.

1. **Disambiguate the target.** Many company names collide (e.g. "Anthropic" is unambiguous, but "Iconic Games" could be multiple entities). Do one initial web search to confirm which entity the user means. If genuinely ambiguous, ask the user before continuing.
2. **Determine stage.** Use this classifier:

   | Signal | Stage |
   |---|---|
   | No public funding announcements, <10 employees on LinkedIn, founded <2 years ago | `#pre-seed` or `#seed` |
   | Series A–B, 10–100 employees, identified Product-Market Fit | `#startup` (early-stage) |
   | Series C+, 100–1000 employees, multiple products, international presence | `#scaleup` |
   | Profitable, >10 years old, private, no imminent IPO signals | `#established-private` |
   | Listed on any stock exchange | `#public` |
   | Owned by a larger parent (check for acquisition history) | `#subsidiary` — research the parent too, and create a stub page for it |

3. **Load the relevant reference file for that stage** from `references/`:
   - `references/stage-startup.md` — for pre-seed / seed / startup / scaleup
   - `references/stage-established.md` — for established-private / subsidiary
   - `references/stage-public.md` — for public companies

   These files contain the stage-specific emphasis, suggested search queries, and data sources to prioritise.

### Phase 1.5 — Check existing knowledge first

Before doing any fresh research, check what the user already has. Skipping this means duplicating work the user has already done — often to a higher standard, since prior notes may include proprietary or insider information that isn't on the public web.

Run these four checks in parallel:

1. **Vault search (Obsidian).** If the `obsidian-mcp-tools` MCP is connected, search the vault for:
   - A direct filename match under `Companies/` (e.g. `Companies/Algolia.md`)
   - Any file mentioning the company name anywhere (full-text search)
   - Any `[[Company Name]]` wikilink references in other notes
   - Tagged pages (`#algolia`, if the user has tagged content by company)

   If the MCP isn't connected, tell the user: "I can't reach the Obsidian vault directly in this session. If you'd like me to check for existing notes, let me know where your vault is or paste/attach the relevant file." Don't silently skip.

2. **Memory search.** Check `userMemories` for any mention of the company. The user's memories may contain top-of-mind context, prior research threads, strategic views, or personal relationships with the company. This is high-signal — the user has already flagged it as worth remembering.

3. **Past conversations search.** Use `conversation_search` with the company name as the query. The user may have researched this company in a previous session, and those findings won't be in the vault yet if the session was recent. Also try common variations (e.g. "Algolia Stephen Lynch", not just "Algolia") if the memory hints at a specific angle.

4. **Uploaded files.** Check if the user has attached any files that could be relevant — investor decks, internal briefs, board packs, prior dossiers.

**How to use what you find:**

- **If the vault already has a full dossier for this company:** stop and ask the user. "I found an existing dossier at `Companies/[Name].md` last updated YYYY-MM-DD. Options: (a) update it in place with new findings since that date, (b) write a fresh dossier alongside the old one, (c) just summarise what's new since the existing dossier was written. Which?" Default recommendation: (a) update in place, preserving the user's own annotations.
- **If the vault has a stub page or partial notes:** incorporate everything from the existing page into the new dossier. Quote or paraphrase the user's own notes as authoritative — they are primary source for anything the user has personally learned. Clearly mark which sections come from existing notes vs. fresh research.
- **If memory or past conversations reveal a specific angle** (e.g. "user is researching Algolia because of the Stephen Lynch leadership transition"): weight the research toward that angle. Don't produce a generic dossier when the user has already signalled what they care about.
- **If uploaded files exist:** read them first. An investor deck or board pack will usually contain information unavailable on the public web and should be treated as the authoritative source for whatever it covers.

**Always flag provenance.** Any factual claim that comes from a user-provided source (vault note, memory, uploaded file, past conversation) must be marked in the dossier — e.g. `[source: existing vault note dated YYYY-MM-DD]` or `[source: from attached investor deck]`. The user needs to know which claims are their own prior knowledge being surfaced, vs. fresh external research, vs. synthesis across both.

**Do not assume public-web data overrides prior notes.** If the vault says the company has 200 employees and LinkedIn shows 180, don't silently replace the vault figure — both are data points, and the user's note may be more current or have come from a privileged source. Present both and flag the discrepancy.

### Phase 2 — Research passes

Run these as distinct research passes. Keep notes in a scratchpad as you go — you'll synthesise them in Phase 3.

**Pass A — Core facts (all stages).** Ownership, incorporation, HQ, founding date, founder names, current CEO, employee count, business model, product line. Prioritise primary sources: company site, Companies House (UK) / SEC (US) filings, LinkedIn.

**Pass B — History and record.** Founding story, key milestones, pivots, acquisitions (made or received), leadership changes. For established and public companies, focus on the last 5 years unless older context is load-bearing.

**Pass C — Product and strategy.** What they actually do, who the customer is, how they make money, what's their stated strategy and recent moves (last 12–18 months). Read their own blog / investor communications / press releases, but triangulate against independent coverage.

**Pass D — Funding and market potential.** Funding rounds, investors, valuation (last known), market size/TAM for the space, growth trajectory. Crunchbase, PitchBook mentions in press, SEC filings for public. For each major investor, note the firm — you'll create stub pages for them.

**Pass E — Press and research mentions.** Tier-1 business press (FT, WSJ, Bloomberg, Reuters), trade press (TechCrunch, The Information, industry-specific), and analyst reports (Gartner, Forrester, IDC — often behind paywalls but mentions are citable). Look for both the last 30 days and the last 12 months. Quote briefly (<15 words per source, one quote per source maximum, per copyright rules).

**Pass E2 — Public-company filings, stock behaviour, and analyst coverage (public stage only).** For `#public` companies, run these three additional passes — they are mandatory and produce their own dedicated sections in the dossier. See `references/stage-public.md` for the full methodology. Summary:

   - **Filings extraction.** Identify the filing jurisdiction(s). Build a dated inventory of the most recent annual report, last 4 quarterly/interim reports, last 12 months of material events (8-K / RNS / ad-hoc), latest proxy / AGM notice, insider transactions (Form 4 / PDMR) over the last 6 months, and major shareholder changes (13D/G / TR-1) over the last 12 months. **Do the risk-factor diff** against the prior year's annual report — this is the highest-signal technique.
   - **Stock behaviour.** Current price, market cap, enterprise value, 52-week range, multi-period returns (1m, 3m, YTD, 1y, 3y, 5y) alongside a relevant benchmark, beta, average volume, short interest, dividend yield, share count trajectory. **Produce a price trajectory chart** (SVG) overlaying the stock vs a benchmark index with event markers, and a **revenue and margin chart** (SVG) for the last 5 FYs.
   - **Analyst coverage.** Consensus rating, analyst count, mean/median/high/low price targets with spread, implied upside, EPS estimate revision trend, recent rating changes (last 6 months) with firm names and rationale where disclosed. State the source aggregator explicitly — analyst data varies by provider.

**Pass F — Negative sentiment (dedicated pass).** This is a deliberately separate search — phrase queries in ways that surface problems. Try each of:
   - `[company] lawsuit OR complaint OR settlement`
   - `[company] layoffs OR restructure`
   - `[company] scandal OR controversy OR criticism`
   - `[company] data breach OR security incident`
   - `[company] Glassdoor` (for employee sentiment — note average rating, recurring complaints)
   - `[company] SEC investigation OR fine OR penalty` (for public)
   - `[company] founder departure` (often signals internal trouble)
   - For any identified competitor, check if that competitor has publicly accused this company of anything

   Even if nothing turns up, write a brief sentence confirming the pass was run and no material issues found. Silence is itself information.

**Pass G — Team (early-stage only — skip for established/public unless user asks).** For each founder and up to ~8 core team members:
   - LinkedIn-derived career history (name the companies and roles, not just years)
   - Educational background
   - Prior exits, notable publications, or public talks
   - Any prior failed ventures — these are not negatives, they're signal

**Pass H — Competitive landscape.** Identify:
   - **Direct competitors** — same product, same customer
   - **Adjacent competitors** — different angle on the same problem
   - **Potential entrants** — large players who could move in (e.g. hyperscalers, incumbents with adjacent products)
   - **Comparable companies** — similar shape but different market (useful for analogy)

   For each, note: name, one-line description, stage, why they're relevant.

### Phase 3 — Synthesise the dossier

Use the template in `references/dossier-template.md`. The template adapts section emphasis by stage — read it and follow its rules. Key invariants regardless of stage:

- **Use `[[wikilinks]]`** for every other company, investor, and named person mentioned (this is what creates the knowledge graph).
- **Use ISO 8601 dates** (`2024-03-15`, not `March 15, 2024` or `15/03/2024`) — the user's convention.
- **Cite inline** with `[source name](url)` at the end of each factual claim. Group citations at the end of a paragraph if there are many.
- **Flag uncertainty explicitly.** Phrases like "unclear whether", "reported but unconfirmed", "last verified YYYY-MM-DD" are expected and welcomed.
- **Include a "Research metadata" footer** with the date the research was conducted, sources checked, and any known gaps.

### Phase 4 — Visual competitive landscape

Pick the visual that best fits the market shape. Read `references/visuals.md` for the decision rubric and the two templates:

| Market shape | Visual | Why |
|---|---|---|
| Many players clustered around a product category, with clear adjacent spaces | **Market map** (clustered SVG) — see `assets/market-map-template.svg` | Shows density and adjacencies at a glance |
| Ecosystem with clear flows (data, money, product) between distinct player types | **D3 ecosystem diagram** — see `assets/ecosystem-template.html` | Shows *how* value moves, not just who's in the market |

The visual is written as a separate file alongside the dossier, and the dossier links to it. Name it `[company-slug]-landscape.svg` or `[company-slug]-landscape.html`.

### Phase 5 — Write to the vault

The user's Obsidian vault is accessible via the `obsidian-mcp-tools` MCP server (noted in their memories). In this session, if that MCP is not connected, write the files to the local workspace and present them for the user to drop into their vault manually.

File layout:
```
Companies/
├── [Company Name].md                      # main dossier
├── [Company Name]-landscape.svg           # competitive landscape (or .html for ecosystem diagrams)
├── [Company Name]-stock-chart.svg         # PUBLIC ONLY — price vs benchmark
├── [Company Name]-revenue-margin.svg      # PUBLIC ONLY — 5-year revenue and operating margin
└── [Stub pages for uncovered companies — minimal, see below]
```

For public companies, link to all three visuals from the appropriate sections of the dossier (landscape from "Competitive landscape", stock chart from "Stock behaviour", revenue/margin chart from "Recent filings" or "Stock behaviour").

**Stub pages** for uncovered companies (competitors, investors, comparable companies, acquirers) should be minimal — just enough that `[[wikilinks]]` from the main dossier resolve, and enough scaffolding that a future research pass on that company has context:

```markdown
---
tags: [stub, <stage-if-known>, <relationship-to-main-company>]
date-created: YYYY-MM-DD
---
# [Company Name]

> Stub page — created as part of research on [[Main Company]] on YYYY-MM-DD.

- **One-line description:** …
- **Relationship to [[Main Company]]:** direct competitor / investor / acquirer / comparable / etc.
- **Stage:** …
- **Why relevant:** …

## Further research needed
- [ ] Ownership and funding history
- [ ] Product and strategy
- [ ] Team
```

**Before creating any stub page, check the vault.** For each company uncovered during research (competitors, investors, acquirers, comparable companies), search the vault first:

- If a full page already exists (not a stub) — **do not overwrite**. Add a `[[wikilink]]` to the main dossier that points to the existing page, and in the main dossier note briefly what the existing page covers so the user knows to cross-reference.
- If an existing stub exists — **augment, don't replace**. Add any new information you've uncovered during this research (role relative to the main company, stage if now known), update the `date-created` frontmatter to include a `date-updated: YYYY-MM-DD` line, and preserve any existing notes the user has added.
- If nothing exists — create a new stub using the template above.

Every stub-creation or augmentation decision should be recorded in the "Stub pages created" list in the dossier's Research metadata footer, distinguishing **created** from **augmented** from **linked-to-existing**.

### Phase 6 — Return to the user

Tell the user:
1. **What was already known** — any existing vault pages, memory context, past conversations, or uploaded files that fed into the research. If nothing existed, say so in one sentence ("No prior notes on [Company] in the vault, memory, or recent conversations — this is a fresh dossier.").
2. What stage you classified the company as, and why
3. Whether the output is a **new dossier**, an **update to an existing dossier**, or a **supplement alongside an existing one**, and the file path
4. The landscape artefact path and which type you chose (and why)
5. For public companies: paths to the price trajectory chart and revenue/margin chart, with one-line commentary on what they show
6. A list of stub pages — split into **created**, **augmented**, and **linked to existing** (do not create new stubs for companies already properly documented in the vault)
7. Known gaps — things you couldn't find that a human might be able to dig up (e.g. "couldn't confirm employee count; LinkedIn shows ~80 but Companies House filings suggest ~120"; for public: "couldn't access detailed analyst notes from [Firm] — paywalled")
8. Any **discrepancies** between existing vault/memory data and fresh external research, flagged clearly so the user can decide which is authoritative

Do NOT summarise the dossier itself in the chat — it's long, it's in the file, and re-summarising wastes the user's attention. A one-sentence headline is fine if genuinely useful.

## When to ask the user vs. proceed

Proceed without asking if:
- The company name is unambiguous
- The user hasn't specified depth (default to full dossier)

Ask before proceeding if:
- Multiple companies share the name and context doesn't disambiguate
- The company is so small / obscure that you can't find primary sources (ask: "I can find limited public information — is this a private/stealth company you have inside knowledge of, or should I do my best with what's available?")
- The user has asked for something narrower ("just the funding history") — in that case, skip the full dossier and return just what they asked for

## Things to avoid

- **Do not fabricate.** If a figure isn't sourced, don't put a number on it. Use ranges ("between 100 and 200 employees based on LinkedIn"), qualitative descriptions ("mid-sized"), or "unknown".
- **Do not copy large chunks.** Paraphrase. Maximum one direct quote per source, under 15 words. This is a hard copyright rule.
- **Do not soften negative findings.** The negative-sentiment section is where the user looks for risk signals. If Glassdoor is 2.1/5 with recurring complaints about management, say so clearly.
- **Do not skip the visual.** The user specifically wants it as a separate artefact. Even for companies in diffuse markets, a sparse market map is more useful than no map.
- **Do not produce a generic template.** Every section should have content specific to this company, or an explicit "not applicable because X" / "unknown — see gaps".
