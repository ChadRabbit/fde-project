import streamlit as st
import os
from db import run_sql
from llm import generate_sql, generate_answer
from guardrails import is_valid_query
from graph import save_graph, save_filtered_graph


if not os.path.exists("data.db"):
    import load_data
    load_data.main()
st.title("📊 Graph + AI Query System")

# Graph
st.subheader("🌐 Full Graph")
save_graph()
st.components.v1.html(open("graph.html").read(), height=600)

st.markdown("""
### Legend:
- 🔴 Customer  
- 🟣 Order  
- 🟠 Delivery  
- 🔵 Billing  
- 🟢 Product  
- ⚫ Payment  
""")
# Chat
query = st.text_input("Ask a question")
highlight_nodes = set()


def extract_nodes_from_df(df):
    nodes = set()

    for col in df.columns:
        for val in df[col].dropna().astype(str):

            # Detect type based on column name
            col_lower = col.lower()

            if "billing" in col_lower:
                nodes.add(f"bill_{val}")

            elif "accounting" in col_lower:
                nodes.add(f"pay_{val}")

            elif "customer" in col_lower or "party" in col_lower:
                nodes.add(f"cust_{val}")

            elif "material" in col_lower:
                nodes.add(f"prod_{val}")

            elif "order" in col_lower or "reference" in col_lower:
                nodes.add(f"order_{val}")

            elif "delivery" in col_lower:
                nodes.add(f"del_{val}")

    return nodes


highlight_nodes = set()

if query:
    if not is_valid_query(query):
        st.warning("⚠️ This system only answers dataset-related queries.")
    else:
        sql = generate_sql(query)
        if "REJECT" in sql:
            st.warning("⚠️ The query is not relevant to the dataset.")

        else:
            st.code(sql)

            result = run_sql(sql)
            st.write(result)

            if not isinstance(result, str) and not result.empty:
                highlight_nodes = extract_nodes_from_df(result)

# st.components.v1.html(open("graph.html").read(), height=600)

if highlight_nodes:
    save_filtered_graph(highlight_nodes)

    st.subheader("🎯 Focus Graph (Query Result)")
    st.components.v1.html(open("filtered_graph.html").read(), height=500)
