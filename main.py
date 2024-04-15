import streamlit as st
import pandas as pd
import plotly.express as px

st.write("""
# Dashboard Dummy Tracer Study
""")

df = pd.read_excel("./data/DataDummyStreamlit.xlsx")
df['Tahun Survey'] = df['Tahun Survey'].astype('str')
st.dataframe(df)


