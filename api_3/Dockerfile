FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FIX: Expect products.json to be inside the relative directory we pass during context
COPY products.json ./products.json
RUN chmod 666 products.json

EXPOSE 8003

CMD ["python", "main.py"]
