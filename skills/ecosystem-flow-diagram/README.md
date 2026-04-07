# Ecosystem Flow Diagram Skill

## Installation

To install this skill, copy the `ecosystem-flow-skill` folder to your Claude skills directory:

## Contents

- **SKILL.md** - Main skill documentation with elicitation questions and implementation guide
- **TEMPLATE.html** - Complete working D3.js template with all features
- **EXAMPLES.md** - Concrete examples including the a Data Marketplace configuration

## What This Skill Creates

Interactive Sankey-style ecosystem flow diagrams with:

### Visual Features

- Draggable nodes with collision avoidance
- 5 edge types: Data (cyan), Recurring Revenue (dark green), One-off Revenue (light green), Product (purple), Potential (pink dashed)
- Revenue split visualization with draggable/lockable split points
- Expandable company sub-nodes
- Hover highlighting that cascades through splits

### UI Panels

- Flow controls (toggle edge types)
- Legend
- Node details panel
- Inbound/outbound connections panels

## Key Innovation: Content-Focused Elicitation

The skill guides Claude to ask the right questions BEFORE generating:

1. **Entities**: Who are the stakeholders? What layers do they belong to?
2. **Connections**: What flows between them (data, money, products)?
3. **Splits**: Does revenue get split? What percentages?
4. **Importance**: Which flows should be emphasized?
5. **Companies**: Want example companies for each entity?

This avoids the iterative refinement that happened in the original conversation.

## Usage Example

```
User: "Create a diagram showing our marketplace ecosystem"

Claude: [Asks focused elicitation questions about entities, flows, splits]

User: [Provides answers]

Claude: [Generates complete HTML diagram in one shot]
```

## Based On

27 iterations of refinement from a real conversation building the a Data Marketplace ecosystem diagram.
