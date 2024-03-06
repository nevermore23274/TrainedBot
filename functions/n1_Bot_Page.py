import streamlit as st
from PIL import Image
import requests

def bot_query():
    # Function to send a query to the Flask API
    def get_prediction(query):
        response = requests.post("http://localhost:5000/predict", json={"text": query})
        if response.status_code == 200:
            return response.json()['prediction']
        else:
            st.error("Failed to get prediction from the model.")
            return "No prediction could be made."

    # Main page layout
    st.title("Bot Command Predictor")

    # Input field for the query
    query = st.text_input("Enter your query:")

    # Button for getting the predictiona
    if st.button("Predict"):
        if query:
            prediction = get_prediction(query)
            st.write(f"Prediction: {prediction}")
        else:
            st.error("Please enter a query.")

def bot_retrain():
    # Function to send feedback to the Flask API for retraining
    def send_feedback(query, expected_response):
        feedback_data = {
            "text": query,
            "expected_response": expected_response
        }
        # backend endpoint
        response = requests.post("http://localhost:5000/feedback", json=feedback_data)
        return response

    st.title("Bot Command Retraining")

    # Input fields for the query and expected response
    query = st.text_input("Enter your query:")
    expected_response = st.text_area("What should the correct response be:")

    # Button for submitting feedback
    if st.button("Submit Feedback"):
        if query and expected_response:
            response = send_feedback(query, expected_response)
            if response.status_code == 200:
                st.success("Feedback submitted successfully for retraining.")
            else:
                st.error("Failed to submit feedback. Please try again.")
        else:
            st.error("Please enter both the query and the expected response.")


page1_funcs = {
    "Bot Query": bot_query,
    "Bot Retraining": bot_retrain
}
