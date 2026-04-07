---
name: ecosystem-flow-diagram
description: >
  Creates interactive D3.js Sankey-style ecosystem flow diagrams showing relationships 
  between entities with data flows, revenue streams (recurring vs one-off), product 
  delivery, revenue splits, and optional company sub-nodes. Use when visualizing 
  business ecosystems, marketplace dynamics, platform relationships, or any multi-stakeholder 
  system with data, money, and product flows.
triggers:
  - "create an ecosystem diagram"
  - "visualize how data flows"
  - "visualize how money flows"
  - "show the relationships in our marketplace"
  - "show the relationships in our platform"
  - "map out the business model"
  - "revenue splits diagram"
  - "sankey diagram for business"
  - "data marketplace visualization"
  - "platform ecosystem map"
tools:
  - create_file
  - view
  - str_replace
  - bash_tool
output_format: html
---

# Ecosystem Flow Diagram Skill

## Overview

Creates interactive D3.js Sankey-style ecosystem flow diagrams showing relationships between entities with data flows, revenue streams (recurring vs one-off), product delivery, revenue splits, and optional company sub-nodes.

## When to Trigger

- "Create an ecosystem diagram showing..."
- "Visualize how data/money flows between..."
- "Show the relationships in our marketplace/platform"
- "Map out the business model with revenue splits"
- Requests involving multiple stakeholders with data, revenue, or product flows

## Elicitation Strategy

**Goal: Understand the CONTENT, not the implementation.** Ask focused questions about what the user wants to show, not how it should be built.

### Phase 1: Core Entities (Required)

Ask: **"What are the main entities/stakeholders in your ecosystem?"**

Probe for:

- Who generates/owns the data or value?
- Who aggregates or brokers it?
- Who consumes or pays for it?
- Any infrastructure providers?

Help them think in layers (left-to-right flow):

- **Layer 0**: Sources/Origins (users, data generators)
- **Layer 1**: Owners/Collectors (first-party holders)
- **Layer 2**: Platforms/Brokers (aggregators, marketplaces)
- **Layer 3**: Consumers/Buyers (end services, purchasers)

### Phase 2: Connections (Required)

Ask: **"How do these entities connect? What flows between them?"**

For each connection, clarify:

1. **Direction**: Who sends to whom?
2. **What flows**: Data? Money? Products/services?
3. **Label**: What would you call this flow?

**Flow types to identify:**
| Type | Question to Ask |
|------|-----------------|
| Data | "Where does data/information flow?" |
| Revenue (recurring) | "Who pays whom regularly? Subscriptions, ongoing fees?" |
| Revenue (one-off) | "Any one-time purchases or occasional payments?" |
| Product | "Who delivers products/services to whom?" |
| Potential | "Any uncertain or speculative relationships?" |

### Phase 3: Revenue Splits (If applicable)

Ask: **"When money flows, does it get split between multiple parties?"**

Probe for:

- Does a platform/broker take a commission? What percentage?
- Is the remainder split further? To whom and what percentages?
- Are there any revenue share arrangements?

Example: "When customers pays for data, does the broker take a cut before passing to suppliers?"

### Phase 4: Relative Importance (Optional)

Ask: **"Should any connections appear more or less prominent than others?"**

Help them think about:

- Primary vs secondary flows
- High volume vs low volume
- Critical vs optional relationships

Use weight scale: 1-2 (thin) → 5 (normal) → 8-10 (thick)

### Phase 5: Example Companies (Optional)

Ask: **"Would you like to show example companies for each entity? (These expand on click)"**

If yes, suggest 4-6 examples per entity based on the domain.

### Phase 6: Node Details (Optional)

Ask: **"For the details panel, what should each entity show?"**

- Role/classification
- Description
- Types of data/services handled

## Key Implementation Details

### Node Structure

```javascript
{
  id: 'uniqueId',           // lowercase, no spaces
  label: 'Display Name',    // use \n for line breaks
  layer: 0,                 // 0-3 for positioning
  color: '#hex',            // see color palette below
  radius: 55,               // 80 for central/broker nodes
  description: 'Text',
  role: 'Classification',
  dataTypes: 'What flows through'
}
```

### Edge Structure

```javascript
{
  source: 'sourceId',
  target: 'targetId',
  type: 'data|revenue|oneoff|product|potential',
  label: 'Flow description',
  weight: 5.0,              // 1-10, multiplied by 10 for display
  brokerCommission: 0.20,    // Optional: broker takes 20%
  split: [{                 // Optional: manual splits
    target: 'nodeId',
    ratio: 0.80,
    label: '80%'
  }]
}
```

