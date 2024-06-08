# Use the official Python 3.8 image from the Docker Hub
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt 

# Copy the Django project files
COPY . /app/

# Copy the SQL file into the container's initialization directory
# COPY oefhz.sql /docker-entrypoint-initdb.d/

EXPOSE 8000  

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]  

