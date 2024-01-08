import streamlit as st
import pandas as pd
from ai import run_grammar_chain, run_rewrite_chain, run_chart_chain
from delta_dental import delta, chart, cpa_chart, vcr_chart, describe_chart

# Sidebar
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Display the data
    st.write("Original Data:")
    st.write(data)

    client_name = st.text_input("Client Name:", "Delta Dental")
    industry_type = st.text_input("Industry Type:", "dental insurance plans")

    start_date = '2023-12-01'
    end_date = '2023-12-31'
    
    # Data manipulations
    create_report = st.checkbox("Create report?")


    if create_report:

        best_performing, ctr_average, vcr_average, cpa_average, total_impressions = delta(data, start_date, end_date)
        
        df = pd.DataFrame(best_performing)
        
        remove_rows = st.checkbox("Remove rows?")
        
        if remove_rows:
            rows_to_remove = st.multiselect(
                "Select rows to remove:", df["Description"].unique())
            df = df[~df["Description"].isin(rows_to_remove)]

        st.write("KPI Analysis:")
        st.write(df)

        ai_report = st.checkbox("Create AI report?")

        if ai_report:

            best_vals = []
            cpa_counter = 0
            ctr_counter = 0
            vcr_counter = 0

            for index, row in df.iterrows():
                
                kpi = row["KPI"]
                variable = row["Variable"]
                description = row["Description"]
                kpi_value = row["KPI_Value"]
                format = row["Format"]

                if kpi == "CTR":

                    if ctr_counter == 0:
                        truth = f"For the {format} format, the best value in the {variable} is {description} with a {kpi} of {kpi_value}"
                    else:
                        truth = f"For the {format} format, the next best value in the {variable} is {description} with a {kpi} of {kpi_value}"

                    best_vals.append(truth)
                    ctr_counter+=1
                
                elif kpi == "CPA":
                    
                    if cpa_counter == 0:
                        truth = f"For the {format} format, the best value in the {variable} is {description} with a {kpi} of {kpi_value}"
                    else:
                        truth = f"For the {format} format, the next best value in the {variable} is {description} with a {kpi} of {kpi_value}"
                    
                    best_vals.append(truth)
                    cpa_counter+=1
                
                elif kpi == "VCR":
                    
                    if vcr_counter == 0:
                        truth = f"For the {format} format, the best value in the {variable} is {description} with a {kpi} of {kpi_value}"
                    else:
                        truth = f"For the {format} format, the next best value in the {variable} is {description} with a {kpi} of {kpi_value}"
                    
                    best_vals.append(truth)
                    vcr_counter+=1

            report = " ".join(best_vals)
            
            def run_report():
                # Call the long-running function with a spinner

                new_report = run_grammar_chain(
                    report, client_name, industry_type)
                
                rewrite_report = run_rewrite_chain(new_report)


                return rewrite_report

            with st.spinner(text='In progress...'):
                                
                months = chart(data)
                
                # Display the result
                st.write("A.I Report:")
                st.write(f"From {start_date} to {end_date}, MiQ has delievered a total of {total_impressions} impressions with a CTR of {ctr_average}, a CPA of {cpa_average}, and a VCR of {vcr_average} for the {client_name} campaign.")
                
                vcr_chart(months)
                vcr_lines = describe_chart(months, chart="OLV")
                vcr_desc = run_chart_chain(vcr_lines)
                st.write(vcr_desc)
                
                cpa_chart(months)
                cpa_lines = describe_chart(months, chart="Display")
                cpa_desc = run_chart_chain(cpa_lines)
                st.write(cpa_desc)
                
                st. write("Insights: ")
                new_report = run_report()
                st.write(new_report)


