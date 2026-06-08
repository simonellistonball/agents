---
name: recipe-manager
description: >
  Manages the Obsidian recipe database — adding, editing, browsing, and analysing recipes.
  Use this skill whenever the user wants to add a new recipe, look up an existing recipe,
  edit a recipe's method or ingredients, log that they cooked something, browse what's in
  the recipe library, find recipes by ingredient, check what they haven't cooked in a while,
  get a nutritionist assessment of a specific recipe, or clean up the recipe database.
  Trigger phrases include: "add a recipe", "save this recipe", "what recipes do I have",
  "find a recipe with", "I cooked X tonight", "log a cook", "edit the recipe for",
  "show me my recipes", "what haven't I cooked recently", "assess this recipe", "recipe
  database", "update the recipe for", "backfill", "add headers to my recipes",
  "fix my recipe files", "make my recipes work with meal planning", "tidy up the recipes",
  "add frontmatter to". Always use this skill for any recipe-specific operation that isn't
  part of a full weekly meal planning run.
compatibility:
  tools:
    - obsidian-mcp-tools (search_vault, get_vault_file, create_vault_file, patch_vault_file, list_vault_files, append_to_vault_file)
---

# Recipe Manager Skill

Manages the `Recipes/` folder in the Obsidian vault — the shared recipe database used by
both this skill and the meal-planner skill.

## Permanent constraints (never ask, always apply)

- **Recipe database location**: `Recipes/` folder in the Obsidian vault
- **Lizzie has a fish and seafood allergy** — flag any recipe containing fish, shellfish,
  or seafood; set `dietary.fish_free: false` and `dietary.seafood_free: false` accordingly
- **Schema**: always use the canonical note format — read `references/operations.md` if
  in doubt, and see the shared schema in the meal-planner skill's `references/recipe-database.md`

---

## Operations

