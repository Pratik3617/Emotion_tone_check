# Base image
FROM python:3.10-slim

# Environment Variables

# prevents python from creating .pyc files and __pycache__ directories
ENV PYTHONDONTWRITEBYTECODE=1 

# forces python to flush output immediately instead of buffering it
ENV PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
