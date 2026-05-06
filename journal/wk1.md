# Week 1 — App Containerization

## Task Overview
The primary focus of this week was to containerize the Cruddur application's microservices. This involved migrating the backend (Flask) and frontend (React) into Docker containers, ensuring they could communicate via Docker Compose, and integrating local development databases (PostgreSQL and DynamoDB) to avoid unnecessary AWS costs.

## GENERAL TASKS COMPLETED

- [x]***Containerized Backend:*** Created a `Dockerfile` at `backend-flask/Dockerfile` for the Flask application and successfully built the image, using 

```dockerfile
    FROM python:3.10-slim-bookworm

    WORKDIR /backend-flask

    COPY requirements.txt requirements.txt
    RUN pip3 install -r requirements.txt

    COPY . .

    ENV FLASK_ENV=development

    EXPOSE ${PORT}
    CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
``` 
and run the container
- [x] ***Containerized Frontend:*** Created a `Dockerfile` at `frontend-react-js/Dockerfile` using 
```dockerfile
FROM node:22-alpine

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```
 for the React application, ensuring `npm install` was handled correctly before and within the build process.

- [x] ***Orchestrated Microservices:*** Developed a `docker-compose.yml` file at the project root file to manage the multi-container setup, including the frontend, backend, and internal networking.
- [x] ***Local Database Integration:*** Added **Postgres** and **DynamoDB Local** to the Docker Compose configuration to allow for local data persistence and offline development.
- [x] ***Verified Connectivity:*** Successfully used `curl` and browser testing to verify that the backend API was returning JSON data at the `/api/activities/home` endpoint.using 
```sh
curl -X GET http://localhost:4567/api/activities/home -H "Accept: application/json" -H "Content-Type: application/json"
```
- [x] ***Image Management:*** Practiced Docker CLI commands for building, running, stopping, and removing containers, as well as gaining shell access to running containers for debugging.

## TECHNICAL CHALLENGES AND PERSONAL SOLUTIONS

### Challenge 1: Python Dependency Conflicts in WSL
While installing backend dependencies locally, I encountered "Externally Managed Environment" errors. Modern Linux distributions restrict global `pip` installs to protect system stability.
- **My Solution:** I utilized the `--break-system-packages` flag. While I am aware that Virtual Environments (venv) are the best practice, I chose this route for immediate simplicity and to align my local environment quickly with the container’s behavior.

### Challenge 2: Outdated Base Images & Security Vulnerabilities
The original bootcamp utilized `python:3.10-slim-buster` and `node:16.18`, both of which are outdated and contain known security vulnerabilities.
- **My Solution (Backend):** I upgraded the base image to `python:3.10-slim-bookworm`. This move to Debian 12 provides a more secure and modern foundation for the Python environment.
- **My Solution (Frontend):** I upgraded the frontend image from Node 16 to `node:22-alpine`. This not only addressed security concerns but also leveraged the Alpine distribution to significantly reduce the image footprint.

### Challenge 3: Container Security Best Practices
I recognized that "just making it work" isn't enough for a production-grade portfolio project.
- **My Solution:** I researched and implemented container security fundamentals, including using specific version tags instead of `latest`, ensuring `.env` files are excluded from images, and understanding the importance of minimizing the attack surface of my containers.

### Challenge 4: Networking and Connectivity
Getting containers to talk to each other while also being accessible from the WSL host required a clear understanding of Docker networking and port mapping.
- **My Solution:** I configured the `docker-compose.yml` with specific port mappings (`4567` for backend, `3000` for frontend) and used environment variables to ensure the React frontend could correctly reference the Flask API URL.
### Challenge 5: I WAS NOT USING GITPOD/ONA 
Since I decided to build in a local environment rather than using Gitpod, I switched to using Docker Desktop on my personal machine. However, I started experiencing performance issues, VS Code would freeze and occasionally crash due to high resource usage and limited storage space.
- **My Solution:** To resolve this, I reconfigured Docker Desktop to use an external hard drive for its storage. This helped free up space on my system and significantly improved overall performance and stability.