### Company Node Structure

```javascript
{
  id: 'companyId',
  label: 'Company Name',
  parent: 'parentNodeId',
  color: '#matchParent'
}
```

## Color Palette

### Edge Colors (Built-in)

- `data`: Cyan (#00d4ff)
- `revenue`: Dark green (#16a34a) - recurring
- `oneoff`: Light green (#86efac) - one-time
- `product`: Purple (#a78bfa)
- `potential`: Pink dashed (#fda4af)

### Suggested Node Colors by Role

- Sources/Users: `#3b82f6` (blue)
- Owners/Collectors: `#10b981` (teal)
- Platforms/Brokers: `#f59e0b` (amber) - use radius: 80
- Consumers/Services: `#8b5cf6` (purple)
- Infrastructure: `#ec4899` (pink)

## Features Included in Template

### Automatic Features

- Node collision avoidance for edges
- Split point auto-positioning (1/3 from source toward weighted centroid)
- Labels along curved paths with auto-flip for readability
- Perpendicular alignment for split branches
- Responsive full-screen layout

### Interactive Features

- **Drag nodes** to reposition
- **Drag split points** to manually adjust (locks in place, golden indicator)
- **Double-click split** to unlock and return to auto
- **Click nodes** to select and view details
- **Hover nodes** to highlight all connected edges (cascades through splits)

### UI Panels

- **Flow Controls** (top-left): Toggle each edge type, companies, animation
- **Legend** (top, next to controls): Color key
- **Instructions** (top-right): User guidance
- **Details Panel** (bottom-left): Selected node info
- **Inbound Panel** (bottom-center): Incoming connections with splits
- **Outbound Panel** (bottom-right): Outgoing connections with splits

## Example Conversation Flow

```
User: "Create a diagram showing how game player data flows to AI companies"

Claude: "I'd be happy to create an ecosystem flow diagram. Let me understand the content:

**1. What entities are involved?**
For example: Players, Game Developers, a Platform, AI Labs, etc.

**2. How do they connect?**
- Where does data flow?
- Who pays whom? (regularly or one-time?)
- Who delivers products/services?

**3. Any revenue splits?**
Does the platform take a commission when payments flow through?

**4. Should any connections be emphasized?**
Primary flows vs secondary?

**5. Want example companies shown for each entity?**"

User: [Provides answers]

Claude: [Generates complete HTML with all features]
```

## Template Location

Use `TEMPLATE.html` in this skill folder. Replace:

1. `nodes` array with user's entities
2. `edges` array with user's connections
3. `companyNodes` array (or empty `[]`)
4. Page `<title>` with diagram name

## Common Patterns

### Platform Marketplace

- Sources → Platform → Consumers
- Revenue flows back with platform commission
- Product/service delivery flows forward

### Data Broker Model

- Data sources → Aggregator → Data buyers
- Split revenue between source owners and broker

### Multi-sided Platform

- Multiple source types feeding one broker
- Multiple consumer types receiving different products
- Revenue from consumers split back to sources

## Weight Guidelines

| Weight  | Display Width | Use For                |
| ------- | ------------- | ---------------------- |
| 1.0-2.0 | 10-20px       | Minor/secondary flows  |
| 3.0-4.0 | 30-40px       | Supporting flows       |
| 5.0     | 50px          | Primary/default flows  |
| 6.0-8.0 | 60-80px       | Emphasized/high-volume |
| 10.0    | 100px         | Dominant flows         |

## Customization Points in Template

When using the template, these are the sections to modify:

### 1. Title (line ~5)

```html
<title>Your Ecosystem Name</title>
```

### 2. Nodes Array (search for `const nodes = [`)

Replace with user's entities following the node structure above.

### 3. Edges Array (search for `const edges = [`)

Replace with user's connections following the edge structure above.

### 4. Company Nodes Array (search for `const companyNodes = [`)

Replace with example companies, or use `[]` if not needed.

### 5. Layer Positions (search for `const layerPositions`)

Adjust if using different number of layers:

```javascript
const layerPositions = {
  0: width * 0.08, // Far left
  1: width * 0.28, // Left-center
  2: width * 0.52, // Center (broker)
  3: width * 0.82, // Right
};
```

## Files in This Skill

- `SKILL.md` - This file (elicitation guide and implementation reference)
- `TEMPLATE.html` - Complete working template with all features
- `EXAMPLES.md` - Example configurations and data structures
