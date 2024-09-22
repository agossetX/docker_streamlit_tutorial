import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="1_Global Earthquake Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("🌍 Global Earthquake Explorer")
st.markdown(
    """
    Use this interactive map to explore earthquake events around the world !!
    Adjust the filters in the sidebar to refine your search
    """
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/earthquake.csv")
    df = df.dropna(subset=["Latitude", "Longitude", "Magnitude", "Depth"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df.rename(
        columns={
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Magnitude": "magnitude",
            "Depth": "depth",
            "Location Name": "location_name",
        },
        inplace=True,
    )
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data()

# Sidebar Controls
st.sidebar.header("Filter Options")

min_date = df["Date"].min()
max_date = df["Date"].max()

start_date = st.sidebar.date_input(
    "Start Date", min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "End Date", max_date, min_value=min_date, max_value=max_date
)

if start_date > end_date:
    st.sidebar.error("Error: End date must fall after start date.")


# Magnitude Range Slider
min_magnitude = float(df["magnitude"].min())
max_magnitude = float(df["magnitude"].max())
magnitude_range = st.sidebar.slider(
    "Magnitude Range",
    min_value=min_magnitude,
    max_value=max_magnitude,
    value=(7.00, 8.75),
    step=0.1,
)

# Depth Range Slider
min_depth = float(df["depth"].min())
max_depth = float(df["depth"].max())
depth_range = st.sidebar.slider(
    "Depth Range (km)",
    min_value=min_depth,
    max_value=max_depth,
    value=(50.00, 200.00),
    step=1.0,
)

# Filter data based on selections
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date))
    & (df["Date"] <= pd.to_datetime(end_date))
    & (df["magnitude"] >= magnitude_range[0])
    & (df["magnitude"] <= magnitude_range[1])
    & (df["depth"] >= depth_range[0])
    & (df["depth"] <= depth_range[1])
]

# Check if data is available
if filtered_df.empty:
    st.warning("No earthquake data available for the selected filters.")
else:
    # Create the map using Viridis color scale
    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="magnitude",
        size="magnitude",
        color_continuous_scale=px.colors.sequential.Viridis,
        size_max=15,
        zoom=1,
        mapbox_style="open-street-map",
        hover_data={
            "Date": True,
            "Time": True,
            "Type": True,
            "depth": True,
            "magnitude": True,
        },
        title="Earthquake Events",
    )

    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        coloraxis_colorbar={
            "title": "Magnitude",
            "lenmode": "fraction",
            "len": 0.75,
        },
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show data table (optional)
    if st.checkbox("Show Data Table"):
        st.dataframe(
            filtered_df[
                [
                    "Date",
                    "Time",
                    "latitude",
                    "longitude",
                    "depth",
                    "magnitude",
                    "Type",
                    "Status",
                ]
            ]
            .sort_values("Date", ascending=False)
            .reset_index(drop=True)
        )