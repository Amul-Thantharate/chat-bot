FROM python:latest

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY .env /app

COPY requirements.txt /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8051

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
