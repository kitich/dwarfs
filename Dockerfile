# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app
RUN mkdir /app/html

# Copy requirements.txt and install dependencies
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./app .

# Expose the port the app will run on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]