# Source Dossier — News Digest {{DATE_RANGE}}

Standalone accountability record for the digest generated {{GENERATED_DATE}}.
Lists every search run and every result returned, verbatim as returned by the tools,
with links and access dates so each digest claim can be traced to its origin. Access
times in {{TZ}}.

> Note: this dossier records search queries and result listings verbatim. It does not
> reproduce full-text copies of the underlying articles or newsletters — follow each
> link to read the complete original.

## 1. Run summary

- **Topics tracked:** {{TOPIC_LIST}}
- **Time window:** {{DATE_RANGE}}
- **Sources used:** web search / email newsletters
- **Totals:** {{N}} queries run · {{N}} results reviewed · {{N}} items included

## 2. Web search log

### Query: `{{exact query}}`
*Run {{access date/time}}*

| # | Result title | Source | Pub. date | URL | Snippet (verbatim as returned) | Decision |
|---|---|---|---|---|---|---|
| 1 | {{title}} | {{source}} | {{date}} | {{url}} | {{snippet}} | Included — maps to "{{topic}}" / Excluded — {{reason}} |

<!-- One block per query. Include every result returned, not only the used ones. -->

### Fetched sources
For any result opened with web_fetch, record the URL and access time. Capture the
factual takeaway in your own words (in the digest); keep any direct quote here under
15 words, attributed.

| URL | Source | Accessed | Used for |
|---|---|---|---|
| {{url}} | {{source}} | {{access time}} | "{{topic}}" |

## 3. Inbox (newsletter) search log

### Query: `{{exact gmail query}}`
*Run {{access date/time}}*

| # | Sender | Subject | Received | Link | Decision |
|---|---|---|---|---|---|
| 1 | {{sender}} | {{subject}} | {{date}} | {{url if any}} | Included — "{{topic}}" / Excluded — {{reason}} |

<!-- One block per inbox query. -->

## 4. Items included in the digest

Cross-reference of every digest item back to its source(s).

| Digest item (your wording) | Topic | Source(s) | Link(s) |
|---|---|---|---|
| {{headline}} | {{topic}} | {{source / newsletter}} | {{url}} |
