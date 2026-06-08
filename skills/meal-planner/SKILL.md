---
name: meal-planner
description: >
  Weekly dinner meal planner triggered by an Ocado grocery delivery. Use this skill whenever
  the user mentions meal planning, an Ocado delivery, "what should we eat this week",
  "plan dinners", "weekly meals", or "ocado receipt". Also trigger when the user asks to
  update recipes, check the recipe database, or log a meal they've cooked. The skill fetches
  the Ocado receipt PDF via Gmail + Chrome, parses ingredients and use-by dates, checks Google
  Calendar for evening commitments, consults the Obsidian recipe database for suggestions,
  builds a dinner plan anchored to use-by dates, presents it for user review, adds a
  nutritionist critique (inflammation + weight management focus), and adds finalised dinners
  to Google Calendar. Run this skill whenever a new Ocado delivery has arrived or the user
  wants to plan their week's dinners.
compatibility:
  tools:
    - Gmail MCP (search_threads, get_thread)
    - Claude in Chrome (navigate, get_page_text, find, computer)
    - Google Calendar MCP (list_events, create_event)
    - obsidian-mcp-tools (search_vault, get_vault_file, create_vault_file, patch_vault_file, list_vault_files)
---

# Meal Planner Skill

Plans a week of home dinners from an Ocado delivery, anchored to use-by dates, informed by
an Obsidian recipe database, and critiqued through a nutritionist lens.

## Permanent constraints (never ask, always apply)
- **Lizzie has a fish and seafood allergy** — no fish, shellfish, or seafood in any meal
- **Dinner calendar slot**: 19:00–20:00, added to the user's primary Google Calendar
- **Nutritionist critique**: always included, focus on inflammation reduction and weight management
- **Recipe database location**: `Recipes/` folder in the Obsidian vault

---

## Phase 1 — Fetch the Ocado receipt

### Step 1a: Search Gmail
Use Gmail MCP to find the most recent Ocado receipt email:
```
search query: "from:ocado@ocado.com receipt" or "subject:Your Ocado receipt"
```
Retrieve the thread and extract the receipt PDF download link. The link is typically labelled
"View your receipt" or similar and points to the Ocado website.

### Step 1b: Download the PDF via Chrome
> Read `references/chrome-ocado.md` before executing this step.

Use Claude in Chrome to:
1. Navigate to the receipt URL extracted from the email
2. Download the PDF (the page usually has a direct download button or renders the PDF inline)
3. Extract the full text content of the receipt

### Step 1c: Parse the receipt
Extract two structured lists from the receipt text:

**Ingredients list** — for each item note:
- Product name (simplified)
- Quantity / weight
- Use-by date (bucket into: today, Wed, Fri, Sat, Sun, Mon, or "1wk+")
- Category: Fridge / Cupboard / No use-by

**Use-by anchor map** — group ingredients by their expiry bucket, tightest first. This drives
meal anchoring in Phase 3.

If no receipt is available (user declines or email not found), ask the user to paste the
receipt text or upload the PDF directly.

---

## Phase 2 — Check the calendar

Use Google Calendar MCP to list all events on the user's primary calendar for the next 7 days
(from today through end of day +7).

Flag any evening events (starting 17:00 or later) as **"out for dinner"** candidates. Use
judgement — a 30-min call is not dinner out; a social event at a named location or running
past 20:00 is.

Build a simple map:
```
Mon: home
Tue: home
Wed: OUT (Chloe & Ross, Saffron Walden, 19:00)
Thu: OUT (AI Meetup — pizza on, until 21:00)
Fri: home
Sat: home
Sun: home
```

Count the number of **home dinner slots** available. This is the target number of meals to plan.

---

## Phase 3 — Consult the recipe database

> Read `references/recipe-database.md` for the recipe note schema before searching.

### Step 3a: Search for matching recipes
Use `obsidian-mcp-tools:search_vault` to search `Recipes/` for recipes whose ingredient tags
match items in the parsed ingredient list. Cast a wide net — search by key ingredient (e.g.
"chicken thigh", "halloumi", "cannellini beans").

