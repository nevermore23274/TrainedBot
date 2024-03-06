# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the necessary files into the container
COPY ./requirements.txt ./requirements.txt
COPY ./predict_api.py ./predict_api.py
COPY ./main.py ./main.py
COPY ./functions ./functions

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create the nltk_data directory and set permissions
RUN mkdir -p /usr/src/app/nltk_data && chmod -R 777 /usr/src/app/nltk_data

# Create the directory for feedback data and set write permissions
RUN mkdir -p /usr/src/app/data && chmod -R 777 /usr/src/app/data

# Create an empty feedback_data.csv file and set permissions
RUN touch /usr/src/app/data/feedback_data.csv && chmod 666 /usr/src/app/data/feedback_data.csv

# Make port 8501 available for the Streamlit app
# Make port 5000 available for the Flask API
EXPOSE 8501
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py (Streamlit) and predict_api.py (Flask API) when the container launches
CMD streamlit run main.py --server.port 8501 & gunicorn --bind 0.0.0.0:5000 predict_api:app
