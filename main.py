import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Tracer Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

with open("./style/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data
df = pd.read_excel("./data/DataDummyStreamlit.xlsx")

# st.dataframe(df)

fakultas_prodi = df[['Fakultas', 'Prodi']].drop_duplicates()
# st.table(fakultas_prodi)

# Dynamic Filters
dynamic_filters = DynamicFilters(
    df,
    filters=['Tahun Survey', 'Fakultas', 'Prodi']
)
with st.sidebar:
    st.title("Filter Data")
dynamic_filters.display_filters(location='sidebar')
filtered_df = dynamic_filters.filter_df().copy()


# # Sidebar
# if 'prodi' not in st.session_state:
#     st.session_state.prodi = None

# if 'fakultas' not in st.session_state:
#     st.session_state.fakultas = None


# with st.sidebar:
#     st.title("Filter Data")
#     tahun = st.slider(
#         label="Tahun Survey",
#         min_value=2010,
#         max_value=2020,
#         value=(2010, 2020))

#     prodi = st.selectbox(
#         label="Program Studi",
#         index=None,
#         placeholder="Pilih Program Studi",
#         options=fakultas_prodi['Prodi'].unique())

#     fakultas = st.selectbox(
#         label="Fakultas",
#         index=None,
#         placeholder="Pilih Fakultas",
#         options=fakultas_prodi['Fakultas'].unique())

# # Filter
# if prodi == None:
#     df2 = df.copy()
# else:
#     df2 = df[(df['Prodi'] == prodi)]

# if fakultas == None:
#     df3 = df2.copy()
# else:
#     df3 = df2[(df2['Fakultas'] == fakultas)]

# if prodi == None and fakultas == None:
#     filtered_df = df[(df["Tahun Survey"] >= tahun[0]) & (df["Tahun Survey"] <= tahun[1])]
# elif prodi == None and fakultas != None:
#     filtered_df = df3[(df3["Tahun Survey"] >= tahun[0]) & (df3["Tahun Survey"] <= tahun[1])]
# elif prodi != None and fakultas == None:
#     filtered_df = df2[(df2["Tahun Survey"] >= tahun[0]) & (df2["Tahun Survey"] <= tahun[1])]
# else:
#     filtered_df = df3[(df3["Tahun Survey"] >= tahun[0]) & (df3["Tahun Survey"] <= tahun[1])]

# bar chart
with st.container(border=True):
    st.title("IPK Mahasiswa")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        # Create category for IPK
        category = ["2,00-2,50", "2,51-3,00", "3,01-3,50", "3,51-4,00"]
        filtered_df['Kategori IPK'] = pd.cut(x=filtered_df['IP'], bins=[
                                             2, 2.5, 3, 3.5, 4], labels=category)
        filtered_df['Kategori IPK'] = filtered_df['Kategori IPK'].astype('str')

        # Create bar chart using histogram to aggregate color (not stacked bar chart in plotly behaviour)
        fig_bar = px.histogram(
            filtered_df,
            y='Kategori IPK',
            color='Kategori IPK',
            text_auto=True
        )
        fig_bar.update_layout(
            xaxis_title="Jumlah Mahasiswa",
            yaxis_title="Kategori IPK",
            legend_title="Kategori IPK",
            yaxis={'categoryorder': 'category ascending'}
        )
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Create box plot
        fig_box = px.box(
            filtered_df,
            y='IP',
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col3:
        ip_stat = filtered_df["IP"].describe(
        ).loc[["count", "mean", "std", "max", "min"]]
        ip_stat["median"] = filtered_df["IP"].median()
        st.dataframe(ip_stat)

# IPK Mahasiswa Per Prodi
with st.container(border=True):
    st.title("Rata-Rata IPK Mahasiswa Per Prodi")
    fig_bar2 = px.histogram(
        filtered_df,
        x='IP',
        y='Prodi',
        text_auto=True,
        histfunc='avg',
        height=1500,
        # color='Prodi'
    )
    fig_bar2.update_layout(
        xaxis_title="Rata-Rata IP Alumni",
        yaxis_title="Program Studi",
        yaxis=dict(
            tickmode='array',
            tickvals=np.arange(len(filtered_df['Prodi'].value_counts())),
            ticktext=[
                f"{i} ({j}/{k})" for i, j, k in zip(
                    filtered_df['Prodi'].value_counts().index,
                    filtered_df['Prodi'].value_counts().values,
                    df['Prodi'].value_counts().values
                )
            ],
        ),
        # showlegend=False
    )
    fig_bar2.update_yaxes(categoryorder='total ascending')
    fig_bar2.update_traces(textposition='outside')
    st.plotly_chart(fig_bar2, use_container_width=True)
