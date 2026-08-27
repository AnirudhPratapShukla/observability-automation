
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

ENV ES_HOST=http://host.docker.internal:9200
ENV ES_INDEX=service-status

CMD ["python", "app.py"]

