import pandas as pd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import streamlit as st

def delta(data, start_date, end_date):

    best_performing = {"KPI": [], "Variable": [], "Description": [], "KPI_Value": [], "Format": []}

    data["Date"] = pd.to_datetime(data["Date"])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    values = ["Request a Quote Fires", "Impressions", "Clicks", "Media Cost", "Video Plays", "Video Completions"]

    total_impressions = data.Impressions.sum()
    ctr_average = data.Clicks.sum() / data.Impressions.sum()
    cpa_average = data["Media Cost"].sum() / data["Request a Quote Fires"].sum()
    vcr_average = data["Video Completions"].sum() / data["Video Plays"].sum()
    
    #display transformations
    display = data[data.Format == "Standard Display"]

    
    tactic_display = display.pivot_table(index="Tactic", values=values, aggfunc="sum").reset_index()
    tactic_display["CTR"] = tactic_display["Clicks"] / tactic_display["Impressions"]
    tactic_display["CPA"] = tactic_display["Media Cost"] / tactic_display["Request a Quote Fires"]

    tactic_sorted_by_ctr_display = tactic_display.reset_index().sort_values(by="CTR", ascending=False)
    tactic_sorted_by_cpa_display = tactic_display.reset_index().sort_values(by="CPA")

    tactic_display_best_cpa = (tactic_sorted_by_cpa_display.CPA[0], tactic_sorted_by_cpa_display.Tactic[0])
    tactic_display_best_ctr = (tactic_sorted_by_ctr_display.CTR[0], tactic_sorted_by_ctr_display.Tactic[0])

    if tactic_display_best_cpa[0] <= cpa_average:
        best_performing["KPI"].append("CPA")
        best_performing["Variable"].append("Tactic")
        best_performing["Description"].append(tactic_display_best_cpa[1])
        best_performing["KPI_Value"].append(tactic_display_best_cpa[0])
        best_performing["Format"].append("Display")


    if tactic_display_best_ctr[0] >= ctr_average:
        best_performing["KPI"].append("CTR")
        best_performing["Variable"].append("Tactic")
        best_performing["Description"].append(tactic_display_best_ctr[1])
        best_performing["KPI_Value"].append(tactic_display_best_ctr[0])
        best_performing["Format"].append("Display")


    size_display = display.pivot_table(index="Ad Size", values=values, aggfunc="sum")
    size_display["CTR"] = size_display["Clicks"] / size_display["Impressions"]
    size_display["CPA"] = size_display["Media Cost"] / size_display["Request a Quote Fires"]

    size_sorted_by_ctr_display = size_display.reset_index().sort_values(by="CTR", ascending=False)
    size_sorted_by_cpa_display = size_display.reset_index().sort_values(by="CPA")

    size_display_best_cpa = (size_sorted_by_cpa_display.CPA[0], size_sorted_by_cpa_display["Ad Size"][0])
    size_display_best_ctr = (size_sorted_by_ctr_display.CTR[0], size_sorted_by_ctr_display["Ad Size"][0])

    if size_display_best_cpa[0] <= cpa_average:
        best_performing["KPI"].append("CPA")
        best_performing["Variable"].append("Ad Size")
        best_performing["Description"].append(size_display_best_cpa[1])
        best_performing["KPI_Value"].append(size_display_best_cpa[0])
        best_performing["Format"].append("Display")


    if size_display_best_ctr[0] >= ctr_average:
        best_performing["KPI"].append("CTR")
        best_performing["Variable"].append("Ad Size")
        best_performing["Description"].append(size_display_best_ctr[1])
        best_performing["KPI_Value"].append(size_display_best_ctr[0])
        best_performing["Format"].append("Display")


    creative_display = display.pivot_table(index="Creative Type", values=values, aggfunc="sum")
    creative_display["CTR"] = creative_display["Clicks"] / creative_display["Impressions"]
    creative_display["CPA"] = creative_display["Media Cost"] / creative_display["Request a Quote Fires"]

    creative_sorted_by_ctr_display = creative_display.reset_index().sort_values(by="CTR", ascending=False)
    creative_sorted_by_cpa_display = creative_display.reset_index().sort_values(by="CPA")

    creative_display_best_cpa = (creative_sorted_by_cpa_display.CPA[0], creative_sorted_by_cpa_display["Creative Type"][0])
    creative_display_best_ctr = (creative_sorted_by_ctr_display.CTR[0], creative_sorted_by_ctr_display["Creative Type"][0])

    if creative_display_best_cpa[0] <= cpa_average:
        best_performing["Format"].append("Display")
        best_performing["KPI"].append("CPA")
        best_performing["Variable"].append("Creative Type")
        best_performing["Description"].append(creative_display_best_cpa[1])
        best_performing["KPI_Value"].append(creative_display_best_cpa[0])

    if creative_display_best_ctr[0] >= ctr_average:
        best_performing["KPI"].append("CTR")
        best_performing["Variable"].append("Ad Size")
        best_performing["Description"].append(creative_display_best_ctr[1])
        best_performing["KPI_Value"].append(creative_display_best_ctr[0])
        best_performing["Format"].append("Display")



    # olv transformations
    olv = data[data.Format == "OLV"]

    tactic_olv= olv.pivot_table(index="Tactic", values=values, aggfunc="sum")
    tactic_olv["VCR"] = tactic_olv["Video Completions"] / tactic_olv["Video Plays"]
    tactic_olv["CPA"] = tactic_olv["Media Cost"] / tactic_olv["Request a Quote Fires"]

    tactic_sorted_by_vcr_olv = tactic_olv.reset_index().sort_values(by="VCR", ascending=False)
    tactic_sorted_by_cpa_olv = tactic_olv.reset_index().sort_values(by="CPA")

    tactic_olv_best_vcr = (tactic_sorted_by_vcr_olv.VCR[0], tactic_sorted_by_vcr_olv.Tactic[0])
    tactic_olv_best_cpa = (tactic_sorted_by_cpa_olv.CPA[0], tactic_sorted_by_cpa_olv.Tactic[0])

    if tactic_olv_best_vcr[0] >= vcr_average:
        best_performing["Format"].append("OLV")
        best_performing["KPI"].append("VCR")
        best_performing["Variable"].append("Tactic")
        best_performing["Description"].append(tactic_olv_best_vcr[1])
        best_performing["KPI_Value"].append(tactic_olv_best_vcr[0])

    if tactic_olv_best_cpa[0] <= cpa_average:
        best_performing["KPI"].append("CPA")
        best_performing["Variable"].append("Tactic")
        best_performing["Description"].append(tactic_olv_best_cpa[1])
        best_performing["KPI_Value"].append(tactic_olv_best_cpa[0])
        best_performing["Format"].append("OLV")


    size_olv= olv.pivot_table(index="Ad Size", values=values, aggfunc="sum")
    size_olv["VCR"] = size_olv["Video Completions"] / size_olv["Video Plays"]
    size_olv["CPA"] = size_olv["Media Cost"] / size_olv["Request a Quote Fires"]

    size_sorted_by_vcr_olv = size_olv.reset_index().sort_values(by="VCR", ascending=False)
    size_sorted_by_cpa_olv = size_olv.reset_index().sort_values(by="CPA")

    size_olv_best_vcr = (size_sorted_by_vcr_olv.VCR[0], size_sorted_by_vcr_olv["Ad Size"][0])
    size_olv_best_cpa = (size_sorted_by_cpa_olv.CPA[0], size_sorted_by_cpa_olv["Ad Size"][0])

    if size_olv_best_vcr[0] >= vcr_average:
        best_performing["Format"].append("OLV")
        best_performing["KPI"].append("VCR")
        best_performing["Variable"].append("Ad Size")
        best_performing["Description"].append(size_olv_best_vcr[1])
        best_performing["KPI_Value"].append(size_olv_best_vcr[0])

    if size_olv_best_cpa[0] <= cpa_average:
        best_performing["KPI"].append("CPA")
        best_performing["Variable"].append("Ad Size")
        best_performing["Description"].append(size_olv_best_cpa[1])
        best_performing["KPI_Value"].append(size_olv_best_cpa[0])
        best_performing["Format"].append("OLV")

    creative_olv= olv.pivot_table(index="Creative Type", values=values, aggfunc="sum")
    creative_olv["VCR"] = creative_olv["Video Completions"] / creative_olv["Video Plays"]
    creative_olv["CPA"] = creative_olv["Media Cost"] / creative_olv["Request a Quote Fires"]

    creative_sorted_by_vcr_olv = creative_olv.reset_index().sort_values(by="VCR", ascending=False)
    creative_sorted_by_cpa_olv = creative_olv.reset_index().sort_values(by="CPA")

    creative_olv_best_vcr = (creative_sorted_by_vcr_olv.VCR[0], creative_sorted_by_vcr_olv["Creative Type"][0])
    creative_olv_best_cpa = (creative_sorted_by_cpa_olv.CPA[0], creative_sorted_by_cpa_olv["Creative Type"][0])

    if creative_olv_best_vcr[0] >= vcr_average:
        best_performing["Format"].append("OLV")
        best_performing["KPI"].append("VCR")
        best_performing["Variable"].append("Creative Type")
        best_performing["Description"].append(creative_olv_best_vcr[1])
        best_performing["KPI_Value"].append(creative_olv_best_vcr[0])

    if creative_olv_best_cpa[0] <= cpa_average:
        best_performing["KPI"].append("CPA")
        best_performing["Variable"].append("Creative Type")
        best_performing["Description"].append(creative_olv_best_cpa[1])
        best_performing["KPI_Value"].append(creative_olv_best_cpa[0])
        best_performing["Format"].append("OLV")


    return best_performing, ctr_average, cpa_average, vcr_average, total_impressions


