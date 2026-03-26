# AI Session Log – Debugging

## Issue 1: SQL execution failing

Error:
SQL query contained ```sql markdown

Fix:
- Added regex cleaning
- Extracted only SELECT statements

---

## Issue 2: Graph colors not updating

Problem:
Graph still showing old colors

Root Cause:
graph.html not being regenerated

Fix:
- Ensured save_graph() runs before rendering
- Cleared browser cache

---

## Issue 3: All nodes grey

Problem:
Highlight mode active with empty set

Fix:
- Added condition:
  if not highlight_nodes → show full colors

---

## Issue 4: Wrong relationships

Problem:
Graph had disconnected clusters

Root Cause:
Missing delivery layer

Fix:
- Added delivery_items table
- Connected:
  Order → Delivery → Billing

---

## Issue 5: Deployment failure

Problem:
Absolute path used for dataset

Fix:
- Switched to relative path
- Moved dataset inside repo