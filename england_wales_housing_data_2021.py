import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

#st.title("Housing Tenure Insights for England & Wales")
st.markdown("<h1 style='text-align: justify;'>Housing Tenure Insights for England and Wales</h1>", unsafe_allow_html=True)

st.subheader("prepared by Queeneth Okpala")
st.markdown("---")

file_path = "householdcharacteristicsbytenureenglandandwalescensus2021.xlsx"

xls = pd.ExcelFile(file_path)

df_1 = xls.parse("1a", header=2)
df_1.rename(columns={"Owned: \nOwns outright": "Owned: Owns outright", "Private rented:\nOther": "Private rented: Other"}, inplace=True)
df_1["Lives rent free"] = pd.to_numeric(df_1["Lives rent free"], errors="coerce")

df_1["Total Owned"] = df_1["Owned: Owns outright"] + df_1["Owned: Owns with a mortgage or loan"]
df_1["Total Rented"] = (
    df_1["Social rented"]
    + df_1["Private rented: Private landlord or letting agency"]
    + df_1["Private rented: Employer of a household member"]
    + df_1["Private rented: Relative or friend of household member"]
    + df_1["Private rented: Other"]
)

# 1st Chart
df_national = df_1.copy()
df_national = df_national[df_national["Area name"].isin(["England", "Wales"])]
sns.set_theme(style="dark")
fig, ax = plt.subplots(figsize=(6,6))
ax.pie([df_national["Total Owned"].sum(), df_national["Total Rented"].sum()], labels=["Owned", "Rented"], autopct="%1.1f%%", colors=sns.color_palette("Paired",2), startangle=90, wedgeprops={"edgecolor": "black"}, textprops={"fontsize": 12, "weight": "bold", "color": "black"})
ax.set_title("Overall Home Ownership vs. Renting in England & Wales", fontsize=14)
st.pyplot(fig)
st.markdown("---")

## Chart 2
# Data reshaped for use in Plotly
df_melted = df_national.melt(id_vars=["Area name"], value_vars=["Total Owned", "Total Rented"],
                             var_name="Housing Type", value_name="Households")

fig = px.bar(
    df_melted,
    x="Area name",
    y="Households",
    color="Housing Type",
    title="Home Ownership vs Renting by Region (England & Wales)",
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Prism
)

# Layout
fig.update_layout(
    title_font = dict(size=20, family="Arial", color="black"),
    xaxis = dict(title="Region", title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title="Number of Households", title_font=dict(size=16, family="Arial", color="black")),
    legend_title="Housing Type",
    width=600,
    height=400,
    template="plotly_white",
)

st.plotly_chart(fig)
st.markdown("---")

exclude_columns = ["Total Owned", "Total Rented", "Area code", "Lives rent free"]
df_filtered = df_national.drop(columns=exclude_columns, errors='ignore')

df_melted2 = df_filtered.reset_index().melt(id_vars=["Area name"], var_name="Tenure Type", value_name="Number of Households")

fig_england = px.bar(
    df_melted2[df_melted2["Area name"] == "England"].sort_values(by="Number of Households", ascending=False),
    x="Tenure Type",
    y="Number of Households",
    title="Tenure Distribution in England",
    labels={"Tenure Type": "Tenure Type", "Number of Households": "Number of Households"},
    color_discrete_sequence=["#8B0000"]
)

fig_england.update_layout(
    title_font = dict(size=20, family="Arial", color="black"),
    xaxis = dict(title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title_font=dict(size=16, family="Arial", color="black")),
    xaxis_tickangle=30,
    template="plotly_white",
    height=800,
    width=700)
st.plotly_chart(fig_england)
st.markdown("---")

fig_wales = px.bar(
    df_melted2[df_melted2["Area name"] == "Wales"].sort_values(by="Number of Households", ascending=False),
    x="Tenure Type",
    y="Number of Households",
    title="Tenure Distribution in Wales",
    labels={"Tenure Type": "Tenure Type", "Number of Households": "Number of Households"},
    color_discrete_sequence=["#006400"]
)