def chart(data):

    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values(by="Date")

    data['Month'] = data['Date'].dt.strftime('%B')
    data["Month_Number"] = data["Date"].dt.month


    months = data.pivot_table(index=["Month", "Month_Number"], values=["Media Cost", "Impressions", "Video Plays", "Video Completions", "Request a Quote Fires"], aggfunc="sum")
    print(months)
    months["VCR"] = months["Video Completions"] / months["Video Plays"]
    months["CPA"] = months["Media Cost"] / months["Request a Quote Fires"]
    
    months = months.reset_index()
    months = months.sort_values(by="Month_Number", ascending=True)

    return months

def describe_chart(months, chart="Display"):

    if chart == "Display":

        line = "You are being describe a line and bar chart combo. The line is CPA (cost per acquistion) over a certain amount of months. The bars are the total spend over a certain amount of months. Here is the description: "
        

        for index, row in months.iterrows():
            
            month = row["Month"]
            cpa = row["CPA"]
            cost = row["Media Cost"]

            line += f"The average cpa for the month of {month} (x-axis) is {cpa} (line) with a total spend of {cost} (bar)."
    
    elif chart == "OLV":
        
        line = "You are being describe a line and bar chart combo. The line is VCR (video completion rate) over a certain amount of months. The bars are the total spend of a certain amount of months. Here is the description: "


        for index, row in months.iterrows():

            month = row["Month"]
            vcr = row["VCR"]
            cost = row["Media Cost"]

            line += f"The average vcr for the month of {month} (x-axis) is {vcr} (line) with a total spend of {cost} (bar)"

    return line





