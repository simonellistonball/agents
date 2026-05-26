# Stage reference: Public company

## Emphasis

Public companies have an abundance of primary-source information. The research shifts from detective work to synthesis — the facts are there; the job is to pick out what matters. The research weighting shifts accordingly:

- **Filings and financials: 25%** — recent filings (annual, quarterly, material events), financial snapshot, guidance
- **Product and strategy: 20%** — strategic moves, capital allocation, stated priorities in earnings calls
- **Stock behaviour and analyst coverage: 15%** — price trajectory, volatility, analyst consensus, recent rating changes
- **Ownership and insider activity: 10%** — major shareholders, insider dealing, activist positions, buybacks
- **History and record: 10%** — IPO, major acquisitions, leadership transitions
- **Competitive landscape: 10%** — explicitly disclosed competitors in the 10-K, plus emerging threats
- **Negative sentiment: 5%** — public companies have public controversies; don't underweight it, but a lot of it will already surface in the risk factors section of the annual report
- **Team: 5%** — C-suite and board chair, plus any notable recent departures

## Filings extraction — the core research activity

This is the highest-priority pass for public companies. The goal is a structured inventory of recent filings, not just reading the latest annual report.

### Identify the correct filing jurisdiction(s)

First, determine where the company files. Many companies file in multiple jurisdictions (e.g. UK-listed with a US ADR also files 20-F with the SEC). Check all relevant ones:

