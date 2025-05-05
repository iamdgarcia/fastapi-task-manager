FROM python:3.11-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY streamlit_requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Set environment variables
ENV PORT=8501
ENV HOST=0.0.0.0
ENV API_URL=http://backend:8000

# Expose the port the app will run on
EXPOSE 8501

# Command to run the application
CMD streamlit run app.py --server.port=$PORT --server.address=$HOST
