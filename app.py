import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


st.sidebar.title("Exploratory Data Analysis")

data_file = st.sidebar.file_uploader("Please upload a csv dataset")

if data_file is not None:
    st.title("Data Preview")

    data = pd.read_csv(data_file)
    st.write(data.head(5))


    def get_column_types(df):
        numeric_columns = 0
        bool_columns = 0
        string_columns = 0

        for column in df.columns:
            column_type = df[column].dtype

            if column_type == 'int64' or column_type == 'float64':
                numeric_columns += 1
            elif column_type == 'bool':
                bool_columns += 1
            elif column_type == 'object':
                string_columns += 1

        return numeric_columns, bool_columns, string_columns
    
    column_count = get_column_types(data)

    st.write(f"The data has {data.shape[0]} row(s) and {data.shape[1]} column(s).")
    st.write(f"Among all columns, it has {column_count[0]} numeric column(s),\
              {column_count[1]} bool_column(s) and {column_count[2]} categorical column(s)")
    
    column = st.sidebar.selectbox("Please select a column", data.columns)

    if column is not None:
        if data[column].dtype == 'int64' or data[column].dtype == 'float64':
            st.title(column)

            st.subheader('Summary Table')
            summary_table = data[column].describe()
            st.write(summary_table)

            st.subheader('Histogram Generation')

            histcol1, histcol2 = st.columns(2)

            with histcol1:
                choose_color = st.color_picker('Choose a Color for column', "#d60d0d")
                choose_opacity = st.slider('Opacity', min_value=0.0, max_value=1.0, value = 1.0, step=0.01)
                hist_title = st.text_input('Set Title', 'Histogram')
            with histcol2:
                choose_edge_color = st.color_picker('Choose a Color for edge of column', "#000000")
                hist_bins = st.slider('Number of bins', min_value=5, max_value=50, value=10)
                hist_xtitle = st.text_input('Set x-axis Title', column)

            fig, ax = plt.subplots()
            ax.hist(data[column], bins=hist_bins,color=choose_color, alpha=choose_opacity, edgecolor = choose_edge_color)
            ax.set_title(hist_title)
            ax.set_xlabel(hist_xtitle)
            ax.set_ylabel('Count')

            st.pyplot(fig)

            filename = 'plot.png'
            fig.savefig(filename,dpi = 300)
            with open("plot.png", "rb") as file:
                btn = st.download_button(
                label="Download image",
                data=file,
                file_name="plot.png",
                mime="image/png"
            )

        if data[column].dtype == 'bool' or data[column].dtype == 'object':
            st.title(column)

            st.subheader('Proportion Table')
            proportions = data[column].value_counts(normalize = True)
            proportions_table = pd.DataFrame({'Category': proportions.index, 'Proportion': proportions.values})
            st.write(proportions_table)

            st.subheader('Histogram Generation')
            choose_color = st.color_picker('Choose a Color for column', "#d60d0d")
            bar_title = st.text_input('Set Title', 'Proportions of Category Levels')

            fig, ax = plt.subplots()
            ax.bar(proportions.index, proportions.values, color=choose_color)
            ax.set_xlabel('Category')
            ax.set_ylabel('Proportion')
            ax.set_title(bar_title)
            
            st.pyplot(fig)

            filename = 'plot.png'
            fig.savefig(filename,dpi = 300)
            with open("plot.png", "rb") as file:
                btn = st.download_button(
                label="Download image",
                data=file,
                file_name="plot.png",
                mime="image/png"
            )






