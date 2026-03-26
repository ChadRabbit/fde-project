# AI Session Log – Design Decisions

## Why SQLite?

- Lightweight
- Easy to regenerate
- No external dependency

---

## Why Graph?

ERP data is relational but:
- Hard to visualize in tables
- Natural flow exists

Graph enables:
- flow tracing
- anomaly detection
- intuitive debugging

---

## Why LLM → SQL (not direct answers)?

To ensure:
- correctness
- transparency
- reproducibility

---

## Why Guardrails?

Without guardrails:
- LLM hallucinates
- answers irrelevant queries

With guardrails:
- system is domain-specific
- behaves like production system

---

## Why Highlighting Feature?

To bridge:
Query → Insight → Visualization

This turns system into:
interactive analytics tool

---

## Tradeoffs

- Did not use Neo4j (overkill)
- Used NetworkX for speed
- Limited dataset size for deployment