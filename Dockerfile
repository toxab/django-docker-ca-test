FROM python:3.11-slim

# Do not write .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    netcat-openbsd \
    && apt-get clean

# Create a virtual environment
RUN python -m venv /opt/venv

# Set virtual environment as the default Python path
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose port for the application
EXPOSE 8000

# Run the entrypoint script with the provided command
CMD ["/app/entrypoint.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]
