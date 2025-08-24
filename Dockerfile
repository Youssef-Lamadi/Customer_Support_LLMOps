# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim
# Set working directory inside container
WORKDIR /app

COPY . /app

# Install system dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]