fig_wales.update_layout(
    title_font = dict(size=20, family="Arial", color="black"),
    xaxis = dict(title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title_font=dict(size=16, family="Arial", color="black")),
    xaxis_tickangle=30,
    template="plotly_white",
    height=800,
    width=700,
)
st.plotly_chart(fig_wales)
st.markdown("---")


df_england_regions = df_1.copy()

df_england_regions = df_england_regions[df_england_regions["Area code"].str.contains("E12")]

# Top and bottom home ownership regions
top_owned_regions = df_england_regions.sort_values(by="Total Owned", ascending=True)[["Area name", "Total Owned"]]

fig_top_owned = px.bar(
    top_owned_regions,
    x="Total Owned",
    y="Area name",
    title=" Home Ownership in English Regions",
    orientation="h",  # Horizontal bars
    color="Total Owned",  # Colour by value
    color_continuous_scale="blues",  # gradient
    text_auto= True # to show values on bars
)

fig_top_owned.update_layout(
    template="plotly_white",
    title_font = dict(size=20, family="Arial", color="black"),
    width=800,
    height=500,
    xaxis_title="<b>Total Owned</b>",
    yaxis_title="<b>Region</b>",
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#C2CCE5",
   font=dict(family="Arial", color="black")
)

st.plotly_chart(fig_top_owned)
st.markdown("---")


# Top and bottom home rental regions
top_rental_regions = df_england_regions.sort_values(by="Total Rented", ascending=False)[["Area name", "Total Rented"]]

fig_top_rented = px.bar(
    top_rental_regions,
    x="Total Rented",
    y="Area name",
    title="Rentals in English Regions",
    orientation="h",
    color="Total Rented",
    color_continuous_scale="peach",
    text_auto= True
)

fig_top_rented.update_layout(
    template="plotly_white",
    title_font = dict(size=20, family="Arial", color="black"),
    width=800,
    height=500,
    xaxis_title="<b>Total Owned</b>",
    yaxis_title="<b>Region</b>",
    yaxis=dict(tickangle=0),
    xaxis=dict(tickangle=0),
    #margin=dict(l=120, r=20, t=40, b=40),
    font=dict(family="Arial", color="black"),
    plot_bgcolor="#FDF7EC",
    paper_bgcolor="white",
)

st.plotly_chart(fig_top_rented)
st.markdown("---")


df_local_authorities = df_1.copy()

df_local_authorities = df_local_authorities[
    (~df_local_authorities["Area name"].isin(["England and Wales", "England", "Wales"]))
    & (~df_local_authorities["Area name"].isin(["North East", "North West", "Yorkshire and The Humber",
                                "East Midlands", "West Midlands", "East of England",
                                "London", "South East", "South West"]))
]

# Top and bottom 10 local authority districts (owned)
top_owned_local = df_local_authorities.sort_values(by="Total Owned", ascending=False)[["Area name", "Total Owned"]].head(10)
bottom_owned_local = df_local_authorities.sort_values(by="Total Owned", ascending=True)[["Area name", "Total Owned"]].head(10)

# Chart for top owned local authorities
fig_top_lollipop = go.Figure()

fig_top_lollipop.add_trace(go.Scatter(
    x=top_owned_local["Total Owned"],
    y=top_owned_local["Area name"],
    mode="markers+lines+text",  # Line & dot combo (text to show values)
    marker=dict(size=10, color="blue"),
    line=dict(color="blue", width=2),
    text=top_owned_local["Total Owned"], # Show values on markers
    textposition="middle right",  # Adjust position for better visibility
    name="Top 10 Owned"
))

