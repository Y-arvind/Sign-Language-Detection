FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY . /app

CMD ["python","app.py"]