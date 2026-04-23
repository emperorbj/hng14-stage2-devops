FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends  procps && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

HEALTHCHECK CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]