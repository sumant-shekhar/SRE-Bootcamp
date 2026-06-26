# Build stage
FROM python:3.14.6-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.14.6-slim-bookworm AS runtime

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 4000

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
