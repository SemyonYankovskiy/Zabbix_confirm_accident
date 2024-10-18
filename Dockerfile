FROM python:3.12.3-alpine
LABEL authors="syankovsky,irudenko"

ENV PYTHONUNBUFFERED 1

RUN addgroup -S appgroup && adduser -S appuser -G appgroup;

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /app/outages && chown -R appuser:appgroup /app/outages;

USER appuser

ENTRYPOINT ["python"]