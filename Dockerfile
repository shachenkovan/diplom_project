FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY config /app/config

COPY . .

CMD ["python", "main.py"]