fig_top_lollipop.update_layout(
    title="Top 10 Local Authority Districts for Home Ownership",
    title_font = dict(size=20, family="Arial", color="black"),
    font=dict(family="Arial", color="black"),
    xaxis = dict(title="Total Owned", title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title="Local Authority", title_font=dict(size=16, family="Arial", color="black")),
    width=700,
    height=450,
    template="plotly",
    paper_bgcolor="#C2CCE5"
)


# Chart for bottom owned local authorities
fig_bottom_lollipop = go.Figure()

fig_bottom_lollipop.add_trace(go.Scatter(
    x=bottom_owned_local["Total Owned"],
    y=bottom_owned_local["Area name"],
    mode="markers+lines+text",
    marker=dict(size=10, color="red"),
    line=dict(color="red", width=2),
    text=bottom_owned_local["Total Owned"],
    textposition="middle left",
    name="Bottom 10 Owned"
))

fig_bottom_lollipop.update_layout(
    title="Bottom 10 Local Authority Districts for Home Ownership",
    title_font = dict(size=20, family="Arial", color="black"),
    font=dict(family="Arial", color="black"),
    xaxis = dict(title="Total Owned", title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title="Local Authority", title_font=dict(size=16, family="Arial", color="black")),
    width=700,
    height=450,
    template="plotly",
    paper_bgcolor="#C2CCE5"
)


st.plotly_chart(fig_top_lollipop, key="2")
st.markdown("---")

st.plotly_chart(fig_bottom_lollipop, key="3")
st.markdown("---")


# Top and bottom 10 local authority districts (rental)
top_rental_local = df_local_authorities.sort_values(by="Total Rented", ascending=False)[["Area name", "Total Rented"]].head(10)
bottom_rental_local = df_local_authorities.sort_values(by="Total Rented", ascending=True)[["Area name", "Total Rented"]].head(10)

# Chart for top rented local authorities
fig_top_lollipop = go.Figure()

fig_top_lollipop.add_trace(go.Scatter(
    x=top_rental_local["Total Rented"],
    y=top_rental_local["Area name"],
    mode="markers+lines+text",
    marker=dict(size=10, color="blue"),
    line=dict(color="blue", width=2),
    text=top_rental_local["Total Rented"],
    textposition="middle right",
    name="Top 10 Rented"
))

fig_top_lollipop.update_layout(
    title="Top 10 Local Authority Districts for Rental",
    title_font = dict(size=20, family="Arial", color="black"),
    font=dict(family="Arial", color="black"),
    xaxis = dict(title="Total Rented", title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title="Local Authority", title_font=dict(size=16, family="Arial", color="black")),
    width=700,
    height=450,
    template="plotly",
    paper_bgcolor="#C2CCE5"
)

# Chart for bottom rented local authorities
fig_bottom_lollipop = go.Figure()

fig_bottom_lollipop.add_trace(go.Scatter(
    x=bottom_rental_local["Total Rented"],
    y=bottom_rental_local["Area name"],
    mode="markers+lines+text",
    marker=dict(size=10, color="red"),
    line=dict(color="red", width=2),
    text=bottom_rental_local["Total Rented"],
    textposition="middle left",
    name="Bottom 10 Rented"
))

fig_bottom_lollipop.update_layout(
    title="Bottom 10 Local Authority Districts for Rental",
    title_font = dict(size=20, family="Arial", color="black"),
    font=dict(family="Arial", color="black"),
    xaxis = dict(title="Total Rented", title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title="Local Authority", title_font=dict(size=16, family="Arial", color="black")),
    width=700,
    height=450,
    template="plotly",
    paper_bgcolor="#C2CCE5"
)


st.plotly_chart(fig_top_lollipop, key="4")
st.markdown("---")

st.plotly_chart(fig_bottom_lollipop, key="5")
st.markdown("---")




df_for_map = df_1.copy()

df_geo = pd.read_excel("uk_la_future.xlsx", sheet_name="uk_local_authorities_future")

df_geo.info()


# Renaming column on the geo data to align with the housing data
df_geo.rename(columns={"gss-code": "Area code"}, inplace=True)

