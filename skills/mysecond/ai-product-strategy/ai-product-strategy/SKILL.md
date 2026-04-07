---
name: ai-product-strategy
description: 'Develop AI product strategy and identify AI opportunities for your product. Use when: ai strategy, ai product, ai features, ai roadmap, ai opportunities, build vs buy ai.'
---

# AI Product Strategy

Develop AI product strategy and identify AI opportunities for your product.

## When to Use This Skill
- Evaluating AI opportunities for your product
- Deciding between build, buy, or partner for AI features
- Assessing data readiness and moat potential
- Planning AI feature roadmap
- Evaluating AI vendors or partners

## What You'll Need
- Description of your product and users (context/product.md helps)
- Understanding of user pain points or workflow inefficiencies
- Current data assets (what data you have access to)
- (Optional) Specific AI use case you're evaluating

## Process

### Step 1: Check Your Context
First, read the user's context files to understand their product and market position.

What to look for:
- `context/product.md` — What product features exist? What workflows could be automated?
- `context/personas.md` — What repetitive tasks drain user time? What decisions require expertise?
- `context/competitors.md` — Who's already using AI? Is it table stakes or differentiation?
- `context/company.md` — What's the strategic priority? Move fast or build defensible moat?

**Tell the user what you found.** For example:
> "I see you're a B2B SaaS project management tool for agencies. Your personas mention spending 4 hours/week on manual status reports. Competitors like Monday.com have basic AI features. Let me explore AI opportunities."

### Step 2: Identify AI Opportunity Areas
Based on their product and user workflows, identify 3-5 potential AI opportunities.

**Categories to explore:**
- **Automation** — Repetitive tasks users do manually
- **Prediction** — Forecasting outcomes based on patterns
- **Personalization** — Tailoring experience to user behavior
- **Content Generation** — Creating text, summaries, templates
- **Data Analysis** — Finding insights in complex data
- **Decision Support** — Recommending actions based on context

**Prioritize by:**
- User value (does this solve a real pain?)
- Feasibility (can we build/buy this now?)
- Data availability (do we have the inputs?)
- Competitive advantage (is this differentiating or table stakes?)

### Step 3: Build vs Buy vs Partner Analysis
For the top 2-3 opportunities, evaluate the approach.

**Build (in-house):**
- ✅ When: Unique data, core differentiator, long-term moat potential
- ❌ When: Commodity feature, rapid time-to-market needed, limited ML expertise

**Buy (third-party API):**
- ✅ When: Table stakes, proven vendors, fast implementation needed
- ❌ When: Vendor lock-in risk, unique use case, data privacy concerns

**Partner (co-develop or integrate):**
- ✅ When: Complementary strengths, shared go-to-market, complex integration
- ❌ When: Misaligned incentives, dependency risk, unclear ownership

### Step 4: Data Moat Assessment
Evaluate whether AI creates a defensible advantage.

**Questions to answer:**
1. **Do you have proprietary data?** Unique data = potential moat
2. **Does the model improve with usage?** Data flywheel effect
3. **Can competitors replicate this?** Switching costs, network effects
4. **Time to defensibility?** How long until the moat is meaningful?

**Red flags:**
- Using only public data → No moat
- One-time model training → No flywheel
- Vendor API with no customization → Commoditized
- Easy to replicate → Not defensible

### Step 5: UX and Trust Considerations
AI requires different UX patterns than traditional features.

**Key principles:**
- **Transparency** — Show confidence scores, explain reasoning
- **User control** — Let users edit, override, or disable AI
- **Graceful failures** — Handle errors without breaking workflow
- **Progressive disclosure** — Start simple, reveal complexity as needed
- **Trust building** — Consistency, accuracy, and reliability over time

**Common UX mistakes:**
- Black box outputs with no explanation
- No way to correct mistakes
- AI takes over critical decisions without user review
- Inconsistent quality damages trust

### Step 6: Implementation Roadmap
Create phased approach from MVP to full vision.

