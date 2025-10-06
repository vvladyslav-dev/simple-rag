FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy the project (will be overridden by volume mount in docker-compose)
COPY . /app

CMD ["streamlit", "run", "app/app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.runOnSave", "true"]

