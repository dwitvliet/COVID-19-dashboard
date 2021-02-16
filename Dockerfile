FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install flask gunicorn
RUN pip install -r requirements.txt
COPY . .
ENV PORT 8080
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 flask_app:app

