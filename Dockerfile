# Use slim python 3.9 as base.
FROM python:3.9-slim

# Install deployment requirements.
RUN pip install flask gunicorn

# Install script requirements.
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all files.
COPY . .

# Setup deployment with gunicorn.
ENV PORT 8080
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 flask_app:app
