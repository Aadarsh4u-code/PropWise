# base image
FROM python:3.9-slim-bullseye

# Set working directory
WORKDIR /app

# Copy project files to the working directory 
COPY . /app

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Run pip install to install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Environment variable to enable unbuffered logging
ENV PYTHONUNBUFFERED=1

# Command to run on container startup
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

# Build command
# docker build -t aadarsh020/propwise .

# Push to docker hub
# docker push aadarsh020/propwise

# Pull from docker hub
# docker pull aadarsh020/propwise

# Run the container
# docker run -d -p 8501:8501 aadarsh020/prop