def vcr_chart(months):

    fig, ax1 = plt.subplots(figsize=(20, 8))

    # Create a line plot for CPA on the primary y-axis with purple color
    sns.lineplot(x='Month', y='VCR', data=months, ax=ax1, marker='o', label='VCR', color='purple')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('VCR', color='purple')  # Add dollar sign to the y-axis label
    ax1.tick_params(axis='y', labelcolor='purple')

    # Create a bar plot for Cost on the secondary y-axis
    ax2 = ax1.twinx()
    ax2.bar(months['Month'], months['Media Cost'], alpha=0.5, color='tab:orange', label='Cost')
    ax2.set_ylabel('Cost', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Rotate x-axis labels for both axes
    ax1.set_xticklabels(months['Month'], rotation=45)
    ax2.set_xticklabels(months['Month'], rotation=45)

    # Annotate the line graph with CPA values including a dollar sign
    for index, row in months.iterrows():
        ax1.text(row['Month'], row['VCR'], f'{row["VCR"] * 100:.2f}%', ha='center', va='bottom', fontsize=8, color='purple')

    # Set labels and title
    plt.title('Monthly Cost vs VCR Performance', fontsize=20, pad=20)
    plt.legend(loc='center left')

    fig.patch.set_facecolor('white')


    # # Add the company logo
    # logo_path = "MiQ-logo-Copy1 (3).jpg"  # Replace with the actual path to your logo image
    # logo_img = plt.imread(logo_path)
    # imagebox = OffsetImage(logo_img, zoom=0.1)  # Adjust the zoom factor as needed
    # ab = AnnotationBbox(imagebox, (0.1, 0.9), frameon=False, pad=0.0, xycoords='axes fraction', boxcoords="axes fraction")
    # plt.gca().add_artist(ab)

    # plt.savefig('vcr.png', dpi=300, bbox_inches='tight')



    # Show the plot
    # plt.tight_layout()

    st.pyplot(fig)  # Display the Matplotlib figure in Streamlit

def cpa_chart(months):

    # Assuming you have your data in a DataFrame named grouped_df
    # If not, you can create one like this:
    # grouped_df = pd.DataFrame({'Date': date_list, 'CPA': cpa_list, 'Cost': cost_list})

    # Create a figure and axis
    fig, ax1 = plt.subplots(figsize=(20, 8))

    # Create a line plot for CPA on the primary y-axis with purple color
    sns.lineplot(x='Month', y='CPA', data=months, ax=ax1, marker='o', label='CPA', color='purple')
    ax1.set_xlabel('Months')
    ax1.set_ylabel('CPA ($)', color='purple')  # Add dollar sign to the y-axis label
    ax1.tick_params(axis='y', labelcolor='purple')

    # Create a bar plot for Cost on the secondary y-axis
    ax2 = ax1.twinx()
    ax2.bar(months['Month'], months['Media Cost'], alpha=0.5, color='tab:orange', label='Cost')
    ax2.set_ylabel('Cost', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Rotate x-axis labels for both axes
    ax1.set_xticklabels(months['Month'], rotation=45)
    ax2.set_xticklabels(months['Month'], rotation=45)

    # Annotate the line graph with CPA values including a dollar sign
    for index, row in months.iterrows():
        ax1.text(row['Month'], row['CPA'], f'${row["CPA"]:.2f}', ha='center', va='bottom', fontsize=8, color='purple')

    # Set labels and title
    plt.title('Monthly Cost vs CPA Performance', fontsize=20, pad=20)
    plt.legend(loc='upper left')


    # # Add the company logo
    # logo_path = "MiQ-logo-Copy1 (3).jpg"  # Replace with the actual path to your logo image
    # logo_img = plt.imread(logo_path)
    # imagebox = OffsetImage(logo_img, zoom=0.1)  # Adjust the zoom factor as needed
    # ab = AnnotationBbox(imagebox, (0.05, 0.8), frameon=False, pad=0.0, xycoords='axes fraction', boxcoords="axes fraction")
    # plt.gca().add_artist(ab)

    # plt.savefig('cpa.png', dpi=300, bbox_inches='tight')

    # Show the plot
    # plt.tight_layout()
    st.pyplot(fig)  # Display the Matplotlib figure in Streamlit



