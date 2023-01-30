# Chat on Socket.io
> ### This is a simple chat API that allows you to send and receive messages.
> The project is also deployed on Kubernetes using Helm. 
> The CI/CD is done using GitHub Actions and container images are stored on Docker Hub.

## Features
- Send and receive messages
- Create and delete rooms, join and leave rooms
- Authentication using JWT tokens
- Unit tests
- Code style
- Linting
- Type checking
- Formatting
- Security checks
- Dependency checks
- Static analysis

## Run locally
1. Clone the repository
2. Run `poetry install`
3. Run `uvicorn app:create_app --reload`
4. Go to `http://localhost:8000/docs` to see the API documentation
5. Go to `http://localhost:8000/redoc` to see the API documentation
6. Go to `http://localhost:8000/socket.io` to the testing the socket connection

## Run with Docker Compose
1. Clone the repository
2. Run `docker-compose up -d --build`
3. Go to `http://localhost:8000/docs` to see the API documentation
4. Go to `http://localhost:8000/socket.io` to the testing the socket connection

## Run with Docker
1. Clone the repository
2. Run `docker build -t chat -f docker/api/Dockerfile .`
3. Run `docker run -p 8000:8000 chat`
4. Go to `http://localhost:8000/docs` to see the API documentation
5. Go to `http://localhost:8000/socket.io` to the testing the socket connection

[//]: # (TODO: Add more information about the project)
[//]: # (TODO: Add Kubernetes deployment and CI/CD)
