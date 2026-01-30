# Use a lightweight Python base image
FROM python:3.11-slim

# Create application directory
WORKDIR /app

# Copy dependency list (if any)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into the container
COPY app/ app/

# Run the program; arguments are passed at runtime
ENTRYPOINT ["python", "app/cli.py"]
