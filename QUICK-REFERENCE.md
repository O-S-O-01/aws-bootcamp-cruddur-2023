# Quick Reference Guide

This document contains quick commands and setup instructions for common tasks.

---

## 🚀 Starting the Application

### In Gitpod
```bash
# Environment is automatically configured
docker-compose up -d
```

### On Desktop
```bash
# First time only
cp .env.local .env
# Edit .env and add your API keys

# Every time
docker-compose up -d
```

---

## 🛑 Stopping the Application

```bash
docker-compose down
```

---

## 📊 Viewing Services

```bash
# See all running services
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend-flask
docker-compose logs -f frontend-react-js
docker-compose logs -f xray-daemon
```

---

## 🔄 Restarting Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend-flask

# Rebuild and restart
docker-compose up -d --build
```

---

## 🌐 Access URLs

### Gitpod
- Frontend: `https://3000--${GITPOD_ENVIRONMENT_ID}.eu-central-1-01.gitpod.dev`
- Backend: `https://4567--${GITPOD_ENVIRONMENT_ID}.eu-central-1-01.gitpod.dev`

Check ports panel in Gitpod for exact URLs.

### Desktop
- Frontend: http://localhost:3000
- Backend: http://localhost:4567

---

## 🔧 Environment Configuration

### Switching Environments

**For Gitpod:**
```bash
cp .env.gitpod .env
docker-compose restart
```

**For Local:**
```bash
cp .env.local .env
docker-compose restart
```

### Environment Files
- `.env` - Active configuration (not in git)
- `.env.gitpod` - Gitpod template (in git)
- `.env.local` - Local template (in git)

---

## 🔍 AWS X-Ray Setup

### Install AWS CLI (First Time in Gitpod)
```bash
cd /workspace
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
cd $THEIA_WORKSPACE_ROOT
```

### Configure AWS Credentials
```bash
aws configure
# Enter AWS Access Key ID
# Enter AWS Secret Access Key
# Enter region: ca-central-1
# Enter output format: json
```

### Verify AWS Setup
```bash
aws sts get-caller-identity
```

### Check X-Ray Daemon
```bash
docker-compose logs xray-daemon --tail 20
```

### Alternative: Use Gitpod Environment Variables
1. Go to: https://gitpod.io/user/variables
2. Add:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION` = `ca-central-1`
3. Scope: `O-S-O-01/aws-bootcamp-cruddur-2023`
4. Restart Gitpod

---

## 🐛 Troubleshooting

### Permission Denied (Gitpod)
```bash
sudo chmod 666 /var/run/docker.sock
```

### Services Won't Start
```bash
# Check Docker is running
docker ps

# Check for errors
docker-compose logs

# Rebuild everything
docker-compose down
docker-compose up -d --build
```

### Frontend Can't Connect to Backend
```bash
# Check .env file has correct URLs
cat .env | grep URL

# Verify backend is running
docker-compose ps | grep backend

# Check backend logs
docker-compose logs backend-flask
```

### X-Ray Credential Errors
```bash
# Verify AWS credentials
aws sts get-caller-identity

# If not configured
aws configure

# Restart services
docker-compose restart xray-daemon
```

---

## 📦 Git Operations

### View Changes
```bash
git status
git diff
```

### Commit Changes
```bash
git add <files>
git commit -m "Your message

Co-authored-by: Ona <no-reply@ona.com>"
git push origin main
```

### Pull Latest Changes
```bash
git pull origin main
```

---

## 🔒 Security Reminders

- ✅ `.env` is in `.gitignore` (never commit it)
- ✅ Use `.env.gitpod` and `.env.local` as templates
- ✅ Never commit real API keys or AWS credentials
- ✅ Use Gitpod environment variables for sensitive data

---

## 📚 Documentation

- **Detailed Setup**: See [SETUP.md](SETUP.md)
- **Full README**: See [README.md](README.md)
- **AWS X-Ray Console**: https://console.aws.amazon.com/xray
- **Honeycomb Console**: https://ui.honeycomb.io

---

## 🎯 Common Workflows

### Starting Work (Gitpod)
```bash
# 1. Open Gitpod (environment auto-configures)
# 2. Start services
docker-compose up -d
# 3. Check services are running
docker-compose ps
# 4. Start coding!
```

### Starting Work (Desktop)
```bash
# 1. Navigate to project
cd aws-bootcamp-cruddur-2023
# 2. Start services
docker-compose up -d
# 3. Open browser to localhost:3000
```

### Ending Work
```bash
# Stop services (optional but recommended)
docker-compose down
```

### After Pulling Changes
```bash
git pull origin main
docker-compose restart
```

---

## 🆘 Getting Help

1. Check this quick reference
2. Check [SETUP.md](SETUP.md) for detailed guides
3. Check [README.md](README.md) for architecture info
4. Check service logs: `docker-compose logs <service-name>`
5. Ask Ona Agent for help!

---

## 📝 Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | React application |
| Backend | 4567 | Flask API |
| PostgreSQL | 5432 | Database |
| DynamoDB | 8000 | Local DynamoDB |
| X-Ray | 2000 | Tracing daemon |

---

## 🔑 Important Environment Variables

| Variable | Purpose | Gitpod | Local |
|----------|---------|--------|-------|
| `FRONTEND_URL` | Frontend location | Gitpod URL | `http://localhost:3000` |
| `BACKEND_URL` | Backend location | Gitpod URL | `http://localhost:4567` |
| `REACT_APP_BACKEND_URL` | Backend for React | Gitpod URL | `http://localhost:4567` |
| `HONEYCOMB_API_KEY` | Observability | Your key | Your key |
| `AWS_ACCESS_KEY_ID` | AWS credentials | Your key | Your key |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials | Your secret | Your secret |

---

Last Updated: 2025-11-30
