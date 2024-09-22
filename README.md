# docker_streamlit_tutorial

## Description

In this repository I build a basic Streamlit app and containerize it using docker


## Installation

### Prerequisites
- Python 3.7 or higher
- Streamlit
- Docker
- pandas
- plotly
- numpy


## Usage

### Running Streamlit App Locally
1. Navigate to the project directory:

    ```sh
    cd docker_streamlit_tutorial
    ```

2. Start the Streamlit:

    ```sh
    streamlit run Home.py
    ```

### Running Streamlit App with Docker

1. Build the Docker image:
    ```sh
    docker build -t streamlit-app .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8501:8501 streamlit-app
    ```

3. Open your browser and go to `http://localhost:8501` to see the app.

4. If need be you can find the docker image [here](https://hub.docker.com/r/agosset29/streamlit-app) or pull it using `docker pull agosset29/streamlit-app:latest`