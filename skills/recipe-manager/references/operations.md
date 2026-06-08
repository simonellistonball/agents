# Operations reference

Detailed guidance for the Add and Edit operations. Read the relevant section before
executing — these contain the decisions that aren't obvious from the SKILL.md alone.

---

## § Add

### Ingredient normalisation rules
Strip all of the following before saving to the `ingredients` frontmatter list:
- Brand names (M&S, Ocado, Waitrose, Unearthed, Cypressa, etc.)
- Pack sizes and weights (1kg, 400g, 2 per pack, etc.)
- Qualifiers that don't affect matching (British, Italian, Ripe & Ready, etc.)
- Plurals → use singular form

Examples:
| Raw | Normalised |
|---|---|
| M&S Oakham Gold Chicken Thigh Fillets 1kg | `chicken thigh` |
| Cypressa Traditional Halloumi Cheese 225g | `halloumi` |
| Clarence Court Burford Buff 10 Medium Free Range Eggs | `eggs` |
| Ocado Courgettes 500g | `courgette` |
| Unearthed Diced Pancetta 2 x 77g | `pancetta` |
| Fresh lemon juice | `lemon` |

### Dietary flag logic
Set flags based on ingredients:

| Flag | Set to `true` when... |
|---|---|
| `vegetarian` | No meat, poultry, or fish. Eggs and dairy are OK. |
| `vegan` | No animal products at all (no meat, fish, dairy, eggs, honey) |
| `fish_free` | No fish of any kind (salmon, tuna, cod, sardines, anchovies, etc.) |
| `seafood_free` | No shellfish or seafood (prawns, crab, lobster, mussels, squid, etc.) |

Note: a recipe can be `fish_free: true` but `seafood_free: false` (e.g. a prawn dish).
For Lizzie's allergy, both must be `true` for shared meals. Flag either being `false`.

**Anchovies edge case**: many Italian and Mediterranean recipes use anchovies as a
background flavour (pasta sauces, dressings). Always flag these — they're easy to miss.

### Drafting from knowledge
When drafting a recipe Claude knows:
- Use standard quantities for 2 servings (the default household size)
- Give a concise method — 4–8 numbered steps is ideal
- Note common variations in `## Notes` (e.g. "swap pancetta for mushrooms for a
  vegetarian version")
- Be honest about uncertainty: if a technique or timing is approximate, say so in Notes

### Filename conventions
- kebab-case, all lowercase
- No articles (a, an, the) at the start
- Keep it short and recognisable
- Examples: `chicken-fajitas.md`, `roast-veg-halloumi.md`, `pasta-amatriciana.md`,
  `butternut-squash-soup.md`

---

## § Edit

### What can be patched vs what requires a full rewrite

`patch_vault_file` works by targeting a heading or block reference. It's reliable for:
- Appending to `## Cook log`
- Replacing the content of a named section (`## Method`, `## Notes`, `## Ingredients`)
- Updating individual frontmatter fields

It's less reliable for:
- Reordering sections
- Structural changes to the note layout

If the user wants a major restructure, fetch the full note content, apply changes in memory,
and use `create_vault_file` to overwrite (after confirming with the user).

### Frontmatter field edits
When editing frontmatter fields, fetch the current note first and confirm the current
value before changing. Example:

> "The current value for `serves` is 2. Changing to 4 — is that right?"

Never silently overwrite a field that has an existing non-null value without showing it.

### Nutritionist flags
These are the most sensitive field to edit. Always:
1. Show the current flags list
2. Show the proposed new/updated flags
3. Get explicit confirmation before writing
4. Log the change in the cook log section with today's date:
   ```
   - **YYYY-MM-DD** — [nutritionist flags updated]
   ```

---

## § Backfill

### What counts as "needs backfilling"
A file needs backfilling if it meets any of these conditions:
- No YAML frontmatter block at all (file doesn't start with `---`)
- Frontmatter exists but is missing any of: `ingredients`, `dietary`, `times_cooked`,
  `last_cooked` — the four fields the meal-planner requires to function
- Frontmatter exists but `ingredients` is an empty list `[]`

A file with partial frontmatter should be treated more carefully than a plain-text file —
preserve all existing fields and only add what's missing. Never overwrite a field that
already has a non-null value without surfacing it to the user.

### Inferring times when not stated
Use these heuristics when prep/cook times aren't explicitly given:

| Signal | Inference |
|---|---|
| "Quick", "15 minutes", "weeknight" in title or text | `prep_time_mins: 10`, `cook_time_mins: 15` |
| Oven mentioned with temperature | `cook_time_mins: 30` minimum; look for duration clue |
| "Slow cook", "braise", "overnight" | `cook_time_mins: 120` minimum |
| Stir-fry, stir, quick sauté | `prep_time_mins: 15`, `cook_time_mins: 10` |
| No clues at all | Omit the field rather than guess; leave as `null` |

Always mark inferred times with an inline note in `## Notes`:
```
_Prep and cook times estimated — update after first cook._
```

### Inferring cuisine
Use dish name and key ingredients as the primary signals:

| Signals | Cuisine |
|---|---|
| halloumi, za'atar, tahini, pomegranate | Middle Eastern |
| pancetta, parmesan, pasta, risotto | Italian |
| cumin, coriander, fajita, tortilla, chipotle | Mexican |
| soy sauce, ginger, sesame, rice wine | Asian (specify if clear: Japanese, Chinese, Thai) |
| harissa, ras el hanout, chickpea, preserved lemon | North African |
| feta, olive, oregano, lemon | Greek / Mediterranean |
| no clear signal | Leave as `null` |

Never guess cuisine from the dish name alone if the ingredients don't support it.

### Handling poorly structured source text
Recipe text copied from websites often has non-standard structure:

**Problem: ingredients embedded in method prose**
e.g. "Add 2 cloves of garlic and 400g tinned tomatoes, then stir for 5 minutes."

Strategy: extract ingredient names for the frontmatter list (`garlic`, `tinned tomato`)
and keep the original prose in `## Method` unchanged. Note in `## Notes`:
```
_Ingredients are woven into the method — see method for quantities._
```

**Problem: quantities and units in ingredient list**
e.g. "400g tinned tomatoes", "2 cloves garlic, minced"

Strategy: strip quantities and preparation notes for the frontmatter `ingredients` list
(used for matching only), but preserve the full lines with quantities in `## Ingredients`
(used for cooking).

Frontmatter: `ingredients: [tinned tomato, garlic]`
Section body: `- 400g tinned tomatoes` / `- 2 cloves garlic, minced`

**Problem: source text has rich formatting (bold, links, ads text)**
Strategy: strip all markdown formatting artefacts, links, and any text that is clearly
not part of the recipe (navigation text, copyright notices, "You might also like" sections).

### Batch mode confirmation strategy
In batch mode, never ask per-file unless:
1. An allergy ambiguity is found — always pause immediately
2. A recipe name is genuinely unresolvable — pause and note it in the summary

For all other ambiguities (inferred times, inferred cuisine, uncertain serves): apply the
inference, mark it in `## Notes` as estimated, and report it in the final batch summary
so the user can review later.

The goal in batch mode is to get all files to a valid, queryable state in one pass. Perfect
data is less important than consistent schema coverage.

---

## § Naming collisions

If a recipe with the same (or very similar) name already exists when attempting to Add:
1. Fetch and show the existing note summary
2. Ask: "A recipe called '[name]' already exists. Do you want to update it, save a new
   version with a different name, or cancel?"
3. If updating: run the Edit operation instead
4. If saving new: ask for a distinguishing name (e.g. "spicy-bean-chilli.md" vs
   "mild-bean-chilli.md")
