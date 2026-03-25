import os
import json
from collections import defaultdict

BASE_PATH = "/Users/devanshmehra/IdeaProjects/fde-project/sap-o2c-data"  # your dataset root

product_totals = defaultdict(float)

for root, _, files in os.walk(BASE_PATH):
    if "billing_document_items" in root:
        for file in files:
            if file.endswith(".jsonl"):
                with open(os.path.join(root, file)) as f:
                    for line in f:
                        d = json.loads(line)

                        material = d["material"]
                        amount = float(d["netAmount"])

                        product_totals[material] += amount

# sort
sorted_products = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)

# print top 10
for mat, total in sorted_products[:10]:
    print(mat, total)
