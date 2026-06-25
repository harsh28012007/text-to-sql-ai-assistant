import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Amazon Data Text to SQL Application")

user_input = st.text_input("Enter your question")

run = st.button("Run Query")

if run:

    if user_input.strip() == "":
        st.warning("Please enter a question")

    else:
        response = requests.post(
            "http://127.0.0.1:8000/query",
            json={"question": user_input}
        )

        result = response.json()

        if "error" in result:
            st.error(result["error"])

        else:
            st.subheader("Generated SQL")
            st.code(result["sql"])

            # ✅ df is defined here
            df = pd.DataFrame(result["data"])

            st.subheader("Result")
            st.dataframe(df)

            # --------------------------
            # BAR CHART
            # --------------------------
            if not df.empty and len(df.columns) >= 2:

                numeric_cols = df.select_dtypes(include="number").columns

                if len(numeric_cols) > 0:
                    st.subheader("Bar Chart")

                    chart_df = df.set_index(df.columns[0])
                    st.bar_chart(chart_df)

            # --------------------------
            # PIE CHART (FIXED)
            # --------------------------
            if not df.empty and len(df.columns) == 2:
                try:
                    st.subheader("Pie Chart (Top 5 Categories)")

                    if len(df) > 5:
                        st.info("Showing top 5 categories for better clarity")

                    df_sorted = df.sort_values(
                        by=df.columns[1],
                        ascending=False
                    ).head(5)

                    # Short labels
                    labels = df_sorted.iloc[:, 0].apply(lambda x: str(x).split("|")[0])
                    values = df_sorted.iloc[:, 1]

                    fig, ax = plt.subplots(figsize=(6, 6))

                    wedges, texts, autotexts = ax.pie(
                        values,
                        autopct='%1.1f%%',
                        startangle=90
                    )

                    ax.axis('equal')

                    ax.legend(
                        wedges,
                        labels,
                        title="Categories",
                        loc="center left",
                        bbox_to_anchor=(1, 0.5)
                    )

                    st.pyplot(fig)

                except:
                    st.warning("Pie chart not suitable for this data")