# Selecting relevant columns for the Bubble map
df_geo_subset = df_geo[["Area code", "long", "lat"]]

# Merging only lat/lon with df_local
df_merged = df_for_map.merge(df_geo_subset, on="Area code", how="left")

# Dropping rows for national & regional area codes
df_merged = df_merged.dropna(subset=["long", "lat"])

# Bubble Map
fig = px.scatter_mapbox(
    df_merged,
    lon="long",
    lat="lat",
    size="Total Rented",  # Bubble size based on rental/homeownership
    color="Total Owned",  # Colour based on renting/homeownership levels
    hover_name="Area name",  # Show Area Name on hover
    hover_data={"Total Owned": True, "Total Rented": True, "lat": False, "long": False},
    title="Homeownership Concentration Across Local Authorities",
    color_continuous_scale="Blues",  # Adjust color scheme
    size_max=50,  # Adjust max bubble size
    opacity=0.8
)

# Set Mapbox Style
fig.update_layout(
    height=1000,
    width=1000,
    title_font = dict(size=20, family="Arial", color="black"),
    mapbox_style="open-street-map",
    mapbox_zoom=6,  # Adjust zoom level
    mapbox_center={"lon": df_merged["long"].mean(), "lat": df_merged["lat"].mean()}  # Center map
)


st.plotly_chart(fig, key="6")
st.markdown("---")


df_2a = xls.parse("2a", header=2)

df_2a = xls.parse("2a", header=2)

df_2a.rename(columns={"Owned: \nOwns outright": "Owned: Owns outright", "Owned: Owns with a mortgage, \nloan or shared ownership": "Owned: Owns with a mortgage, loan or shared ownership","Private rented or \nlives rent free": "Private rented or lives rent free"}, inplace=True)

columns_to_convert = ["Owned: Owns outright", "Owned: Owns with a mortgage, loan or shared ownership", "Social rented", "Private rented or lives rent free"]
df_2a[columns_to_convert] = df_2a[columns_to_convert].apply(pd.to_numeric, errors="coerce")

df_2a["Total Owned"] = df_2a["Owned: Owns outright"] + df_2a["Owned: Owns with a mortgage, loan or shared ownership"]
df_2a["Total Rented"] = df_2a["Social rented"] + df_2a["Private rented or lives rent free"]

df2a_national = df_2a.copy()

df2a_national = df2a_national[df2a_national["Area name"].isin(["England", "Wales"])]
df2a_england_regions = df_2a.copy()

df2a_england_regions = df2a_england_regions[df2a_england_regions["Area code"].str.contains("E12")]

df_long = df2a_england_regions.melt(
    id_vars=["Household size", "Area name"],
    value_vars=["Total Owned", "Total Rented"],
    var_name="Tenure Type",
    value_name="Number of Households"
)


# Interactive dropdown for regions
fig = px.bar(df_long,
             x="Household size",
             y="Number of Households",
             color="Tenure Type",
             barmode="group",
             facet_col_wrap=3,  # Wrap subplots into multiple rows for better visibility
             animation_frame="Area name",  # Adds a dropdown to switch between regions
             title="Homeownership vs Renting by Household Size (English Regions)",
             labels={"Household size": "Household Size", "value": "Number of Households"},
             height=700,
             width=900,
             color_discrete_sequence=px.colors.qualitative.Pastel)

fig.update_layout(
    xaxis=dict(tickangle=20),
    template="plotly",
    title_font = dict(size=20, family="Arial", color="black"),
    font=dict(family="Arial", color="black"),
    legend=dict(font=dict(size=14, family="Arial", color="black")),
   # xaxis = dict(title_font=dict(size=16, family="Arial", color="black")),
    yaxis= dict(title_font=dict(size=16, family="Arial", color="black"))

)

st.plotly_chart(fig, key="7")
st.markdown("---")


df_4a = xls.parse("4a", header=2)

