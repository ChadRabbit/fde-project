# Graph Based ERP Query System with LLM Integration

An interactive, graph driven query system built on top of semi structured ERP style JSONL data. The project transforms raw business records into relational tables and a navigable graph, then lets users ask questions in natural language and receive grounded answers backed by SQL results.

## Working Link:- https://fde-project-assignment.streamlit.app/
## Overview

Real ERP data is rarely stored in one clean table. Instead, business events are scattered across sales orders, deliveries, billing documents, accounting entries, products, customers, and address records. This project was built to handle exactly that kind of environment.

The system ingests nested JSONL files, normalizes them into SQLite, reconstructs relationships as a directed graph, and exposes everything through a Streamlit interface. Users can explore the full business flow visually, ask questions in plain English, and inspect the exact SQL that powers every answer.

The most important design choice in this project is that the LLM never answers freely. It only helps translate natural language into SQL over the known schema. Every answer is grounded in the dataset.

## What the project does

The application supports three main experiences.

1. A graph view that shows how customers, sales orders, deliveries, billing documents, products, and payments connect.
2. A conversational interface that turns user questions into SQL queries and executes them on SQLite.
3. A focused result view that highlights the exact nodes involved in the answer and shows a smaller graph around them.

It also includes a guardrail layer so irrelevant prompts are rejected instead of being answered incorrectly.

## Why this project exists

The assignment was designed to test more than coding ability. It was meant to evaluate how well a candidate can reason about messy data, infer relationships, choose a practical architecture, and build something useful quickly.

This project focuses on:

1. Data modeling from semi structured JSONL inputs.
2. Graph based representation of business flows.
3. Natural language to SQL translation.
4. Reliable querying with output grounded in the data.
5. Clear visual explanation of results.

## Architecture

The system follows a simple but effective pipeline.

1. Raw JSONL files are scanned recursively from the extracted dataset folder.
2. Relevant records are loaded into SQLite tables.
3. Relationship aware tables are used to build a directed graph.
4. The user asks a question in Streamlit.
5. Gemini converts the question into SQL when the query is in scope.
6. SQL is executed on SQLite.
7. Results are returned as a table and converted into a natural language response.
8. Relevant nodes are highlighted in the graph and a focused subgraph is rendered.

A simplified view looks like this:

Raw JSONL data
→ Schema discovery
→ SQLite tables
→ Directed graph model
→ Gemini powered SQL generation
→ SQL execution
→ Answer and highlighted graph

## Data model

The dataset contains multiple business domains that together form a realistic ERP workflow.

### Core transactional entities

1. Sales orders
2. Delivery records
3. Billing documents
4. Accounting and receivable entries

### Supporting master data

1. Customers
2. Business partners
3. Addresses
4. Products
5. Plants
6. Sales area assignments
7. Company assignments

## Key tables used in the project

The project loads the most important fields into normalized SQLite tables.

### sales_orders

Contains sales order headers.

Typical fields:

1. salesOrder
2. customer
3. creationDate

### sales_order_items

Contains item level order data.

Typical fields:

1. salesOrder
2. item
3. material

### deliveries

Contains outbound delivery headers.

Typical fields:

1. deliveryDocument
2. deliveryDate

### delivery_items

Contains delivery item records and the order reference.

Typical fields:

1. deliveryDocument
2. salesOrder
3. item

### billing

Contains billing document headers.

Typical fields:

1. billingDocument
2. accountingDocument
3. soldToParty
4. totalNetAmount
5. billingDocumentDate

### billing_items

Contains billing line items.

Typical fields:

1. billingDocument
2. material
3. netAmount
4. referenceSdDocument

### payments

Contains receivable posting information.

Typical fields:

1. accountingDocument
2. referenceDocument
3. customer
4. amount

### customers

Contains customer master data.

Typical fields:

1. customer
2. name

## Graph model

The graph is a directed business flow graph. Each node represents an entity instance, and each edge represents a meaningful business relationship.

### Main flow

Customer → Sales Order → Delivery → Billing → Payment

### Supporting connections

1. Sales Order Item → Product
2. Billing Item → Product
3. Customer → Address
4. Customer → Company Assignment
5. Customer → Sales Area Assignment

