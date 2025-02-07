FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium
ENV PATH="/usr/lib/chromium-browser/:${PATH}"

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
