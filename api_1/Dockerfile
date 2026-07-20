FROM python:3.9-slim
RUN pip install flask flask-cors prometheus-flask-exporter
COPY app.py .
EXPOSE 8001
CMD ["python", "app.py"]
