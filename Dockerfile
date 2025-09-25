FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl build-essential g++ && \
    curl -Ls https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./

ENV PATH="/root/.local/bin/:$PATH"
RUN uv pip install --system .

COPY . .

RUN adduser --disabled-password --gecos "" appuser

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
