FROM python:3.11-slim

WORKDIR /app

# System deps for scikit-learn / pandas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-run.txt .
RUN pip install --no-cache-dir -r requirements-run.txt

COPY . .

# Train model if pickle is missing (dataset.csv is in the repo)
RUN python train_model.py

EXPOSE 8001

CMD ["sh", "-c", "gunicorn univast_ai.wsgi:application --bind 0.0.0.0:${PORT:-8001} --workers 2"]