| Listing | Regulator | Primary portal | Filing types to hunt for |
|---|---|---|---|
| NYSE / NASDAQ / other US | SEC | [SEC EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch) | 10-K, 10-Q, 8-K, DEF 14A, Form 4, 13D/13G, S-1 |
| LSE Main / AIM | FCA | [LSE RNS](https://www.londonstockexchange.com/news) + [FCA National Storage Mechanism](https://data.fca.org.uk/#/nsm/nationalstoragemechanism) | Annual Report, Interim Report, RNS announcements, TR-1 (major shareholding), PDMR notifications |
| Euronext (Amsterdam, Paris, Brussels, Lisbon, Dublin, Oslo) | Local regulator + AFM/AMF etc. | Company IR page + [Euronext](https://live.euronext.com) | Universal Registration Document (URD), half-year report, ad-hoc announcements |
| Deutsche Börse | BaFin | Company IR + [Bundesanzeiger](https://www.bundesanzeiger.de) | Annual Report, half-year report, ad-hoc disclosure |
| TSX (Canada) | CSA / OSC | [SEDAR+](https://www.sedarplus.ca) | AIF, MD&A, interim financial statements |
| ASX (Australia) | ASIC | [ASX announcements](https://www2.asx.com.au) | Annual Report, Appendix 4E, Appendix 4D, continuous disclosure |
| HKEX | SFC | [HKEXnews](https://www.hkexnews.hk) | Annual Report, interim report, announcements |
| Multiple listings / foreign private issuer with US ADR | SEC | SEC EDGAR | 20-F (annual), 6-K (material events) |

### Build a filings inventory

For the dossier, produce a dated inventory of the most recent relevant filings. Template:

```markdown
## Recent filings

### Annual report (most recent)
- **[20XX Annual Report / 10-K filed YYYY-MM-DD](url)** — FY ending YYYY-MM-DD
  - **Headline numbers:** Revenue $Xm (YoY +/-X%), operating income $Xm, net income $Xm
  - **Auditor:** [Firm]. Audit opinion: unqualified / qualified / going concern / adverse.
  - **Key risk factors newly added or escalated vs prior year:** [list — this is high-signal]
  - **Material weaknesses or internal control issues disclosed:** [list or "none disclosed"]

### Quarterly / interim reports (last 4 quarters)
- YYYY-MM-DD — 10-Q / Interim — Revenue $Xm, [one-line summary]
- YYYY-MM-DD — 10-Q / Interim — Revenue $Xm, [one-line summary]

### Material events / ad-hoc disclosures (last 12 months)
- YYYY-MM-DD — 8-K / RNS — [event summary, e.g. CEO departure, acquisition announced, guidance revision]
- YYYY-MM-DD — 8-K / RNS — [event summary]

### Proxy / governance filings
- YYYY-MM-DD — DEF 14A / Notice of AGM — executive compensation: CEO $Xm (ratio X:1 to median employee); say-on-pay vote X% approval

### Insider transactions (last 6 months — Form 4 / PDMR notifications)
Summarise the pattern (don't list every trade):
- Net insider buying/selling: $Xm net sold / bought
- Notable individual transactions: CEO sold X shares on YYYY-MM-DD (~$Xm); CFO exercised options and sold on YYYY-MM-DD
- Any 10b5-1 plan adoptions or terminations
- Overall pattern: [e.g. "concentrated CEO selling in Q3 despite positive guidance — flag for review"]

### Major shareholder changes (last 12 months — 13D/13G / TR-1)
- YYYY-MM-DD — [[Investor]] filed 13D disclosing X% stake (activist) / 13G disclosing X% (passive)
- YYYY-MM-DD — [[Investor]] reduced holding from X% to Y%
```

### What to actually read in the annual report

Do not read the whole 10-K / Annual Report — it's 200+ pages. Extract these sections specifically:

| Section | What you're looking for |
|---|---|
| Item 1 — Business (10-K) / Strategic Report (UK) | Segment structure, named competitors, stated strategy |
| Item 1A — Risk Factors (10-K) / Principal Risks (UK) | **Compare against prior year.** Newly added risks are the most important signal in the document. |
| Item 7 — MD&A | Management's explanation of results; guidance for upcoming year |
| Item 8 — Financial Statements and Notes | The notes are where the interesting stuff lives — commitments, contingencies, off-balance-sheet items |
| Exhibit 21 (10-K) / Subsidiaries schedule | Full corporate structure — often reveals unexpected acquisitions or foreign entities |
| Contingencies / litigation notes | Pending lawsuits with estimated ranges |
| Related-party transactions | Always worth a look |
| Going concern / subsequent events | If present, it's important |

### Risk factor diff — high-value technique

Download this year's AND last year's risk factors section. Note which risks are:
- **Newly added** — something management is now worried about that they weren't before
- **Escalated** — stronger language used, moved earlier in the list
- **Removed** — something management no longer sees as material
- **Unchanged** — boilerplate

Newly added and escalated risks are often the most important signal in the entire annual report. List them in the dossier with the specific language used (paraphrased — one short quote per source maximum, under 15 words).

## Stock behaviour — required section

The user's preferences require charts for numerical comparisons over time. Share price analysis is the canonical example.

### Data to gather

Use whatever source has the data (Yahoo Finance, Google Finance, company IR page, Bloomberg/Reuters quote pages, exchange website). Ideal primary source: the exchange itself.

For the dossier, produce:

- **Current price** (as of YYYY-MM-DD)
- **Market capitalisation** ($ or £ bn/m)
- **Enterprise value** (market cap + debt − cash)
- **52-week range** with dates of high and low
- **1-month, 3-month, YTD, 1-year, 3-year, 5-year total returns** (price + dividends)
- **Same returns for a relevant benchmark** (S&P 500 for US large-cap, FTSE 100 for UK, sector-specific index where applicable). Show both absolute return and *relative* return vs benchmark.
- **Beta** (volatility relative to market)
- **Average daily trading volume** (last 3 months)
- **Short interest** (% of float shorted — SEC filings in US, short-selling disclosure regimes in Europe)
- **Dividend yield** (if applicable) and payout history
- **Share count trajectory** — buybacks have reduced shares outstanding by X%, or dilution has increased them by X%

### Required chart: price trajectory

Create an SVG line chart showing the company's share price (or total return) over the last 3 or 5 years, overlaid with a relevant index. Include:

- Axes clearly labelled (time on X, price or rebased index on Y)
- Both lines colour-distinguished with a legend
- Vertical markers on key events (earnings beats/misses, major announcements, leadership changes) — label them briefly
- Caption with data source and date range

Save this as `[company-slug]-stock-chart.svg` alongside the dossier.

### Required chart: revenue and margin trajectory

A separate chart showing 5-year revenue (bar) with operating margin (line overlay). This visualises the growth vs profitability story that quarterly MD&As talk about in prose.

### What to note in the commentary

- Any period of unusual volatility — why?
- Divergence from the benchmark — outperforming or underperforming and since when?
- Reaction to specific events — did the stock pop on the acquisition announcement, or sell off?
- Short interest trends — rising short interest is a negative-sentiment signal worth flagging in the negative-sentiment section
- Unusual volume days — often correlate with earnings or material disclosures

## Analyst coverage — required section

### Data to gather

Most accessible sources: Yahoo Finance "Analysis" tab, MarketWatch, Reuters, company IR page (which sometimes lists covering analysts), TipRanks, Koyfin (free tier). Aggregators often paywall the detailed notes but the summary data is free.

For the dossier, produce:

- **Consensus rating** (Strong Buy / Buy / Hold / Sell / Strong Sell — or the equivalent scale)
- **Number of analysts** issuing the consensus
- **Price target: mean, median, high, low** — and the spread. Wide spread = analyst disagreement = interesting.
- **Implied upside/downside vs current price**
- **Recent rating changes (last 6 months)** — who upgraded/downgraded and when, and why if reported. This is the highest-signal data point.
- **Earnings estimate trend** — have estimates been revised up or down over the last 90 days? (Most aggregators publish "EPS estimate revisions" as a metric.)
- **Next earnings date** — so the user knows when the picture will update

### Table format

```markdown
## Analyst coverage

| Metric | Value | As of |
|---|---|---|
| Consensus rating | Buy (13 analysts: 3 Strong Buy, 7 Buy, 3 Hold) | YYYY-MM-DD |
| Mean price target | $XX.XX | YYYY-MM-DD |
| Median price target | $XX.XX | YYYY-MM-DD |
| Price target range | $XX – $XX (spread: X%) | YYYY-MM-DD |
| Implied upside vs current | +X% | YYYY-MM-DD |
| EPS estimate trend (90-day) | Revised +X% / −X% | YYYY-MM-DD |
| Next earnings date | YYYY-MM-DD (Q[X] FY20XX) | — |

### Recent rating changes (last 6 months)
- YYYY-MM-DD — [Firm] upgraded from Hold to Buy, raised PT to $XX (from $XX). Rationale reported: [brief].
- YYYY-MM-DD — [Firm] initiated coverage at Buy with PT $XX.
- YYYY-MM-DD — [Firm] downgraded from Buy to Hold; concerns cited: [brief].
```

### Caveats to state explicitly

- Analyst ratings are systematically biased toward "Buy" (well-documented); a consensus Hold is often a de facto Sell signal
- Price targets are 12-month projections and most are wrong
- Sell-side research is often paywalled; this summary is assembled from aggregators and press coverage of rating changes. Name the aggregator used.
- Independent research (Bernstein, MoffettNathanson, Redburn Atlantic, etc.) is often higher-quality than bulge-bracket but less available

## Financial snapshot

Include a compact financials table alongside the filings inventory:

| Metric | Latest FY | Prior FY | YoY change | Source |
|---|---|---|---|---|
| Revenue | $Xm | $Xm | +X% | 10-K FY20XX |
| Gross margin | X% | X% | +X pp | 10-K FY20XX |
| Operating income | $Xm | $Xm | +X% | 10-K FY20XX |
| Net income | $Xm | $Xm | +X% | 10-K FY20XX |
| Cash and equivalents | $Xm | $Xm | — | Latest 10-Q |
| Total debt | $Xm | $Xm | — | Latest 10-Q |
| Free cash flow | $Xm | $Xm | — | Latest 10-K |

## Ownership

Identify:

- **Top 5–10 institutional shareholders** with % held (from DEF 14A, 13F filings aggregated on WhaleWisdom / Dataroma / company IR, or TR-1 filings for UK)
- **Insider holdings** — CEO, founder, board combined % of shares outstanding
- **Any >5% shareholders** — named in filings
- **Activist positions** — any 13D filings in the last 18 months? Look at the schedule 13D itself for stated intent.
- **Buyback programmes** — active authorisation? How much executed in the last FY? Remaining authorisation?
- **Dual-class structure** — if the founder or insiders retain a super-voting share class, note it and quantify the voting power
- **Insider selling cluster analysis** — if multiple insiders sold in the same narrow window, that's a sentiment signal

## Competitors — use the 10-K / Strategic Report as starting point

The company names its own competitors in the Business section. Start there — it's what management actually thinks about. Then add:

- **Competitors management doesn't name** but analysts and press do
- **Emerging private-company threats** — often not in the 10-K because they're too small
- **Adjacent platform players** — especially Big Tech if the company operates in a space that hyperscalers could enter

## Regulatory exposure

For public companies, regulatory risk is often the biggest negative-sentiment category. Check:

- **SEC enforcement actions** (US) — search SEC.gov litigation releases by company name
- **FCA / CMA actions** (UK) — search FCA final notices
- **FTC / DOJ antitrust** (US) / equivalent elsewhere
- **Pending major legislation** affecting the business model (GDPR, DMA, AI Act, etc.)
- **Recent litigation disclosed in 10-K** — usually in contingencies notes
- **Short-seller reports** — Hindenburg, Muddy Waters, Culper, etc. often publish detailed research alleging fraud or misconduct. Always worth checking whether the company has been targeted.

## Obsidian tags for this stage

`#public` + exchange tag (`#nyse`, `#nasdaq`, `#lse`, `#ftse`, `#euronext`, `#tsx`, `#asx`, `#hkex`, `#aim`), plus `#company` as a root tag. Add `#founder-led` if the founder is still CEO, `#dual-class` if there's a super-voting share class, `#activist-target` if an activist has filed a 13D in the last 18 months.
