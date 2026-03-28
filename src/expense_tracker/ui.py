import duckdb
from expense_tracker.transactions import Database
import pandas as pd
import streamlit as st
import time


# Setup a database
duck = Database()

# Setup a placeholder to wrap any stremlit component
placeholder = st.empty()


def handle_submit() -> None:
    label: str = st.session_state.category_label
    try:
        duck.add_category(label.strip().title())
        with placeholder.container():
            # TODO (Avinash): Make this interactive with streamlit-notify
            st.success(f"Added category: {label}")
    except duckdb.ConstraintException:
        with placeholder.container():
            # TODO (Avinash): Make this interactive with streamlit-notify
            st.warning(f"Category: {label} already exists")
    finally:
        time.sleep(1.5)
        placeholder.empty()


st.set_page_config(page_title="Personal Expense Tracker", layout="centered")

st.title("Expense Tracker")
st.text("Welcome to your personal expense tracker!")
st.space(size="medium")

bank1, _ = st.tabs(["Bank1", " + "])

with bank1:
    uploaded_file = st.file_uploader("Upload a .csv file of transactions", type="csv")
    st.space()

    if uploaded_file:
        # Extract metadata
        uploaded_file.seek(0)
        meta_lines = [
            uploaded_file.readline().decode("utf-8").strip() for _ in range(4)
        ]

        meta_df = pd.DataFrame(
            [line.split(";") for line in meta_lines], columns=["key", "value"]
        )

        # Extract transactions into another table and clean up
        df = pd.read_csv(
            uploaded_file,
            sep=";",
            parse_dates=[0],
            date_format="%d.%m.%y",
            decimal=",",
            thousands=".",
        )
        df = df.iloc[:, [0, 4, 6, 8]]
        df.rename(
            {
                "Buchungsdatum": "Booking Date",
                "Zahlungsempfänger*in": "Payee",
                "Umsatztyp": "Transaction",
                "Betrag (€)": "Amount",
            },
            axis="columns",
            inplace=True,
        )
        df.replace("Ausgang", "Debit", inplace=True)
        df.replace("Eingang", "Credit", inplace=True)
        df.insert(loc=4, column="Category", value="Uncategorized")

        report_df = pd.DataFrame(
            {
                "Total Credit": [df[df["Transaction"] == "Credit"].iloc[:, 3].sum()],
                "Total Debit": [
                    -1 * (df[df["Transaction"] == "Debit"].iloc[:, 3].sum())
                ],
            }
        )

        metadata, add_category = st.columns([0.4, 0.6], vertical_alignment="bottom")

        # Display metadata
        with metadata:
            with st.container(border=True):
                st.html(
                    f"<b>{meta_df.iloc[0, 0].replace('"', '')}:</b><br> {meta_df.iloc[0, 1].replace('"', '')}"
                )
                st.html(
                    f"<b>{meta_df.iloc[1, 0].replace('"', '')}</b><br> {meta_df.iloc[1, 1].replace('"', '')}"
                )

        with add_category:
            with st.form("add_category", clear_on_submit=True, border=False):
                text, button = st.columns([3, 1])

                with text:
                    st.text_input(
                        "Add a category",
                        placeholder="Add a category",
                        label_visibility="collapsed",
                        key="category_label",
                    )

            with button:
                st.form_submit_button(
                    "Add", on_click=handle_submit, use_container_width=True
                )

        # Display cleaned up transactions DataFrame
        st.space(size="xxsmall")

        categories_df = duck.categories.df()
        st.data_editor(
            df,
            hide_index=True,
            column_config={
                "Booking Date": st.column_config.DateColumn(),
                "Category": st.column_config.SelectboxColumn(
                    help="Assign a category",
                    default="Uncategorized",
                    options=categories_df["label"].tolist(),
                    required=True,
                ),
            },
        )

        # TODO (Avinash): Add a "Save Changes" button here. On click, it should load the data into the database and clear this view.  
        st.space(size="medium")

        st.markdown("#### Report")
        st.write(report_df)

        tc: float = report_df.loc[0, "Total Credit"]
        td: float = report_df.loc[0, "Total Debit"]

        if td > tc:
            st.markdown(f":red[**Overspent {(td - tc):.2f} EUR**]")
        elif tc > td:
            st.markdown(f":green[**Saved {(tc - td):.2f} €**]")
        else:
            st.markdown("Right on the spot!")