This skill handles six distinct operations. Identify which one(s) the user wants and execute
the relevant phase(s). Multiple operations can be combined in a single session (e.g. "add a
recipe and then show me everything I haven't cooked in a month").

| Operation           | When to use                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------- |
| **Add**             | User wants to save a new recipe                                                          |
| **Edit**            | User wants to change an existing recipe's content                                        |
| **Backfill**        | Existing recipe file(s) have no frontmatter — add structured data so meal planning works |
| **Log cook**        | User cooked a meal and wants to record it                                                |
| **Browse / search** | User wants to find or list recipes                                                       |
| **Assess**          | User wants a nutritionist critique of a specific recipe                                  |
| **Maintain**        | Housekeeping — fixing schema issues, merging duplicates, seeding defaults                |

---

## Operation: Add a recipe

> Read `references/operations.md` § Add before proceeding.

### Step A1 — Gather the recipe

Accept input in any form:

- User pastes or dictates the recipe in conversation
- User shares a URL (website recipe) — use Chrome if available to fetch the page, otherwise
  ask them to paste the text
- User describes the dish and asks Claude to draft it from knowledge

If drafting from knowledge, clearly state: "I've drafted this from general knowledge — please
review the method and ingredients before saving."

### Step A2 — Extract structured data

From the raw input, extract:

- Name, cuisine, meal type, prep/cook times, serves
- Ingredients list (normalised to lowercase singular form, brand-free)
- Method steps
- Any serving notes or tips
- Dietary flags (vegetarian, vegan, fish_free, seafood_free)

**Allergy check**: if any ingredient contains fish, shellfish, or seafood, flag it:

> "⚠️ This recipe contains [ingredient] — it won't be suitable for shared meals with Lizzie.
> I'll set `fish_free: false`. Shall I still save it?"

### Step A3 — Confirm before saving

Present a summary card of the recipe data and ask for confirmation:

> "Here's what I'll save — anything to change before I create the note?"

Show: name, cuisine, key ingredients, times, serves, dietary flags.

### Step A4 — Create the note

Use `obsidian-mcp-tools:create_vault_file` with:

- Path: `Recipes/[recipe-name-kebab].md`
- Content: full recipe note using the canonical template
- Set `times_cooked: 0`, `last_cooked: null`

Confirm: "Saved as `Recipes/[filename].md`."

---

## Operation: Edit a recipe

> Read `references/operations.md` § Edit before proceeding.

### Step E1 — Find the recipe

Use `obsidian-mcp-tools:search_vault_simple` with the recipe name to locate the note.
If multiple matches, list them and ask the user to confirm which one.

### Step E2 — Fetch and display current content

Use `get_vault_file` to retrieve the note. Show the user the relevant section they want
to edit (don't dump the whole note unless asked).

### Step E3 — Apply the edit

Understand what the user wants to change:

- **Frontmatter field** (e.g. serves, cuisine, dietary flag) → use `patch_vault_file`
  targeting the frontmatter
- **Ingredients list** → show current list, confirm changes, patch the `## Ingredients` section
- **Method** → show current method, confirm changes, patch the `## Method` section
- **Notes** → patch the `## Notes` section
- **Nutritionist flags** → always confirm before writing:
  > "I'll update the nutritionist flags for this recipe. Current: [x]. New: [y]. OK?"

### Step E4 — Confirm

Confirm the change was applied. Offer to show the updated section.

---

## Operation: Backfill a recipe

Used when recipe files already exist in `Recipes/` but were copied from elsewhere (a website,
a notes app, a cookbook transcription) and contain raw text only — no YAML frontmatter, no
structured sections, and no metadata the meal-planner can query.

> Read `references/operations.md` § Backfill before proceeding. It contains the full
> inference rules, ambiguity handling, and rewrite strategy for this operation.

### Step BF1 — Identify scope

Determine whether the user wants to backfill:

- **A single named recipe** — proceed directly to BF2
- **All unfrontmatted recipes in `Recipes/`** — use `list_vault_files` to list all notes,
  then `get_vault_file` on each; filter to those with no YAML frontmatter block (no `---`
  at the top). Report count to user before proceeding:

  > "I found [N] recipe files without frontmatter. Shall I backfill them all, or go one
  > at a time?"

  **Batch mode**: process all automatically, pausing only on genuine ambiguity (see BF3).
  **One at a time**: present each summary card and wait for confirmation before writing.

### Step BF2 — Parse the existing content

Fetch the note with `get_vault_file`. Read the full text and extract:

- **Recipe name** — from the `# H1` heading if present, otherwise from the filename
- **Ingredients** — find the ingredients list (usually a bullet list or numbered list
  before the method); normalise each to lowercase singular form per the rules in
  `references/operations.md` § Add
- **Method** — the numbered steps or prose instructions
- **Serves** — look for "serves X", "makes X", "for X people" anywhere in the text;
  default to 2 if not found
- **Prep / cook times** — look for "prep: Xmins", "X minutes prep", "cook for X minutes",
  oven temperature clues; estimate from method length if not stated
- **Cuisine** — infer from dish name and ingredients (e.g. halloumi → Mediterranean/Middle
  Eastern, pancetta → Italian); mark as inferred
- **Meal type** — infer from ingredients and dish name; default to `dinner`
- **Dietary flags** — derive from normalised ingredients list using the flag logic in
  `references/operations.md` § Add; apply the anchovies check

### Step BF3 — Flag ambiguities before writing

Do not guess silently on fields where inference is weak. Surface these to the user:

| Ambiguous situation                                                  | How to handle                                  |
| -------------------------------------------------------------------- | ---------------------------------------------- |
| Recipe name unclear (no H1, cryptic filename)                        | Ask: "What should this recipe be called?"      |
| Serves not mentioned and dish is unusual size                        | Ask: "How many does this serve?"               |
| Ingredients list mixed with method (no clear separation)             | Show your interpretation; ask to confirm       |
| Cuisine genuinely ambiguous                                          | Use `cuisine: null` and note it's unset        |
| Both `fish_free` and `seafood_free` uncertain (e.g. "seafood stock") | Flag explicitly; ask to confirm before setting |
| File appears to be a shopping list or meal plan, not a recipe        | Skip it; tell the user                         |

In batch mode: collect all ambiguities across all files and ask them together at the end
rather than interrupting file by file, unless an allergy ambiguity is found — always pause
immediately for those.

### Step BF4 — Reconstruct the full note

Build the complete note in memory: canonical frontmatter block + preserved original content
restructured into the standard sections (`## Ingredients`, `## Method`, `## Notes`,
`## Cook log`).

Preserve the original wording of ingredients and method exactly — do not paraphrase or
improve the prose. Only the structure changes, not the content.

Set:

- `times_cooked: 0`
- `last_cooked: null`
- `nutritionist_flags: []`

Add a `## Notes` section if one doesn't exist (leave body as `_Add notes here._`).
Add an empty `## Cook log` section.

### Step BF5 — Confirm and write

Show the user the proposed frontmatter block (not the full note — just the YAML header):

```
Here's the frontmatter I'll add to [recipe name]:

---
name: "Pasta Amatriciana"
tags: [recipe]
ingredients: [pancetta, tinned tomato, onion, garlic, parmesan, spaghetti]
cuisine: Italian
meal_type: dinner
prep_time_mins: 10
cook_time_mins: 20
serves: 2
last_cooked: null
times_cooked: 0
nutritionist_flags: []
dietary:
  vegetarian: false
  vegan: false
  fish_free: true
  seafood_free: true
---

Anything to change?
```

In batch mode: show a compact summary table of all files being updated, not individual
cards. Ask once for confirmation. Write all files on approval.

Use `create_vault_file` to overwrite the note with the full reconstructed content.

### Step BF4b — Add a nutritionist assessment (when assessable)

A backfilled recipe should arrive fully usable, which includes a nutritionist read-out
whenever there's enough to assess.
Assessable = a real ingredients list (not an empty stub) and a method to reason
about portions from. If either is missing — a bare stub, a non-recipe file, or anything you
couldn't fully parse — skip this step, leave nutritionist_flags: [], and omit the section.
When assessable:

Read references/nutritionist-single.md for the single-recipe framework.

Assess the reconstructed recipe (protein, inflammatory signals, phytonutrient density,
glycaemic impact, saturated fat, omega-3, allergy re-check).
Add a ## Nutritionist assessment section — placed after ## Notes, before ## Cook log,
dated with today's date — following the output structure in nutritionist-single.md.
Populate nutritionist_flags from the assessment (short kebab-case, e.g.
watch-saturated-fat), instead of leaving it [].

Batch mode: don't embed a full report in every file — it bloats the pass and the
confirmation. Compute and set nutritionist_flags where a clear concern exists, report them
in the batch summary, and offer to generate full assessment sections afterwards. Only embed
full reports per file in batch if the user explicitly asks. See references/operations.md
§ Backfill for the detail.

### Step BF6 — Report

After writing, confirm:

- Single: "Done — `[filename].md` is now fully structured and ready for meal planning."
- Batch: "Backfilled [N] recipes. [M] were skipped (ambiguities noted above). All are
  now ready for meal planning."

Offer to run Assess on any backfilled recipe if the user wants an immediate nutritionist
review.

---

## Operation: Log a cook

Used when the user has just cooked a meal and wants to record it — outside of a full
meal-planning run.

### Step L1 — Identify the recipe

Ask: "Which recipe did you cook?" — search `Recipes/` if not obvious from context.
If the recipe doesn't exist yet, offer to create a stub first (run the Add operation).

### Step L2 — Gather notes

Ask (briefly — can be skipped if user says nothing to add):

> "Any tweaks or notes from tonight's cook? (Hit enter to skip)"

### Step L3 — Update the note

Use `patch_vault_file` to:

1. Update frontmatter: increment `times_cooked`, set `last_cooked` to today's date
2. Append to `## Cook log`:
   ```
   - **YYYY-MM-DD** — [user's notes, or "Standard run. No changes."]
   ```

Confirm: "Logged. [Recipe name] has now been cooked [N] times, last on [date]."

---

## Operation: Browse / search

### Step B1 — Determine what the user wants

| Request type                          | Approach                                                                                |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| "Show me all my recipes"              | `list_vault_files` on `Recipes/`, then display as a summary table                       |
| "Find recipes with [ingredient]"      | `search_vault_simple` with ingredient term; filter to `Recipes/`                        |
| "What haven't I cooked recently?"     | List all recipes, sort by `last_cooked` ascending; surface those not cooked in 30+ days |
| "What can I make with [ingredients]?" | Search by each ingredient, find recipes where all/most match                            |
| "Show me quick dinners"               | Filter by `prep_time_mins + cook_time_mins < 30`                                        |
| "Show me vegetarian recipes"          | Filter by `dietary.vegetarian: true`                                                    |

### Step B2 — Present results

Use `show_widget` to render a browsable recipe card grid. Each card shows:

- Recipe name and emoji (infer from cuisine/type)
- Key ingredients (first 3–4)
- Times cooked + last cooked date
- Dietary badges (vegetarian, vegan, fish_free)
- Any nutritionist flags (⚠️ icon)

For "what haven't I cooked recently" specifically, sort by staleness and highlight the top
3–5 as suggestions.

### Step B3 — Offer to open or act

After displaying results, offer:

> "Want me to show the full recipe for any of these, or log a cook?"

---

## Operation: Assess a recipe

Provides a nutritionist critique of a single recipe — more granular than the weekly plan
critique.

### Step AS1 — Fetch the recipe

Retrieve the full note from Obsidian.

### Step AS2 — Run the assessment

> Read `references/nutritionist-single.md` for the single-recipe assessment framework.

Assess against:

- Protein adequacy per serving
- Inflammatory ingredient signals (refined carbs, seed oils, processed meat volume)
- Phytonutrient density (variety and colour of vegetables)
- Omega-3 / omega-6 balance
- Saturated fat load
- Glycaemic impact
- Any Lizzie allergy concerns (even if currently flagged)

### Step AS3 — Present and optionally save flags

Present the critique in conversation. If new `nutritionist_flags` are identified that aren't
already on the note, ask:

> "Shall I add these flags to the recipe note for future reference?"

Only write if confirmed.

---

## Operation: Maintain

Housekeeping tasks — run when user asks to "clean up the recipe database" or automatically
flag issues found during other operations.

### Seed defaults

Check for the five standing default stubs. Create any that are missing:

- `chicken-fajitas.md`
- `veggie-bean-chilli.md`
- `roast-veg-and-halloumi.md`
- `chicken-and-veg-tray-bake.md`
- `homemade-omelette.md`

Use the canonical template. Set `times_cooked: 0`, `last_cooked: null`. Notify the user
which stubs were created.

### Schema validation

For each recipe note in `Recipes/`:

- Check required frontmatter fields are present (name, ingredients, dietary, times_cooked,
  last_cooked)
- Check `dietary.fish_free` and `dietary.seafood_free` are explicitly set
- Flag any notes missing these fields

Report issues as a list; offer to fix them one by one or in bulk.

### Duplicate detection

If two recipe names are very similar (e.g. "chicken tray bake" and "chicken and veg tray
bake"), flag them and ask the user if they should be merged.

---

## Edge cases

| Situation                                       | Handling                                                                                                          |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Recipe note not found by name                   | Try fuzzy search; offer closest matches; offer to create new                                                      |
| Duplicate recipe names                          | Show both; ask user to confirm which to edit/log                                                                  |
| User pastes a recipe URL but Chrome unavailable | Ask user to paste the recipe text directly                                                                        |
| Drafted recipe from knowledge                   | Always label as drafted; require user confirmation before saving                                                  |
| Fish/seafood ingredient found                   | Flag allergy, set dietary flags false, confirm before saving                                                      |
| `times_cooked` missing from an existing note    | Default to 0 before incrementing; flag as schema issue                                                            |
| User wants to delete a recipe                   | Confirm explicitly: "Are you sure you want to delete [name]? This can't be undone." Then use `delete_vault_file`. |
| Backfill finds a file with partial frontmatter  | Don't overwrite existing fields — only add missing ones; treat as a schema validation task                        |
| Backfill finds a file that isn't a recipe       | Skip silently in batch mode; report in summary                                                                    |
| Backfill — ingredients and method not separable | Show the full text; ask user to point to where ingredients end and method begins                                  |
