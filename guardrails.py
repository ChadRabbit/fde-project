def is_valid_query(query):
    keywords = [
        "order", "delivery", "billing",
        "payment", "customer", "product",
        "sales", "invoice"
    ]
    return any(k in query.lower() for k in keywords)