This makes the graph useful for both tracing one business transaction and understanding broader relationships across customers and products.

## Why a graph was the right choice

A graph is a natural way to represent ERP data because business objects are linked by reference keys rather than by isolated meaning.

A relational table tells you what happened in one record. A graph helps you see how that record connects to the rest of the flow.

This is especially useful for questions such as:

1. Which products are associated with the highest number of billing documents?
2. Trace the full flow of a billing document.
3. Find incomplete flows such as billed but not paid or delivered but not billed.
4. Show what entities are connected to a given customer or order.

## LLM integration

Gemini is used as a query translator, not as a free form answer generator.

The LLM receives:

1. The user query.
2. The allowed schema.
3. A prompt that asks it to return raw SQL only.
4. Rules that reject unrelated questions.

The system then cleans the model output, executes the SQL, and returns the result.

This design keeps the answer grounded in the dataset and reduces hallucinations.

## Guardrails

Guardrails are a critical part of the project.

The application rejects irrelevant prompts such as general knowledge questions or creative writing requests. This is intentional because the system is only meant to answer dataset specific questions.

The guardrail logic works at two layers.

1. A lightweight intent check blocks obviously irrelevant questions before they reach the model.
2. The model itself is instructed to return REJECT for unsupported requests.

This prevents the assistant from pretending it knows things outside the dataset.

## Query highlighting

One of the most useful interactions in the project is query driven highlighting.

When the user asks a question and the SQL result returns identifiers, the app extracts those values and maps them back to graph nodes. The graph then highlights the matching nodes and their immediate neighbors.

This turns the app into more than a table interface. It becomes a visual analysis tool.

A focused subgraph is also shown so the user can inspect only the relevant path instead of the full graph.

## Example queries supported

1. Top products by billing.
2. Trace a given billing document.
3. Identify incomplete flows.
4. Find billing documents without payments.
5. List customers linked to billing activity.
6. Show the graph neighborhood of a specific document.

## Validation approach

The project was validated in two ways.

### 1. Raw data verification

Aggregations from SQLite were compared against direct computation from the raw JSONL records to make sure ingestion and transformation were correct.

### 2. Relationship verification

Known sample records were used to confirm that the relationships between sales orders, delivery items, billing items, and payments were reconstructed correctly.

This helped ensure that the graph and the SQL results aligned with the source data.

## Design decisions and tradeoffs

### SQLite instead of a heavier database

SQLite was chosen because it is lightweight, easy to recreate, and good enough for a focused demo. The entire database can be rebuilt locally from the JSONL files.

### NetworkX and Pyvis instead of Neo4j

A full graph database would have added setup time without providing much benefit for this assignment. NetworkX and Pyvis gave enough flexibility to model and render the graph quickly.

### Gemini for SQL generation

Gemini was used because it is easy to integrate, available in free tiers, and performs well on structured query generation when prompted carefully.

### Focus on a few strong features

Instead of building many shallow features, the project focuses on a few strong ones:

1. Reliable SQL generation.
2. Strong graph modeling.
3. Query driven highlighting.
4. Guardrails.
5. A readable and inspectable interface.

## Project structure

```text
fde-project/
├── app.py
├── graph.py
├── load_data.py
├── llm.py
├── guardrails.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── data/
```

## Setup

### 1. Create the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the Gemini API key

Create a `.env` file from the example and set your key.

```bash
export GEMINI_API_KEY=your_api_key_here
```

### 4. Load the data

```bash
python load_data.py
```

### 5. Run the app

```bash
streamlit run app.py
```

## Environment variables

The project expects the Gemini API key to be provided through an environment variable.

### Required

```text
GEMINI_API_KEY
```

### Example

```text
GEMINI_API_KEY=your_api_key_here
```

## Requirements

The project uses the following main libraries:

1. streamlit
2. pandas
3. networkx
4. pyvis
5. google generative ai
6. python dotenv

## Final note

This project is intentionally built to feel practical. It mirrors a real enterprise setting where data is messy, relationships matter, and answers need to be explainable. The goal was not to build something flashy. The goal was to build something that is useful, understandable, and credible.