df_4a.rename(columns={"Owned: \nOwns outright": "Owned: Owns outright", "Owned: Owns with a mortgage, \nloan or shared ownership": "Owned: Owns with a mortgage, loan or shared ownership","Private rented or \nlives rent free": "Private rented or lives rent free"}, inplace=True)

columns_to_convert = ["Owned: Owns outright"]
df_4a[columns_to_convert] = df_4a[columns_to_convert].apply(pd.to_numeric, errors="coerce")

df_4a["Total Owned"] = df_4a["Owned: Owns outright"] + df_4a["Owned: Owns with a mortgage, loan or shared ownership"]

df_4a["Total Rented"] = df_4a["Social rented"] + df_4a["Private rented or lives rent free"]

df_ew = df_4a[df_4a["Area name"] == "England and Wales"]

df_ew_long = df_ew.melt(id_vars=["Age of the household reference person"],
                        value_vars=["Total Owned", "Total Rented"],
                        var_name="Tenure Type",
                        value_name="Number of Households")


# Compute % for each tenure type within each age group
df_ew_long["Percentage"] = df_ew_long.groupby("Age of the household reference person")["Number of Households"].transform(lambda x: (x / x.sum()) * 100)


fig = px.bar(df_ew_long,
             x="Age of the household reference person",
             y="Number of Households",
             color="Tenure Type",
             barmode="group",
             title="Homeownership vs Renting by Age Group (England & Wales)",
             labels={"Age of the household reference person": "Age Group"},
             height=600,
             width=1000,
             #color_discrete_sequence=px.colors.qualitative.Bold
             color_discrete_map={"Total Owned": "#1D3557", "Total Rented": "#E67E22"},
             text=df_ew_long["Percentage"].apply(lambda x: f"{x:.1f}%") # Format as percentage
           )

fig.update_layout(
    template="plotly",
    title_font = dict(size=20, family="Arial", color="black"),
    font=dict(family="Arial", color="black"),
    legend=dict(font=dict(size=14, family="Arial", color="black")),
    xaxis = dict(title_font=dict(size=16, family="Arial", color="black"), tickangle=15),
    yaxis= dict(title_font=dict(size=16, family="Arial", color="black")),
    paper_bgcolor="#C2CCE5"

)

st.plotly_chart(fig, key="8")
st.markdown("---")


df_7a = xls.parse("7a", header=2)

df_7a.rename(columns={"Owned: \nOwns outright": "Owned: Owns outright", "Owned: Owns with a mortgage, \nloan or shared ownership": "Owned: Owns with a mortgage, loan or shared ownership","Private rented or \nlives rent free": "Private rented or lives rent free"}, inplace=True)

columns_to_convert = ["Owned: Owns outright", "Owned: Owns with a mortgage, loan or shared ownership", "Social rented", "Private rented or lives rent free"]
df_7a[columns_to_convert] = df_7a[columns_to_convert].apply(pd.to_numeric, errors="coerce")

df_7a["Total Owned"] = df_7a["Owned: Owns outright"] + df_7a["Owned: Owns with a mortgage, loan or shared ownership"]
df_7a["Total Rented"] = df_7a["Social rented"] + df_7a["Private rented or lives rent free"]

df_eng_wales = df_7a[df_7a["Area name"] == "England and Wales"]
df_regions = df_7a[df_7a["Area name"].isin(["North East", "North West", "Yorkshire and The Humber",
                                            "East Midlands", "West Midlands", "East of England",
                                            "London", "South East", "South West"])]
df_local_authorities = df_7a[
    (~df_7a["Area name"].isin(["England and Wales", "England", "Wales"]))
    & (~df_7a["Area name"].isin(["North East", "North West", "Yorkshire and The Humber",
                                "East Midlands", "West Midlands", "East of England",
                                "London", "South East", "South West"]))
]

