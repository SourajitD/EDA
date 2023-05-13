#Core package
import streamlit as st
import codecs

#EDA packages
import pandas as pd
import sweetviz as sv
from ydata_profiling import ProfileReport

#Component package
from streamlit_pandas_profiling import st_profile_report
import streamlit.components.v1 as components

#Math package
import math

# function to display SweetViz report on page
def st_display_sweetviz(report_html, height=720, width=1080):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page, height=height, width=width, scrolling=True)

#EDA package selection menu
def main():
    menu = ['Home','Explore Dataset','Split dataset & Compare Test-Train split']
    choice = st.sidebar.selectbox("Menu",menu)
    
    # Home
    if choice == 'Home':
        st.header('''
                  **Automated Exploratory Data Analysis**
                  
                  __EDA web app has been created in Python by [Sourajit Dutta](https://www.linkedin.com/in/sourajitdutta/).__
                  
                  *Libraries used: Streamlit, Pandas, YData-Profiling and SweetViz*

                    ''')
        
        st.subheader(
                    "Exploratory Data Analysis"
                    )
        
        st.markdown('''
                   **Exploratory data analysis (EDA) is a crucial step in the data analysis process that involves the visualization, summarization, and interpretation of data to gain insights into patterns, relationships, and anomalies in the data. EDA methods help analysts identify potential issues with the data, formulate hypotheses, and make informed decisions about subsequent analysis steps.**


                   Some of the key methods used in EDA include:

                       - Data visualization techniques such as histograms, scatter plots, box plots, and heat maps

                       - Descriptive statistics such as mean, median, standard deviation, and correlation coefficients

                       - Data transformation techniques such as normalization, scaling, and standardization

                       - Data cleaning techniques such as handling missing data, outlier detection, and data imputation


                   Some common use cases for EDA include:

                       - Exploring the distribution of variables in the data to identify trends and patterns

                       - Identifying relationships between variables to understand how they are related to each other

                       - Detecting anomalies or outliers in the data that may need further investigation

                       - Checking assumptions about the data and testing hypotheses

                       - Identifying potential issues with the data such as missing values, incorrect values, or data inconsistencies


                    Overall, EDA is a critical step in the data analysis process that helps analysts gain insights into their data, identify potential issues, and make informed decisions about subsequent analysis steps.
                    ''')

    # Y-Data Profiling report
    elif choice == 'Explore Dataset':
        st.subheader("Automated dataset analysis with YData-Profiling")
        uploaded_file = st.file_uploader('Upload CSV file', type=["csv"])
        if uploaded_file is not None:
            @st.cache_data
            def load_csv():
                csv = pd.read_csv(uploaded_file)
                return csv
            df = load_csv()
            pr = ProfileReport(df, explorative=True)
            st.subheader('Input Dataset')
            st.write(df)
            st.subheader('YData-Profiling Report')
            st_profile_report(pr)
        else:
            st.info('Awaiting CSV file upload.')
            if st.button('Press to use Sample Dataset'):
                # sample dataset
                @st.cache_data
                def load_data():
                    sample_csv = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/auto-mpg.csv')
                    return sample_csv
                df = load_data()
                pr = ProfileReport(df, explorative=True)
                st.subheader('Sample Dataset')
                st.write(df)
                st.subheader('YData-Profiling Report')
                st_profile_report(pr)

    # Sweetviz report
    elif choice == 'Split dataset & Compare Test-Train split':
        st.subheader("Automated Test-Train split comparison with SweetViz")
        select_test_size = st.slider('Select Test Data percentage:', 0.0, 100.0, 0.1)
        uploaded_file = st.file_uploader('Upload CSV file', type=["csv"])
        if uploaded_file is not None:
            @st.cache_data
            def load_csv():
                csv = pd.read_csv(uploaded_file)
                return csv
            df = load_csv()
            test_size = math.ceil(((select_test_size/100.0) * df.shape[0]))
            train = df[0:test_size]
            test = df[test_size:]
            pr = sv.compare([train,'Training Data'],[test,'Testing Data'])
            st.subheader('Input Dataset')
            st.write(df)
            st.subheader('SweetViz Comparison Report')
            pr.show_html()
            st_display_sweetviz("SWEETVIZ_REPORT.html")
        else:
            st.info('Awaiting CSV file upload.')
            if st.button('Press to use Sample Dataset'):
                # sample dataset
                @st.cache_data
                def load_data():
                    sample_csv = pd.read_csv('https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv')
                    return sample_csv
                df = load_data()
                test_size = math.ceil(((select_test_size/100.0) * df.shape[0]))
                train = df[0:test_size]
                test = df[test_size:]
                pr = sv.compare([train,'Training Data'],[test,'Testing Data'])
                st.subheader('Sample Dataset')
                st.write(df)
                st.subheader('SweetViz Comparison Report')
                pr.show_html()
                st_display_sweetviz("SWEETVIZ_REPORT.html")
main()