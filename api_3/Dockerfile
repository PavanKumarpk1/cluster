FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FIX: Copy products.json right alongside main.py if it's in the repo
# If it's inside a separate folder, change this path to: COPY products/products.json ./products.json
COPY products.json ./products.json
RUN chmod 666 products.json

EXPOSE 8003

CMD ["python", "main.py"]