**Phase 1: MVP (Prove Value)**
- Smallest possible feature that solves user pain
- Manual fallbacks if AI fails
- Limited scope, controlled rollout
- Success metric: User adoption and satisfaction

**Phase 2: Expansion (Scale & Refine)**
- Expand to more use cases
- Improve accuracy with production data
- Reduce manual interventions
- Success metric: Usage frequency, accuracy improvement

**Phase 3: Differentiation (Build Moat)**
- Proprietary data advantages
- Network effects or switching costs
- Advanced features competitors can't match
- Success metric: Retention, competitive win rate

### Step 7: Risk and Mitigation Planning
Identify risks across value, usability, feasibility, and viability.

**Value risks:**
- Users don't trust AI outputs
- Accuracy not good enough to be useful
- Solving the wrong problem

**Usability risks:**
- Too complex to use
- Errors break user workflow
- No way to verify correctness

**Feasibility risks:**
- Insufficient training data
- Model accuracy below threshold
- Latency or cost too high

**Viability risks:**
- Regulatory or legal constraints
- Customer data privacy concerns
- Vendor lock-in or dependency

## Output Template

```markdown
# AI Product Strategy: [Product Name]

**Date:** [Date]
**Owner:** [PM Name]
**Status:** Draft | Review | Approved

## Context from Your Files
*What I found in your context:*
- **Product:** [Summary from product.md]
- **Users:** [Key personas and pain points]
- **Competitors:** [Who's using AI? How?]
- **Strategic priority:** [From company.md]

## AI Opportunity Assessment

### High-Impact Opportunities

#### 1. [Opportunity Name]
- **User value:** [What pain does this solve?]
- **Example:** [Concrete user story]
- **Feasibility:** High / Medium / Low — [Why?]
- **Data requirements:** [What data needed?]
- **Competitive context:** [Table stakes or differentiator?]
- **Recommended approach:** Build / Buy / Partner

#### 2. [Opportunity Name]
- **User value:** [What pain does this solve?]
- **Example:** [Concrete user story]
- **Feasibility:** High / Medium / Low — [Why?]
- **Data requirements:** [What data needed?]
- **Competitive context:** [Table stakes or differentiator?]
- **Recommended approach:** Build / Buy / Partner

### Medium-Impact Opportunities

#### 3. [Opportunity Name]
- **User value:** [Brief description]
- **Feasibility:** [Assessment]
- **Recommended approach:** [Build/Buy/Partner]

## Build vs Buy vs Partner Analysis

### For [Top Opportunity]: Recommended → [Approach]

#### Build (In-House)
**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Data moat potential:** [Assessment]
**Timeline:** [Estimate]
**Team required:** [Skills/headcount needed]

#### Buy (Third-Party API)
**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Vendor options:**
1. [Vendor A] — [Strengths/pricing]
2. [Vendor B] — [Strengths/pricing]

**Timeline:** [Estimate]
**Monthly cost:** [Estimate]

#### Partner (Co-Develop)
**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Potential partners:**
1. [Partner A] — [Why good fit]
2. [Partner B] — [Why good fit]

**Timeline:** [Estimate]
**Commercial terms:** [Revenue share, licensing, etc.]

### Recommendation: [Build/Buy/Partner]

**Why this approach:**
[1-2 paragraph rationale considering user value, time-to-market, cost, and strategic fit]

## Data Moat Assessment

**Current data advantage:**
- ✅ **Yes** — [Describe proprietary data]
- ⬜ **Partial** — [What data exists, what's missing]
- ❌ **No** — [Using only public/vendor data]

**Data flywheel potential:**
- **Does usage generate better data?** [Yes/No — how?]
- **Do outcomes improve model?** [Yes/No — mechanism?]
- **Can data be used across products?** [Yes/No — synergies?]

**Competitive defensibility:**
- **Can competitors access same data?** [Yes/No]
- **Switching cost after AI adoption?** [High/Medium/Low]
- **Time to build meaningful advantage?** [Estimate]

**Verdict:** [Durable moat / Temporary advantage / Commodity feature]

## UX Considerations

### Transparency & Trust
**How users will understand AI:**
- [Confidence scores, explanations, citations, etc.]

**How to build trust:**
- [Consistency, accuracy benchmarks, user control, etc.]

### User Control
**What users can adjust:**
- [Settings, preferences, override mechanisms]

**Fallback to manual:**
- [How users work without AI if needed]

### Failure Modes
**What happens when AI is wrong:**
- [Error handling, user notifications, graceful degradation]

**How users verify correctness:**
- [Review workflows, validation steps, feedback loops]

### Progressive Rollout
**Phase 1 UX:** [Basic version]
**Phase 2 UX:** [Enhanced capabilities]
**Phase 3 UX:** [Advanced features]

## Implementation Roadmap

### Phase 1: MVP — Prove Value
**Timeline:** [Estimate]
**Scope:**
- [Feature 1]
- [Feature 2]

**Success criteria:**
| Metric | Target | Why It Matters |
|--------|--------|---------------|
| [Metric 1] | [Target] | [Rationale] |
| [Metric 2] | [Target] | [Rationale] |

**Key risks:**
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

### Phase 2: Expansion — Scale & Refine
**Timeline:** [Estimate]
**Scope:**
- [Feature 1]
- [Feature 2]

**Success criteria:**
| Metric | Target | Why It Matters |
|--------|--------|---------------|
| [Metric 1] | [Target] | [Rationale] |

**Dependencies:**
- [Dependency 1]
- [Dependency 2]

### Phase 3: Differentiation — Build Moat
**Timeline:** [Estimate]
**Scope:**
- [Feature 1]
- [Feature 2]

**Success criteria:**
| Metric | Target | Why It Matters |
|--------|--------|---------------|
| [Metric 1] | [Target] | [Rationale] |

**Moat indicators:**
- [Indicator 1]: [How to measure]
- [Indicator 2]: [How to measure]

## Risks & Mitigations

*Risk types: V=Value, U=Usability, F=Feasibility, B=Business Viability. Impact: H=High, M=Medium, L=Low*

| Risk | Type | Impact | Mitigation |
|------|------|--------|------------|
| [Risk 1] | V/U/F/B | H/M/L | [Mitigation plan] |
| [Risk 2] | V/U/F/B | H/M/L | [Mitigation plan] |
| [Risk 3] | V/U/F/B | H/M/L | [Mitigation plan] |

## Open Questions

| Question | Assumption | How to Validate | Timeline |
|----------|-----------|-----------------|----------|
| [Question 1] | [What we're assuming] | [Experiment to run] | [When we need answer] |
| [Question 2] | [What we're assuming] | [Experiment to run] | [When we need answer] |

## Next Steps

**Immediate (This Week):**
1. [Action 1]
2. [Action 2]

**Short-term (This Month):**
1. [Action 1]
2. [Action 2]

**Long-term (This Quarter):**
1. [Action 1]
2. [Action 2]
```

## Framework Reference

This skill draws on:
- **Marty Cagan's V/U/F/V Risk Framework** (*Inspired*, *Empowered*) — Systematic risk assessment
- **Andrew Ng's AI Transformation Playbook** — Build vs buy decision framework
- **Ben Evans on AI Moats** — Data advantages and defensibility
- **Julie Zhuo on Product Strategy** — User value first, technology second

## Tips for Best Results

1. **Start with user pain, not AI capabilities** — AI is a means, not an end
2. **Be honest about data assets** — No proprietary data? Building in-house may not create a moat
3. **Consider regulatory landscape** — AI in healthcare, finance, education has compliance requirements
4. **Plan for trust-building** — Users need time to trust AI; start conservatively
5. **Measure early and often** — Track accuracy, adoption, and satisfaction from day 1
6. **Don't underestimate UX** — Poor AI UX destroys trust faster than good AI builds it