df_ethnic_totals = df_7a[df_7a["Household combination of resident ethnic group"].str.contains("Total")]
df_ethnic_subgroups = df_7a[~df_7a["Household combination of resident ethnic group"].str.contains("Total")]

df_ethnic_total = df_eng_wales[df_eng_wales["Household combination of resident ethnic group"].str.startswith("Total")].copy()

# Convert Ownership Counts to Percentages
df_ethnic_total["Ownership Percentage"] = (df_ethnic_total["Owned: Owns outright"] / df_ethnic_total["Owned: Owns outright"].sum()) * 100

fig = px.treemap(
    df_ethnic_total,
    path=["Household combination of resident ethnic group"],
    values="Ownership Percentage",  # Now using percentage
    title="Homeownership Breakdown by Ethnic Group",
    color="Ownership Percentage",
    color_continuous_scale="Blues",
    hover_data={"Ownership Percentage": ":.1f"}  # Display percentage in hover
)

# Step 3: Improve Readability
fig.update_traces(
    textinfo="label+text+value",  # Show label + % value inside the boxes
    texttemplate="%{label}<br>%{value:.1f}%", # Format inside text as "Label + %"
    textfont_size=14,
    )

# Change Legend Title to "% Ownership"
fig.update_layout(
    coloraxis_colorbar=dict(title="% Ownership"),  # Modify legend title
    template="plotly_white",
    title_font = dict(size=20, family="Arial", color="black"),
    font=dict(family="Arial", color="black"),
    legend=dict(font=dict(size=14, family="Arial", color="black")),
    xaxis = dict(title_font=dict(size=16, family="Arial", color="black"), tickangle=15),
    yaxis= dict(title_font=dict(size=16, family="Arial", color="black")),
    paper_bgcolor="#C2CCE5"

)

st.plotly_chart(fig, key="9")
st.markdown("---")



df_11a = xls.parse("11a", header=2)

df_11a.rename(columns={"Owned: \nOwns outright": "Owned: Owns outright", "Owned: Owns with a mortgage, \nloan or shared ownership": "Owned: Owns with a mortgage, loan or shared ownership","Private rented or \nlives rent free": "Private rented or lives rent free"}, inplace=True)

columns_to_convert = ["Owned: Owns outright", "Owned: Owns with a mortgage, loan or shared ownership", "Social rented", "Private rented or lives rent free"]
df_11a[columns_to_convert] = df_11a[columns_to_convert].apply(pd.to_numeric, errors="coerce")



regions = [
    "North East", "North West", "Yorkshire and The Humber", "East Midlands",
    "West Midlands", "East of England", "London", "South East", "South West"
]
df_regions = df_11a[df_11a["Area name"].isin(regions)].copy()

df_regions["Total Owned"] = df_regions["Owned: Owns outright"] + df_regions["Owned: Owns with a mortgage, loan or shared ownership"]
df_regions["Total Rented"] = df_regions["Social rented"] + df_regions["Private rented or lives rent free"]


# Normalize Data (Convert to % of Total Households per occupation)
df_regions["Total Households"] = df_regions["Total Owned"] + df_regions["Total Rented"]
df_regions["Owned %"] = (df_regions["Total Owned"] / df_regions["Total Households"]) * 100
df_regions["Rented %"] = (df_regions["Total Rented"] / df_regions["Total Households"]) * 100

df_long = df_regions.melt(
    id_vars=["Area name", "Occupation of the household reference person"],
    value_vars=["Owned %", "Rented %"],
    var_name="Tenure Type",
    value_name="Percentage"
)

# Plot Heatmap
fig = px.density_heatmap(
    df_long,
    x="Area name",
    y="Occupation of the household reference person",
    z="Percentage",
    facet_col="Tenure Type",  # One heatmap for Owned % and one for Rented %
    color_continuous_scale="Blues",
    height=500,
    width=1200,
    title="Homeownership vs Renting by Occupation Across 9 English Regions (Heatmap)",
)

st.plotly_chart(fig, key="10")
st.markdown("---")