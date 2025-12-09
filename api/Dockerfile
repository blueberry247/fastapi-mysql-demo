# Use an official lightweight Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file first (for better build caching)
COPY requirements.txt .

# Install Python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application package into the container
COPY app ./app

# Command to run when the container starts:
#   - uvicorn runs The FastAPI app
#   - "app.main:app" means package app/, module main.py, variable 'app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



