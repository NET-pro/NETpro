import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


def fetch_quiz_analytics(user_uuid):
    # Implement your logic to fetch additional analytics data based on user_uuid
    # Example: Fetching data from the analytics API
    api_endpoint = "http://localhost:5000/analytics/predict_future_quiz_scores"
    params = {"uuid": user_uuid}

    try:
        response = requests.get(api_endpoint, json=params)
        if response.status_code == 200:
            analytics_data = response.json()
            return analytics_data
        else:
            st.error(f"Error fetching analytics data: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error fetching analytics data: {str(e)}")
        return None


def app():

    # Streamlit app
    st.title("Quiz Analytics")

    # Fetch analytics data
    analytics_data = fetch_quiz_analytics(st.session_state.uuid)

    # Create a DataFrame from the analytics_data dictionary
    df = pd.DataFrame.from_dict(
        analytics_data, orient='index', columns=['Value'])
    df.index.name = 'Metric'
    df.reset_index(inplace=True)

    # Create a bar chart with a larger sizes
    fig, ax = plt.subplots(figsize=(20, 13))
    ax.bar(df["Metric"], df["Value"])

    # Display the larger bar charts using st.pyplot
    st.pyplot(fig)
