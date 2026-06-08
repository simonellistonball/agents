# Nutritionist assessment — single recipe framework

Used by the Assess operation in recipe-manager. More granular than the weekly plan
critique in the meal-planner skill's `references/nutritionist-framework.md` — this
focuses on a single dish rather than a week's pattern.

---

## Assessment dimensions

### 1. Protein adequacy
- Estimate grams of protein per serving based on main ingredients
- Reference: chicken thigh ~28g/100g cooked, eggs ~6g each, halloumi ~18g/100g,
  cannellini beans ~9g/100g, pancetta ~15g/30g serving
- **Flag**: <15g protein per serving for a dinner
- **Flag**: protein is entirely from processed meat (pancetta, bacon, sausage) with no
  whole protein source

### 2. Inflammatory signals
Score each ingredient as neutral, mildly inflammatory, or concerning:

| Ingredient type | Signal |
|---|---|
| Olive oil, avocado oil | Anti-inflammatory ✓ |
| Vegetables, legumes, whole grains | Anti-inflammatory ✓ |
| Oily fish (salmon, sardines, mackerel) | Anti-inflammatory ✓ |
| Nuts and seeds | Anti-inflammatory ✓ |
| Refined white flour (tortillas, pasta) | Mildly inflammatory — note |
| Commercial sauces / spice kits | Check for seed oils and added sugar — flag if present |
| Processed/cured meat (pancetta, salami) as a main protein | Mildly inflammatory — note |
| Processed/cured meat as a garnish (<30g per serving) | Acceptable |
| Hard cheese (halloumi, cheddar) as a main protein | Saturated fat load — note portion |
| Seed oils (sunflower, vegetable, rapeseed) as cooking oil | Flag — suggest swap to olive oil |

### 3. Phytonutrient density
Count the number of distinct vegetables/plant foods in the recipe:
- 0–1: **Low** — flag
- 2–3: **Moderate** — acceptable
- 4+: **Good**

Note presence of:
- Cruciferous veg (broccoli, cauliflower, kale, cabbage, Brussels) — strongest evidence
- Dark leafy greens (spinach, rocket, cavolo nero, chard)
- Alliums (onion, garlic, leeks, shallots) — anti-inflammatory
- Colourful produce (tomatoes, peppers, aubergine, carrots, beetroot)

### 4. Glycaemic impact
Consider:
- Is the main carbohydrate refined (white flour, white rice, white pasta)?
- Is there fibre to slow glucose absorption (beans, vegetables, whole grains)?
- Is there protein and fat alongside the carbohydrate? (Both blunt glucose response)

**Flag**: refined carb is the dominant ingredient with no fibre or fat pairing

### 5. Saturated fat load
- Estimate grams of saturated fat per serving
- Reference: halloumi ~11g/100g, cheddar ~21g/100g, pancetta ~8g/30g serving,
  chicken thigh (skin off) ~3g/100g
- **Flag**: >15g saturated fat per serving in a dinner
- **Note**: if halloumi or hard cheese is main protein, recommend 80–100g per person max

### 6. Omega-3 presence
- Is there any omega-3 source? (oily fish, walnuts, flaxseed, chia, pecans, hemp seeds)
- Note: plant omega-3 (ALA) is less bioavailable than marine (EPA/DHA) — worth noting
  but don't over-penalise plant sources
- **Flag**: no omega-3 source at all (this is weak evidence for a single meal; mention
  briefly rather than as a major concern)

### 7. Allergy and safety check
- Re-verify against Lizzie's allergy even if dietary flags are set
- Check for hidden fish/seafood: anchovies in Worcestershire sauce, fish sauce, prawn
  crackers used as garnish
- If any concern: flag clearly with the specific ingredient

---

## Output structure

```
**[Recipe name] — nutritionist assessment**

**Overall: [one sentence] — Grade: [A/B/C/D]**

**Strengths**
[2–3 specific positive observations]

**Concerns**
[1–4 specific concerns with actionable suggestions]
If none: "No significant concerns."

**Per-serving snapshot** (estimated)
- Protein: ~Xg
- Saturated fat: ~Xg
- Phytonutrient score: Low / Moderate / Good
- Inflammatory profile: Low / Moderate / Elevated

**Allergy status**
- Fish-free: ✓ / ⚠️ [ingredient]
- Seafood-free: ✓ / ⚠️ [ingredient]
```

---

## Grading rubric (single recipe)

| Grade | Meaning |
|---|---|
| A | Strong on most dimensions. Minor tweaks only. |
| B | Good base; one or two fixable concerns. |
| C | Useful dish but meaningful nutritional gaps or inflammatory signals. |
| D | Significant concerns — processed ingredients dominant, very low veg, or allergy risk. |

---

## Tone
Same as the weekly framework: direct, specific, evidence-referenced, not preachy.
One flag per issue. Acknowledge what's good first. Never suggest removing the dish
entirely — always offer a modification instead.
