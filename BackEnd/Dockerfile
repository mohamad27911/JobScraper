# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY ./src/requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome, Chromedriver, and required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    chromium \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Chromedriver (matching installed Chrome version)
RUN CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will use
EXPOSE 8000

# Set environment variables (important for Selenium in Docker)
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/local/bin/chromedriver

# Command to run the application
CMD Xvfb :99 -screen 0 1280x720x24 & uvicorn src.main:app --host 0.0.0.0 --port 8000
