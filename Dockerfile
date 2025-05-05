FROM python:3.11-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application
CMD gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT main:app

