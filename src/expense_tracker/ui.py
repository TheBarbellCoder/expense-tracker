import pandas as pd
import streamlit as st
# from expense_tracker.transactions import Database


st.set_page_config(page_title="Personal Expense Tracker", layout="centered")

st.title("Expense Tracker")
st.text("Welcome to your personal expense tracker!")
st.space(size="medium")

dkb_giro, _ = st.tabs(["Deutsche Kredit Bank", " + "])

with dkb_giro:
    uploaded_file = st.file_uploader("Upload a .csv file of transactions", type="csv")
    st.space()

    # Setup a database
    # duck = Database()

    if uploaded_file:
        # Extract metadata
        uploaded_file.seek(0)
        meta_lines = [
            uploaded_file.readline().decode("utf-8").strip() for _ in range(4)
        ]

        meta_df = pd.DataFrame(
            [line.split(";") for line in meta_lines], columns=["key", "value"]
        )

        # Extract transactions into another table
        df = pd.read_csv(uploaded_file, sep=";", decimal=",", thousands=".")
        df = df.iloc[:, [0, 4, 6, 7, 8, 11]]

        report_df = pd.DataFrame(
            {
                "Total Credit": [df[df["Umsatztyp"] == "Eingang"].iloc[:, 4].sum()],
                "Total Debit": [
                    -1 * (df[df["Umsatztyp"] == "Ausgang"].iloc[:, 4].sum())
                ],
            }
        )

        st.html(
            f"<b>{meta_df.iloc[0, 0].replace('"', '')}:</b> &nbsp {meta_df.iloc[0, 1].replace('"', '')}"
        )
        st.html(
            f"<b>{meta_df.iloc[1, 0].replace('"', '')}</b> &nbsp {meta_df.iloc[1, 1].replace('"', '')}"
        )

        st.write(df)

        st.space(size="medium")

        st.markdown("#### Report")
        st.write(report_df)

        tc: float = report_df.loc[0, "Total Credit"]
        td: float = report_df.loc[0, "Total Debit"]

        if td > tc:
            st.markdown(f":red[**Overspent {(td - tc):.2f} EUR**]")
        elif tc > td:
            st.markdown(f":green[**Saved {(tc - td):.2f} EUR**]")
        else:
            st.markdown("Right on the spot!")
