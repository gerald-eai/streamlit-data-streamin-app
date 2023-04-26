# app/Dockerfile
# select an image to use 
FROM python:3.9-slim
# create a working directory
WORKDIR /app
# install necessary software packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements to working directory 
COPY . .
#clone the example app from streamlit official repository
# RUN git clone https://github.com/streamlit/streamlit-example.git .


# install necessay python libraries
RUN pip3 install -r requirements.txt
# expose the port to run on 
EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
WORKDIR /app

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]