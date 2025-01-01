# FLASK API DOCKER FILE

FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    DATABASE_URL=postgresql://neondb_owner:y85gResQXJtc@ep-lively-sun-a5i0suhp-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require 
    # use secrets later

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser



EXPOSE 5000

CMD ["python", "app.py"]