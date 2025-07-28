FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

COPY . .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]