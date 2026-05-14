# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application code
COPY app.py .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the MCP server
CMD ["python", "app.py"]
