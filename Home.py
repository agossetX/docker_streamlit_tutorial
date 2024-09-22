import streamlit as st

st.set_page_config(
    page_title="Interactive Earthquake Data Explorer",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🌎 Interactive Earthquake Data Explorer")
st.markdown(
    """
    Welcome to the **Interactive Earthquake Data Explorer** ! This simple streamlit app allows you to explore global earthquake data through interactive maps and insightful visualizations
    
    **Features:**
    - **Global Earthquake Explorer:** Visualize recent earthquake events around the world
    - **Magnitude and Frequency Insights:** Analyze the distribution and frequency of earthquake magnitudes over time
    - **Depth vs Magnitude Analysis:** Explore the relationship between earthquake depth and magnitude
    """
)

# Acknowledgment
st.markdown(
    """
    ---
    This app is based on this kaggle earthquake [dataset](https://www.kaggle.com/datasets/usgs/earthquake-database/data) and some of the work was inspired by this github repository [Earthquake Data Analysis](https://github.com/xDiste/EarthquakeAnalysis)
    """
)


st.sidebar.success("Select a Visualization above!")
st.sidebar.image(
    "earthquake.jpg",
    use_column_width=True
)