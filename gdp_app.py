# Task 3:
#       Reuse your python file that webscrapes GDP by country from this link (https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)). 
#       and plots a stacked interactive bar plot using plotly. Stack countries within regions using the IMF numbers. 
#       Create streamlit app that displays a stacked bar plot of country GDPs stacked within regions. 
#       Allow the user to select between the IMF, UN and World Bank reported numbers.

# Task 3:
# Reuse your python file that webscrapes GDP by country from this link 
# (https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal))
# and plots a stacked interactive bar plot using plotly.
# Stack countries within regions using the IMF numbers.
# Create streamlit app that displays a stacked bar plot of country GDPs stacked within regions.
# Allow the user to select between the IMF, UN and World Bank reported numbers.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as pc
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="🌍 Country GDP Stacked Bar",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌍 GDP by Country (Stacked by Region)")
st.write("""
This app displays GDP by country stacked within regions.
Choose the data source: **IMF**, **UN**, or **World Bank**.
""")

# --- Select Source ---
source = st.selectbox("Select data source:", ["IMF", "UN", "World Bank"])

# --- Load GDP Data Function ---
@st.cache_data
def load_gdp_data():
    wiki_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    resp = requests.get(wiki_url, headers=headers)
    resp.raise_for_status()
    tables = pd.read_html(resp.text)

    # Find the main GDP table (the one with "IMF" in its columns)
    gdp_df = None
    for tbl in tables:
        if any("IMF" in str(col) for col in tbl.columns):
            gdp_df = tbl
            break
    if gdp_df is None:
        raise ValueError("No GDP table found on Wikipedia.")

    gdp_df.columns = [str(c).replace("\n", " ").strip() for c in gdp_df.columns]
    cols = list(gdp_df.columns)
    country_col = cols[0]
    imf_col = next((c for c in cols if "IMF" in c), None)
    wb_col = next((c for c in cols if "World Bank" in c), None)
    un_col = next((c for c in cols if "United Nations" in c or "United Nation" in c), None)

    gdp_df = gdp_df[[country_col, imf_col, wb_col, un_col]].copy()
    
    gdp_df.columns = ["Country", "IMF", "World Bank", "UN"]

    # Clean country names and GDP numbers
    gdp_df["Country"] = gdp_df["Country"].astype(str).str.replace(r"\[.*\]", "", regex=True).str.strip()
    for col in ["IMF", "World Bank", "UN"]:
        gdp_df[col] = pd.to_numeric(
            gdp_df[col].astype(str).str.replace(r"[^\d.]", "", regex=True),
            errors="coerce"
        )
    
    # Filter out 'World' or aggregates
    exclude = [
        "World", "World total", "European Union", "Eurozone",
        "Asia", "Africa", "Europe", "Americas", "Oceania"
    ]
    gdp_df = gdp_df[~gdp_df["Country"].isin(exclude)]

    gdp_df.dropna(subset=["IMF", "World Bank", "UN"], how="all", inplace=True)
    return gdp_df

# --- Get Clean Data ---
data = load_gdp_data()

# --- Region Mapping ---
region_map = {
    "United States": "North America", "Canada": "North America", "Mexico": "North America",
    "Brazil": "South America", "Argentina": "South America", "Chile": "South America",
    "Colombia": "South America", "Peru": "South America", "Venezuela": "South America",
    "Germany": "Europe", "France": "Europe", "Italy": "Europe", "United Kingdom": "Europe",
    "Spain": "Europe", "Netherlands": "Europe", "Sweden": "Europe", "Poland": "Europe",
    "Russia": "Europe/Asia", "Turkey": "Europe/Asia", "Ukraine": "Europe", "Switzerland": "Europe",
    "China": "Asia", "Japan": "Asia", "India": "Asia", "Indonesia": "Asia",
    "South Korea": "Asia", "Saudi Arabia": "Asia", "Thailand": "Asia", "Malaysia": "Asia",
    "Vietnam": "Asia", "Philippines": "Asia", "Singapore": "Asia",
    "South Africa": "Africa", "Egypt": "Africa", "Nigeria": "Africa", "Kenya": "Africa",
    "Ethiopia": "Africa", "Ghana": "Africa", "Algeria": "Africa", "Morocco": "Africa",
    "Australia": "Oceania", "New Zealand": "Oceania",
    "United Arab Emirates": "Middle East", "Israel": "Middle East",
    "Qatar": "Middle East", "Kuwait": "Middle East"
}

data["Region"] = data["Country"].map(region_map).fillna("Other")

# --- Filter by source ---
plot_df = data[["Country", "Region", source]].rename(columns={source: "GDP"})
plot_df.dropna(subset=["GDP"], inplace=True)

# --- Limit to Top N + "Other" ---
TOP_N = 10

top_countries = (
    plot_df
    .sort_values(["Region", "GDP"], ascending=[True, False])
    .groupby("Region")
    .head(TOP_N)
    .reset_index(drop=True)
)

others = (
    plot_df
    .merge(top_countries[["Country"]], on="Country", how="left", indicator=True)
    .query("_merge == 'left_only'")
    .groupby("Region", as_index=False)
    .agg(Country=("Country", lambda s: "Other (rest)"), GDP=("GDP", "sum"))
)

plot_df = pd.concat([top_countries, others], ignore_index=True)
plot_df = plot_df.sort_values(["Region", "GDP"], ascending=[True, False])

# --- Pivot and reshape for stacking ---
pivot = plot_df.pivot_table(
    index="Region",
    columns="Country",
    values="GDP",
    aggfunc="sum",
    fill_value=0
)
long_df = pivot.reset_index().melt(id_vars="Region", var_name="Country", value_name="GDP")

# --- Generate a color scale ---
n_colors = long_df["Country"].nunique()
color_scale = pc.sample_colorscale("Rainbow", [i / (n_colors - 1) for i in range(n_colors)])

# --- Plot ---
fig = px.bar(
    long_df,
    x="Region",
    y="GDP",
    color="Country",
    title=f"GDP by Country (Stacked by Region) - {source}",
    labels={"GDP": "GDP (US$ million)", "Region": "Region"},
    barmode="stack",
    color_discrete_sequence=color_scale
)

fig.update_layout(
    xaxis_title="Region",
    yaxis_title="GDP (US$ million)",
    legend_title="Country",
    template="plotly_white",
    height=650,
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)
