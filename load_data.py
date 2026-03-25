import os
import json
import sqlite3

BASE_PATH = "/Users/devanshmehra/IdeaProjects/fde-project/sap-o2c-data"  # your dataset root
conn = sqlite3.connect("data.db")
dataFilesFormat = ".jsonl"


def insert_billing():
    rows = []
    for root, _, files in os.walk(BASE_PATH):
        if "billing_document_headers" in root:
            for file in files:
                if file.endswith(dataFilesFormat):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)
                            rows.append((
                                d["billingDocument"],
                                d["accountingDocument"],
                                d["soldToParty"],
                                float(d["totalNetAmount"]),
                                d["billingDocumentDate"]
                            ))
    conn.execute("DROP TABLE IF EXISTS billing")
    conn.execute("""
                 CREATE TABLE billing
                 (
                     billingDocument     TEXT PRIMARY KEY,
                     accountingDocument  TEXT,
                     soldToParty         TEXT,
                     totalNetAmount      REAL,
                     billingDocumentDate TEXT
                 )
                 """)
    conn.executemany("INSERT INTO billing VALUES (?,?,?,?,?)", rows)


def insert_sales_order_items():
    rows = []

    for root, _, files in os.walk(BASE_PATH):
        if "sales_order_items" in root:
            for file in files:
                if file.endswith(".jsonl"):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)

                            rows.append((
                                d["salesOrder"],
                                d["salesOrderItem"],
                                d["material"]
                            ))

    conn.execute("DROP TABLE IF EXISTS sales_order_items")
    conn.execute("""
                 CREATE TABLE sales_order_items
                 (
                     salesOrder TEXT,
                     item       TEXT,
                     material   TEXT
                 )
                 """)
    conn.executemany("INSERT INTO sales_order_items VALUES (?,?,?)", rows)


def insert_delivery_items():
    rows = []

    for root, _, files in os.walk(BASE_PATH):
        if "outbound_delivery_items" in root:
            for file in files:
                if file.endswith(".jsonl"):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)

                            rows.append((
                                d["deliveryDocument"],
                                d["referenceSdDocument"],  # → SALES ORDER
                                d["deliveryDocumentItem"]
                            ))

    conn.execute("DROP TABLE IF EXISTS delivery_items")
    conn.execute("""
                 CREATE TABLE delivery_items
                 (
                     deliveryDocument TEXT,
                     salesOrder       TEXT,
                     item             TEXT
                 )
                 """)
    conn.executemany("INSERT INTO delivery_items VALUES (?,?,?)", rows)


def insert_deliveries():
    rows = []

    for root, _, files in os.walk(BASE_PATH):
        if "outbound_delivery_headers" in root:
            for file in files:
                if file.endswith(".jsonl"):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)

                            rows.append((
                                d["deliveryDocument"],
                                d.get("actualGoodsMovementDate")
                            ))

    conn.execute("DROP TABLE IF EXISTS deliveries")
    conn.execute("""
                 CREATE TABLE deliveries
                 (
                     deliveryDocument TEXT PRIMARY KEY,
                     deliveryDate     TEXT
                 )
                 """)
    conn.executemany("INSERT INTO deliveries VALUES (?,?)", rows)


def insert_items():
    rows = []
    for root, _, files in os.walk(BASE_PATH):
        if "billing_document_items" in root:
            for file in files:
                if file.endswith(".jsonl"):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)
                            rows.append((
                                d["billingDocument"],
                                d["material"],
                                float(d["netAmount"]),
                                d["referenceSdDocument"]
                            ))
    conn.execute("DROP TABLE IF EXISTS billing_items")
    conn.execute("""
                 CREATE TABLE billing_items
                 (
                     billingDocument     TEXT,
                     material            TEXT,
                     netAmount           REAL,
                     referenceSdDocument TEXT
                 )
                 """)
    conn.executemany("INSERT INTO billing_items VALUES (?,?,?,?)", rows)


def insert_sales_orders():
    rows = []

    for root, _, files in os.walk(BASE_PATH):
        if "sales_order_headers" in root:
            for file in files:
                if file.endswith(".jsonl"):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)

                            rows.append((
                                d["salesOrder"],
                                d["soldToParty"],
                                d.get("creationDate")
                            ))

    conn.execute("DROP TABLE IF EXISTS sales_orders")
    conn.execute("""
                 CREATE TABLE sales_orders
                 (
                     salesOrder   TEXT PRIMARY KEY,
                     customer     TEXT,
                     creationDate TEXT
                 )
                 """)
    conn.executemany("INSERT INTO sales_orders VALUES (?,?,?)", rows)


def insert_customers():
    rows = []
    for root, _, files in os.walk(BASE_PATH):
        if "business_partners" in root:
            for file in files:
                if file.endswith(".jsonl"):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)
                            rows.append((
                                d["customer"],
                                d["businessPartnerFullName"]
                            ))
    conn.execute("DROP TABLE IF EXISTS customers")
    conn.execute("""
                 CREATE TABLE customers
                 (
                     customer TEXT PRIMARY KEY,
                     name     TEXT
                 )
                 """)
    conn.executemany("INSERT INTO customers VALUES (?,?)", rows)


def insert_payments():
    rows = []
    for root, _, files in os.walk(BASE_PATH):
        if "journal_entry_items_accounts_receivable" in root:
            for file in files:
                if file.endswith(".jsonl"):
                    with open(os.path.join(root, file)) as f:
                        for line in f:
                            d = json.loads(line)
                            rows.append((
                                d["accountingDocument"],
                                d["referenceDocument"],
                                d["customer"],
                                float(d["amountInTransactionCurrency"])
                            ))
    conn.execute("DROP TABLE IF EXISTS payments")
    conn.execute("""
                 CREATE TABLE payments
                 (
                     accountingDocument TEXT,
                     referenceDocument  TEXT,
                     customer           TEXT,
                     amount             REAL
                 )
                 """)
    conn.executemany("INSERT INTO payments VALUES (?,?,?,?)", rows)


if __name__ == "__main__":
    insert_billing()
    insert_items()
    insert_customers()
    insert_payments()
    insert_sales_orders()
    insert_sales_order_items()
    insert_deliveries()
    insert_delivery_items()
    conn.commit()
    conn.close()
    print("✅ DB Created")
