# Cruddur Setup Guide

This guide explains how to run the Cruddur application in different environments.

## Environment Configuration

The application uses environment variables to configure URLs for different environments. We provide two configuration files:

- `.env.gitpod` - For running in Gitpod
- `.env.local` - For running on your local desktop/laptop

## Running in Gitpod

The `.env` file is already configured for Gitpod. Just run:

```bash
docker-compose up -d
```

Access the application:
- Frontend: `https://3000--<ENVIRONMENT_ID>.eu-central-1-01.gitpod.dev`
- Backend API: `https://4567--<ENVIRONMENT_ID>.eu-central-1-01.gitpod.dev`

The ports will be automatically opened and URLs will be available in the Ports panel.

## Running Locally (Desktop/Laptop)

1. Copy the local environment configuration:
   ```bash
   cp .env.local .env
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:4567

## Switching Between Environments

To switch from Gitpod to local or vice versa:

```bash
# For Gitpod
cp .env.gitpod .env
docker-compose restart

# For Local
cp .env.local .env
docker-compose restart
```

## Services

The application runs the following services:

- **backend-flask** (Port 4567) - Python Flask API
- **frontend-react-js** (Port 3000) - React frontend
- **db** (Port 5432) - PostgreSQL database
- **dynamodb-local** (Port 8000) - Local DynamoDB
- **xray-daemon** (Port 2000) - AWS X-Ray daemon

## Useful Commands

```bash
# View running services
docker-compose ps

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend-flask

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Stop and remove volumes (clean slate)
docker-compose down -v
```

## Environment Variables

The following environment variables are used:

| Variable | Description | Gitpod Value | Local Value |
|----------|-------------|--------------|-------------|
| `FRONTEND_URL` | Frontend URL | `https://3000--${GITPOD_ENVIRONMENT_ID}...` | `http://localhost:3000` |
| `BACKEND_URL` | Backend URL | `https://4567--${GITPOD_ENVIRONMENT_ID}...` | `http://localhost:4567` |
| `REACT_APP_BACKEND_URL` | Backend URL for React | Same as BACKEND_URL | `http://localhost:4567` |
| `AWS_XRAY_URL` | X-Ray daemon URL | Gitpod URL pattern | `*localhost:4567*` |
| `HONEYCOMB_API_KEY` | Honeycomb API key | (from .env) | (from .env) |
| `HONEYCOMB_DATASET` | Honeycomb dataset | `cruddur` | `cruddur` |
| `SERVICE_NAME` | Service name | `backend-flask` | `backend-flask` |

## Troubleshooting

### Services won't start
- Check Docker is running: `docker ps`
- Check logs: `docker-compose logs`
- Try rebuilding: `docker-compose up -d --build`

### Frontend shows connection error
- Verify backend is running: `docker-compose ps`
- Check REACT_APP_BACKEND_URL matches your environment
- Verify .env file is correct for your environment

### Permission denied errors (Gitpod)
```bash
sudo chmod 666 /var/run/docker.sock
```

### Port already in use
```bash
# Find what's using the port
lsof -i :3000
lsof -i :4567

# Stop the conflicting service or change ports in docker-compose.yml
```

## Notes

- The `.env` file is tracked in git and configured for Gitpod by default
- `.env.local` and `.env.gitpod` are reference files
- Never commit sensitive API keys or credentials
- The `node_modules` volume prevents local files from overwriting container dependencies