For each candidate recipe note, extract:
- Recipe name
- Key ingredients required
- `last_cooked` date
- `times_cooked` count
- Any `nutritionist_flags`

### Step 3b: Score and rank candidates
Rank recipes by:
1. **Ingredient match** — how many of the required ingredients are in the delivery? (higher = better)
2. **Recency penalty** — deprioritise recipes cooked in the last 14 days
3. **Nutritionist flags** — surface any flagged concerns to the user

### Step 3c: Supplement with defaults
If fewer recipes are found than home dinner slots, fill gaps with standing defaults in this
priority order (checking each against available ingredients):
1. Chicken fajitas (if fajita kit present)
2. Veggie bean chilli
3. Roast veg & halloumi
4. Chicken & veg tray bake
5. Homemade omelette

---

## Phase 4 — Build the dinner plan

### Anchoring rules (apply strictly, in order)
1. **Assign tightest use-by ingredients first** — the meal that uses today's/Wednesday's
   produce goes earliest in the week
2. **Out-for-dinner slots get no meal** — note any produce that expires on an out day and
   flag it for lunch/breakfast use
3. **Batch cook where possible** — if a recipe yields 2+ portions (e.g. chilli), assign one
   dinner slot and note lunch usage for subsequent days
4. **Chicken on last safe day or earlier** — never leave meat to the final use-by day if
   an earlier slot is available

### Output format
Present the plan as a day-by-day visual using `show_widget` (see the widget template in
`references/widget-template.md`). Each day card shows:
- Day and date
- Meal name and emoji
- Key ingredients used
- Use-by chips (red for urgent, grey for comfortable)
- Lunch note if relevant (batch cook overflow, produce expiring on an out day)

### User review loop
After presenting the plan, invite corrections explicitly:
> "Happy with this, or would you like to swap anything around?"

Apply any changes and re-render the widget. Repeat until the user confirms.

---

## Phase 5 — Nutritionist critique

After the user confirms the plan, always produce a nutritionist critique.

> Read `references/nutritionist-framework.md` for the full evaluation framework.

Structure the critique as:
1. **Overall verdict** (one sentence + letter grade A–D)
2. **What's working well** (2–3 specific observations with reasoning)
3. **What needs attention** (2–4 specific concerns, actionable)
4. **Missing this week** (nutrients, food groups, or diversity gaps)
5. **Weight management note** (specific to the week's pattern)

Keep the critique honest and direct — do not soften concerns.

---

## Phase 6 — Add to Google Calendar

For each confirmed dinner slot (home evenings only):
- Create an event on the user's **primary Google Calendar** (simon@simonellistonball.com)
- Time: 19:00–20:00 in Europe/London
- Title format: `[emoji] Dinner: [Meal name]`
- Description: key ingredients + any use-by warnings + nutritionist flags if relevant

After adding, remind the user to move events to the Mawson Apple Calendar.

---

## Phase 7 — Update the recipe database

For each recipe used in the final plan, update (or create) its note in `Recipes/`:

**If the recipe note already exists**: use `patch_vault_file` to update the frontmatter fields:
- `last_cooked`: today's date
- `times_cooked`: increment by 1
- Append a dated entry to the `## Cook log` section with any notes or tweaks

**If the recipe note does not exist**: create it using the template in
`references/recipe-database.md`. Populate what you know from this session; leave other fields
as defaults.

> Only update `nutritionist_flags` if the critique in Phase 5 identified a specific concern
> about that recipe. Do not overwrite existing flags without surfacing them to the user first.

---

## Edge cases

| Situation | Handling |
|---|---|
| Gmail not connected | Ask user to forward the receipt email or paste text |
| Chrome not available | Ask user to upload the PDF directly |
| No Ocado receipt found in last 14 days | Warn user, ask if they want to proceed with a manual ingredient list |
| Fewer recipes in DB than dinner slots | Fill with standing defaults; offer to create stub recipe notes for them |
| All slots are out-for-dinner | Tell the user, offer to plan lunches instead |
| Produce expires on an out-for-dinner night | Flag prominently for breakfast/lunch use that day |
| Lizzie not eating that meal | Note but still apply allergy constraint (default to safe) |
