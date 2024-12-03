FROM python:3.12.0-slim

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["python", "api_start.py"]
