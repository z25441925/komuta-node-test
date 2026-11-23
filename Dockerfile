FROM python:3.12-slim
WORKDIR /app
COPY app.py .
EXPOSE 8080 9000
CMD ["python", "app.py"]
