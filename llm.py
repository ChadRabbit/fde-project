from google import genai
import re
import os
from dotenv import load_dotenv

load_dotenv()

print("Getting api key from environment variable 'GOOGLE_API_KEY'...")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Done.")

SYSTEM_PROMPT = """
You are a SQL generator for a business ERP dataset.

Tables:
billing(billingDocument, accountingDocument, soldToParty, totalNetAmount, billingDocumentDate)
billing_items(billingDocument, material, netAmount, referenceSdDocument)
customers(customer, name)
payments(accountingDocument, referenceDocument, customer, amount)
sales_orders(salesOrder, customer, creationDate)
sales_order_items(salesOrder, item, material)
deliveries(deliveryDocument, deliveryDate)
delivery_items(deliveryDocument, salesOrder, item)

Rules:
- Only output SQL
- No explanation
- Use joins properly
- If unrelated return REJECT
"""


def clean_sql(text):
    text = re.sub(r"```sql|```", "", text, flags=re.IGNORECASE)
    return text.strip()


def generate_sql(user_query):
    prompt = SYSTEM_PROMPT + "\nUser Query: " + user_query
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    sql = clean_sql(response.text)
    return sql


def generate_answer(user_query, df):
    prompt = f"""
    User question: {user_query}
    SQL result:
    {df.to_string()}

    Give a short clear answer.
    """
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    return response.text
