FROM python:3.12.2-alpine
LABEL authors="syankovsky,irudenko"

ENV PYTHONUNBUFFERED 1

RUN addgroup --system app && adduser --system --group app;

USER app

WORKDIR /app

COPY requirements-dev.txt .
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt;

COPY . .

ENTRYPOINT ["python"]