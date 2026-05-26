# Visuals reference: competitive landscape artefacts

The skill produces one visual artefact per company dossier. Pick the format based on market shape, not personal preference.

## Decision rubric

Answer these three questions:

1. **Are there clear flows between player types?** (data, money, product, users)
2. **Are there 3+ distinct player roles?** (e.g. creators, platforms, aggregators, buyers)
3. **Does the user need to understand *how* value moves, not just who is where?**

| Yes to all three | → **D3 ecosystem diagram** (HTML) |
| Yes to some / No | → **Market map** (SVG) |

### Examples

- **Algolia** (search infrastructure) — competitors cluster by tier (enterprise vs SMB) and approach (managed vs open-source). No meaningful flows between competitors themselves. → **Market map**
- **Unity's data marketplace** — multiple roles (developers, data providers, game studios, advertisers) with distinct data and revenue flows. → **D3 ecosystem diagram**
- **Anthropic** (AI lab) — competitors cluster by model capability and approach. Flows exist (model access, API revenue) but mostly to customers, not between competitors. → **Market map**, unless the user specifically wants to see the infrastructure-provider → model-lab → application ecosystem, in which case → **D3 ecosystem**

When in doubt, default to **market map** — it's simpler, always works, and conveys positioning clearly.

---

## Market map (SVG)

Use `assets/market-map-template.svg` as the starting point. The template has placeholder clusters you replace with actual competitor positioning.

### Structure

A 2D positioning space. Choose two axes that capture the most meaningful differentiation for this market. Common pairings:

| Axis 1 | Axis 2 | When to use |
|---|---|---|
| Target customer size (SMB ↔ Enterprise) | Approach (DIY ↔ Managed) | B2B SaaS markets |
| Breadth (Single product ↔ Platform) | Depth (Shallow ↔ Deep) | Competitive platform markets |
| Price point (Low ↔ High) | Feature richness (Basic ↔ Advanced) | Consumer/prosumer markets |
| Stage of pipeline (Source ↔ Consume) | Abstraction (Raw ↔ Abstracted) | Data / infrastructure markets |

State the axis choice explicitly in the caption — the axes *are* the analytical claim.

### Clustering

Group competitors by similarity. Use coloured clusters or convex hulls to show groups. Label clusters ("Established enterprise vendors", "Open-source native", "AI-first challengers").

### Required elements

- **Two labelled axes** with clear endpoints
- **The target company** marked distinctively (e.g. filled shape vs outlined, or different colour)
- **Direct competitors** clustered around the target
- **Adjacent / potential entrants** shown on the edges or in a separate cluster
- **Legend** explaining symbol/colour coding
- **Caption** with: axis rationale, as-of date, data source

### Styling

Keep it clean. Black/white/grey base with one or two accent colours. Label every point. If a cluster has too many competitors to label individually, collapse them into a cluster label with a count (e.g. "6 smaller regional players").

---

## D3 ecosystem diagram (HTML)

Use `assets/ecosystem-template.html` as the starting point. This template follows the same pattern as the user's existing `ecosystem-flow-diagram` skill output, for consistency across their vault.

### When to use

When the market has distinct *roles* (not just competitors) with flows between them. The insight isn't "who's winning" — it's "how does value move".

### Structure

Left-to-right flow diagram with:

- **Node columns** — each column represents a role (e.g. "Data sources", "Platforms", "Buyers")
- **Nodes** — individual companies within each role
- **Links** — flows between nodes, coloured by flow type:
  - Blue: data flow
  - Green: recurring revenue
  - Gold: one-off revenue
  - Grey: product/service delivery
  - Dashed: potential / speculative flow

### Required elements

- **Target company highlighted** (different colour or border)
- **Flow legend**
- **Role labels** for each column
- **Hover tooltips** showing flow details (from template)
- **Title and caption** with as-of date

### When to create your own structure

If the template doesn't fit the market shape (e.g. a true network rather than a left-to-right flow), modify the D3 code. Keep the core conventions — flow colour coding, target company highlight, hover tooltips — but change the layout.

---

## Common pitfalls

- **Don't put too many competitors on either visual.** A market map with 30 logos is unreadable. Cap at ~15 named entities; use "and N others" cluster labels for the rest.
- **Don't invent positioning.** Place competitors based on evidence (their own website claims, analyst categorisation, pricing pages). If placement is uncertain, use a lighter shade or mark with a "?".
- **Don't skip the caption.** The visual without a caption is just a decoration. The caption explains what the analyst (Claude) is claiming the reader should take away.
- **Don't forget the date.** Markets move fast. Every visual is as-of a specific date — write it in the caption.
- **Always link from the main dossier** to the visual file, with a short sentence explaining what the visual shows and why it's structured the way it is.
