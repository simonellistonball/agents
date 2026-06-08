# Recipe database — schema and conventions

All recipe notes live in `Recipes/` at the top level of the Obsidian vault.
One note per recipe, filename = recipe name in kebab-case (e.g. `chicken-fajitas.md`).

---

## Recipe note template

```markdown
---
name: "Recipe Name"
tags: [recipe]
ingredients:
  - chicken thigh
  - red pepper
  - fajita kit
  - soured cream
cuisine: Mexican
meal_type: dinner
prep_time_mins: 15
cook_time_mins: 20
serves: 2
last_cooked: 2026-06-01
times_cooked: 3
nutritionist_flags:
  - "Commercial fajita kit contains refined flour and added sugar — swap for corn tortillas"
dietary:
  vegetarian: false
  vegan: false
  fish_free: true
  seafood_free: true
---

# Recipe Name

Brief description of the dish.

## Ingredients
- Item 1
- Item 2

## Method
1. Step one
2. Step two

## Notes
General tips, substitutions, serving suggestions.

## Cook log
- **2026-06-01** — Used M&S chicken thighs. Swapped kit tortillas for corn tortillas. Good.
- **2026-03-14** — Standard run. No changes.
```

---

## Field definitions

| Field | Type | Notes |
|---|---|---|
| `name` | string | Display name of the recipe |
| `tags` | list | Always include `recipe`; add others freely (e.g. `batch-cook`, `quick`) |
| `ingredients` | list | Lowercase, simplified names — these are used for ingredient matching |
| `cuisine` | string | Optional but useful |
| `meal_type` | string | `dinner`, `lunch`, `breakfast`, or `any` |
| `prep_time_mins` | int | Active prep time |
| `cook_time_mins` | int | Passive/oven time |
| `serves` | int | Default serving size |
| `last_cooked` | date | ISO format `YYYY-MM-DD` — updated by skill each run |
| `times_cooked` | int | Incremented by skill each run |
| `nutritionist_flags` | list | Concerns identified during critique; strings, human-readable |
| `dietary.fish_free` | bool | Must be `true` for all shared meals (Lizzie's allergy) |
| `dietary.seafood_free` | bool | Must be `true` for all shared meals |

---

## Ingredient matching conventions

When searching for recipes matching a delivery's ingredients, the skill searches the
`ingredients` frontmatter list. Use these simplified forms consistently:

| Receipt label | Ingredient tag to use |
|---|---|
| M&S Oakham Gold Chicken Thigh Fillets 1kg | `chicken thigh` |
| Cypressa Traditional Halloumi Cheese 225g | `halloumi` |
| Epicure Cannellini Beans 400g | `cannellini beans` |
| Unearthed Diced Pancetta | `pancetta` |
| Unearthed Spinach Spanish Omelette | `spinach omelette (ready-made)` |
| Clarence Court Burford Buff Eggs | `eggs` |
| Ocado Courgettes | `courgette` |
| M&S Red Peppers | `red pepper` |
| Ocado Red Onions | `red onion` |
| Galbani Mini Italian Mozzarella | `mozzarella` |
| M&S British Soured Cream | `soured cream` |

Always use singular form and lowercase. Strip brand names and pack sizes.

---

## Updating a recipe note after cooking

Use `obsidian-mcp-tools:patch_vault_file` to:
1. Update frontmatter fields: `last_cooked`, `times_cooked`
2. Append to `## Cook log` section with the date and any session notes

Example patch for cook log:
```
## Cook log
- **2026-06-01** — [auto-logged by meal planner] Used with Ocado delivery. No tweaks.
```

If `nutritionist_flags` need updating, surface the proposed change to the user before writing:
> "The critique flagged [issue] for [recipe]. Shall I add this to the recipe note?"

---

## Creating a new recipe note

Use `obsidian-mcp-tools:create_vault_file` with path `Recipes/[recipe-name-kebab].md`.
Populate all known fields from the current session. Leave `times_cooked: 1` and
`last_cooked` as today. Leave `## Method` and `## Notes` with placeholder text if unknown:
```
## Method
_Add method here._

## Notes
_Add notes here._
```

The user can fill these in later directly in Obsidian.

---

## Seed recipes (create these stubs on first run if not present)

The following are the standing defaults. Check for their existence on every run and create
stubs if missing:

- `chicken-fajitas.md`
- `veggie-bean-chilli.md`
- `roast-veg-and-halloumi.md`
- `chicken-and-veg-tray-bake.md`
- `homemade-omelette.md`
