FROM python:3.11-slim
COPY ./app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
