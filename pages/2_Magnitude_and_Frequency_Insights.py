import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Magnitude Insights",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Magnitude Insights")
st.markdown(
    """
    Explore the distribution of earthquake magnitudes with this interactive histogram
    Use the filters in the sidebar to customize the visualization
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

# Magnitude Distribution Analysis
st.subheader("Magnitude Distribution")

if filtered_df.empty:
    st.warning("No earthquake data available for the selected filters.")
else:
    # Histogram
    fig_hist = px.histogram(
        filtered_df,
        x="magnitude",
        nbins=30,
        title="Distribution of Earthquake Magnitudes",
        labels={"magnitude": "Magnitude"},
        color_discrete_sequence=["#636EFA"],
    )
    fig_hist.update_layout(
        xaxis_title="Magnitude",
        yaxis_title="Count",
        bargap=0.05,
    )
    st.plotly_chart(fig_hist, use_container_width=True)