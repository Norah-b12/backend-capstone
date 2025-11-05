# Base image
FROM python:3.10

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /usr/src/backend

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose Django port
EXPOSE 8000

# Default command (we'll override in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
