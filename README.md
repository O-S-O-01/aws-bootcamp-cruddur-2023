# FREE AWS Cloud Project Bootcamp

![](https://codebuild.ca-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidzQ5bVBva0pyU1lDODd1Uy96dXFxelNnTEh0dHFXUXNRR3hLT2RzRmVOaTZ5T3ZadHpSS29CazZ2SHBYckc0VXJEWEI2NFBKalMwcWM4RHh1Tk02b3RnPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZTSzAxY2NiTU4rMmJJVGsiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)

- Application: Cruddur
- Cohort: 2023-A1

This is the codebase for the FREE AWS Cloud Project Bootcamp 2023. This repository has been configured to work seamlessly in both **Gitpod** (cloud development environment) and **local desktop environments**.

![Cruddur Graphic](_docs/assets/cruddur-banner.jpg)

![Cruddur Screenshot](_docs/assets/cruddur-screenshot.png)

---

## 🚀 Quick Start

### Running in Gitpod (Recommended for Beginners)

1. **Open in Gitpod**: Click the Gitpod button or open this repository in Gitpod
2. **Wait for setup**: The environment will automatically configure itself
3. **Start the application**:
   ```bash
   docker-compose up -d
   ```
4. **Access the app**: Gitpod will provide URLs for:
   - Frontend: `https://3000--<your-environment-id>.gitpod.dev`
   - Backend API: `https://4567--<your-environment-id>.gitpod.dev`

### Running Locally (Desktop/Laptop)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/aws-bootcamp-cruddur-2023.git
   cd aws-bootcamp-cruddur-2023
   ```

2. **Copy local environment configuration**:
   ```bash
   cp .env.local .env
   ```

3. **Start the application**:
   ```bash
   docker-compose up -d
   ```

4. **Access the app**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:4567

---

## Recent Configuration Changes

This repository has been updated to work in both Gitpod and local environments. Here's what changed and why:

### 1. Environment Variable System

**What Changed:**
- Created `.env.gitpod` - Configuration template for Gitpod
- Created `.env.local` - Configuration template for local development
- Updated `docker-compose.yml` to use environment variables instead of hardcoded values

**Why This Matters:**
The original configuration used Gitpod Classic variables (`GITPOD_WORKSPACE_ID`, `GITPOD_WORKSPACE_CLUSTER_HOST`) that don't exist in the new Gitpod. The new system uses:
- `GITPOD_ENVIRONMENT_ID` for Gitpod
- `localhost` for local development

**How It Works:**
```yaml
# Old way (hardcoded):
FRONTEND_URL="https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"

# New way (flexible):
FRONTEND_URL=${FRONTEND_URL}
```

The actual URL is now defined in your `.env` file, which you copy from either `.env.gitpod` or `.env.local` depending on where you're running.

---

### How Services Communicate

---

## 📂 Project Structure

```
aws-bootcamp-cruddur-2023/
├── backend-flask/           # Python Flask API
│   ├── app.py              # Main application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container configuration
│   └── services/           # Business logic modules
├── frontend-react-js/       # React frontend
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container configuration
 docker-compose.yml       # Multi-container orchestration
├── .env.gitpod             # Gitpod environment template
├── .env.local              # Local environment template
├── .env                    # Active configuration (not in git)
├── .gitignore              # Git ignore rules
├── SETUP.md                # Detailed setup instructions
├── README.md               # This file
└── journal/                # Weekly homework documentation
```

---



---

## 📋 Journaling Homework

The `/original bootcamp journal` directory contains weekly homework documentation:

- [ ] [Week 0](journal/week00.md)
- [ ] [Week 1](journal/week01.md)
- [ ] [Week 2](journal/week02.md)
- [ ] [Week 3](journal/week03.md)
- [ ] [Week 4](journal/week04.md)
- [ ] [Week 5](journal/week05.md)
- [ ] [Week 6](journal/week06.md)
- [ ] [Week 7](journal/week07.md)
- [ ] [Week 8](journal/week08.md)
- [ ] [Week 9](journal/week09.md)
- [ ] [Week 10](journal/week10.md)
- [ ] [Week 11](journal/week11.md)
- [ ] [Week 12](journal/week12.md)
- [ ] [Week 13](journal/week13.md)

---

## 📞 Getting Help

If you encounter issues:

1. Check [SETUP.md](SETUP.md) for detailed troubleshooting
2. Review the error messages in `docker-compose logs`
3. Verify your `.env` file matches your environment
4. Check that all services are running with `docker-compose ps`

---

## 📄 License

This project is part of the FREE AWS Cloud Project Bootcamp 2023.
