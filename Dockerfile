FROM python:3.9-slim
RUN pip install flask gunicorn
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
ENV PORT 8080
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:update_database
