# Use a lightweight Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copies the requirements.txt file 
# This helps Docker cache dependency installation
COPY requirements.txt .

# Install the required Linux tools and Python packages
RUN apt-get update && apt-get install -y curl zip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 so the FastAPI app can be reached
EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]