FROM python:3.14.2-slim

WORKDIR /app

# Copy requirements from REST directory
COPY REST/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy fmodule and REST contents
COPY config ./config
COPY fmodule ./fmodule
COPY REST/main.py .

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8080

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]