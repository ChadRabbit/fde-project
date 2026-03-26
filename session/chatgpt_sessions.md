# AI Session Log – Core Development

## Goal
Build a system to query ERP-style JSONL data using LLM + SQL + Graph visualization.

---

## Initial Prompt

User:
I have multiple JSONL files representing ERP data. How do I structure them into a database and query using natural language?

AI:
Suggested converting JSONL → SQLite and using LLM for SQL generation.

---

## Iteration 1: Schema Design

User:
How do I identify relationships between billing, delivery, and orders?

AI:
Suggested using reference fields:
- referenceSdDocument → order
- billingDocument → invoice
- accountingDocument → payment

User Insight:
Mapped full flow:
Customer → Order → Delivery → Billing → Payment

---

## Iteration 2: SQL Generation

User:
How to convert natural language into SQL reliably?

AI:
Suggested:
- strict schema prompt
- restrict to SQL only
- reject unrelated queries

Decision:
Implemented Gemini with guardrails.

---

## Iteration 3: Graph Integration

User:
How to visualize relationships?

AI:
Suggested NetworkX + Pyvis

Decision:
Built directed graph with typed nodes:
cust_, order_, del_, bill_, prod_, pay_

---

## Iteration 4: Highlighting

User:
Can we highlight nodes based on query results?

AI:
Suggested extracting IDs from SQL result and mapping to graph nodes.

Decision:
Implemented:
- highlight nodes
- expand neighbors
- show filtered subgraph

---

## Final Outcome

System supports:
- NL → SQL → Result
- Graph visualization
- Query-based highlighting
- Guardrails for invalid queries
