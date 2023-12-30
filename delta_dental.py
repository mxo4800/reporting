import pandas as pd

def delta(data, start_date, end_date):

    best_performing = {"KPI": [], "Variable": [], "Description": [], "KPI_Value": [], "Format": []}

    data["Date"] = pd.to_datetime(data["Date"])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    values = ["Request a Quote Fires", "Impressions", "Clicks", "Media Cost", "Video Plays", "Video Completions"]

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


    return best_performing, ctr_average, cpa_average, vcr_average


