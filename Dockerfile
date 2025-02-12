# Use an official Python runtime as a parent image
FROM python:3.13.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Flask
RUN pip install Flask

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application
CMD ["python", "app.py"]
