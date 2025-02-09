FROM python:3.9-slim-buster

WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY ./src/requirements.txt ./

# Install dependencies. Make sure to include all dependencies in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome and Chromedriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code.  Crucially, copy from the *parent* directory
COPY . .

# Expose the port that FastAPI will listen on
EXPOSE 8000

# Set environment variables (important for Selenium in Docker)
ENV DISPLAY=:99

# Command to run the application
CMD Xvfb :99 -screen 0 1280x720x24 & uvicorn src.main:app --host 0.0.0.0 --port 8000