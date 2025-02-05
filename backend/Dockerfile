# Select 'python:3.11-slim' as base image to provide lightweight python environment.
FROM python:3.11-slim

# Create the working dir inside Docker container named "backend".
# This is necessary since 'app' dir is part of python dir path.
WORKDIR /backend

RUN mkdir -p /backend/app/

# Copy contents! of local /app dir into /backend/app dir.
COPY ./app /backend/app

# Copy in path 'requirements.txt' into working dir of Docker container.
COPY requirements.txt /backend

# Install required dependencies in container environment.
RUN pip install -r requirements.txt

# Expose port on which Docker container will listen.
# This is imortant since the API will run on this port.
EXPOSE 1111

# Start FastAPI API service. Run service on local host on port 1111.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0",  "--port", "1111"]

# Build Docker container:
# -t: to tag the container (name the container):
# fastapi-app: Name of the tag.
# . : Reads the Dockerfile of the current dir path.
# docker build -t fastapi-app .

# Run Docker container:
# -p: Flag to specify port which will be binded to exposed Docker port.
# 1111:1111: Bind local port to exposed Docker port.
# fastapi-app: Name of docker image.
# docker run -p 1111:1111 fastapi-app
