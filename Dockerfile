
# Start from a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the files needed
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY .. 

# Default command (you can change this later)
CMD ["python", "load/load_to_bigquery.py"]
