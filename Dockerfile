FROM python:3.10-slim as base

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt update -qq && \
    apt install -y -qq --no-install-recommends gcc libpq-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# # Add and make the wait-for-it.sh script executable
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
RUN chmod -R 775 /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose application port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]