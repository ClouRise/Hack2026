FROM python:3.13-slim

WORKDIR /app

# Установка сертификатов и сетевых утилит
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    netcat-openbsd \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Настройка pip
ENV PIP_DEFAULT_TIMEOUT=300 \
    PIP_RETRIES=10 \
    PIP_NO_CACHE_DIR=1 \
    PIP_TRUSTED_HOST="pypi.org files.pythonhosted.org"

# Копируем requirements
COPY requirements.txt .

# Установка с обработкой ошибок
RUN pip install --upgrade pip && \
    (pip install -r requirements.txt || \
     pip install -r requirements.txt --index-url https://pypi.org/simple/ --timeout 300 || \
     echo "Installing without SSL..." && \
     pip install -r requirements.txt --index-url http://pypi.org/simple/ --trusted-host pypi.org)

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]