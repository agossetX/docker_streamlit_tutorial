import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Depth vs. Magnitude",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔎 Depth vs. Magnitude")
st.markdown(
    """
    Explore the relationship between earthquake depth and magnitude with this interactive scatter plot.
    Use the filters in the sidebar to customize the visualization.
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
        },
        inplace=True,
    )
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data()

# Sidebar Controls
st.sidebar.header("Filter Options")

# Date Range Selector
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


# Filter data based on selections
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date))
    & (df["Date"] <= pd.to_datetime(end_date))
    & (df["magnitude"] >= magnitude_range[0])
    & (df["magnitude"] <= magnitude_range[1])
]


# Depth vs. Magnitude Scatter Plot
st.subheader("Depth vs. Magnitude Scatter Plot")

if filtered_df.empty:
    st.warning("No earthquake data available for the selected filters.")
else:
    fig_scatter = px.scatter(
        filtered_df,
        x="depth",
        y="magnitude",
        size="magnitude",
        color="depth",
        color_continuous_scale="Viridis",
        hover_data=["Date", "latitude", "longitude"],
        title="Depth vs. Magnitude",
        labels={"depth": "Depth (km)", "magnitude": "Magnitude"},
    )

    fig_scatter.update_traces(marker=dict(line=dict(width=0.6, color='White'))) 
    
    fig_scatter.update_layout(
        xaxis_title="Depth (km)",
        yaxis_title="Magnitude",
        coloraxis_colorbar=dict(title="Depth (km)"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)