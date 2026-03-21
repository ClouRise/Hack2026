FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && update-ca-certificates --fresh \
    && rm -rf /var/lib/apt/lists/*

# RUN pip install --upgrade pip && \
#     pip install cython && \
#     cythonize -i loop.pyx

ENV PIP_DEFAULT_TIMEOUT=300 \
    PIP_RETRIES=10 \
    PIP_NO_CACHE_DIR=1 \
    PIP_TRUSTED_HOST="pypi.org pypi.python.org files.pythonhosted.org"

COPY requirements.txt .


RUN pip install --upgrade pip && pip install requests && \
    pip install -r requirements.txt --timeout 300 --retries 10


RUN useradd -m back_user
USER back_user

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]