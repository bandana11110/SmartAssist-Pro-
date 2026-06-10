import streamlit as st
import pandas as pd

def dataset_summary(df):

    st.subheader("📊 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("📋 Data Types")
    st.dataframe(
        pd.DataFrame(df.dtypes, columns=["Datatype"])
    )

    st.subheader("📈 Statistical Summary")
    st.dataframe(df.describe())