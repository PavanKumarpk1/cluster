FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the products JSON database file directly into the workdir
COPY products.json ./products.json

# Ensure the database file has read/write permissions for TinyDB
RUN chmod 666 products.json

EXPOSE 8003

# Run the app
CMD ["python", "main.py"]
