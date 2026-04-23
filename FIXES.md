# HNG14 Stage 2 DevOps - Complete Bugs & Bad Practices Analysis

## Initial Fixes Applied
1.  Pulled Redis Docker image and ran container before API calls
2.  Installed all package dependencies for main.py, worker.py, and app.js

---

# CRITICAL ISSUES

## 1. Missing Containerization
**Location:** Root directory  
**Issue:** No Dockerfiles, no docker-compose.yml  
**Details:**
- Each of those services like frontend,api and worker directories do not have a Dockerfile
- There is no docker compose file for multiple container build

**Required Files:**
```
api/Dockerfile
frontend/Dockerfile
worker/Dockerfile
docker-compose.yml (root)
.dockerignore (each service)
```

---

## 2. Redis Connection Not Using Credentials and hardcoded values
**File:** `api/main.py:8` and `worker/worker.py:5`
**Current Code:**
```python
r = redis.Redis(host="localhost", port=6379)
```
**Problem:**
- `.env` defines `REDIS_PASSWORD=<example>` but it's never used
- The password authentication disabled
- The env variables not loaded at all
- The port is hardcoded


**Fix:**
  - import dotenv,initiate it and use it load env variables
---

## 3. Hardcoded Frontend Url
**File:** `frontend/app.js:5`
**Current Code:**
```javascript
const API_URL = "http://localhost:8000";
```
**Problem:**
- Hardcoded to localhost
- Won't work in containerized environment

**Fix:**
```javascript
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
```

---

## 4. We are committing secrets to Git 
**File:** `api/.env`
**Content:**
```
REDIS_PASSWORD=<set-in-your-env-not-in-git>
APP_ENV=production
```
**Problem:**
- Credentials exposed to everyone with repo access

**Fix:**
 - Added .gitignore to both worker and api project


---

# HIGH PRIORITY ISSUES

## 5. No Error Handling & Logging
**Files:** All services
**Problems:**
- `api/main.py`: No try-catch blocks
- `frontend/app.js`: Errors logged are too generic



**Fix:**
 - Add error handling and logging to all endpoints across all the services
 - Add try-catch blocks to where endpoints are


---

## 6. No CORS Configuration
**File:** `api/main.py`  
**Problem:**
- Frontend (port 3000) cannot call API (port 8000)
- Browser blocks cross-origin requests
- Results in "Access-Control-Allow-Origin" errors

**Fix:**
 - We will ensure to add middlewares that handles the CORS

---

## 7. Missing Health Check Endpoints
**All Services Need This**  
**Problem:**
- Docker will not have a way to check for the services health

**Fix:**
 - Add a separate health check endpoints across the services


---

## 8. Hardcoded Redis Host in All Services [SEVERITY: HIGH]
**Files:** `api/main.py:8`, `worker/worker.py:5`  
**Problem:**
```python
r = redis.Redis(host="localhost", port=6379)
```
- In Docker, Redis is at service name `redis`, not `localhost`
- In production, Redis is at different hostname
- Not using environment variables

**Fix:** 
- import,load and apply dotenv to load env variables in the project

---

## 9. API Doesn't Bind to All Interfaces [SEVERITY: HIGH]
**File:** `api/main.py`  
**Problem:**
- When running with uvicorn, default binds only to localhost
- Docker environment won't expose API properly

**Fix - Startup Command:**
```bash
# Instead of: uvicorn main:app --reload
# Use:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 10. Python dotenv library was not added to requirements.txt
**File:** `api and worker`  
**Problem:**
- While building multiple containers they eventually failed because of a missing module python-dotenv

**Fix **
- I added the package in the requirements.txt for both api and worker services
- i cleared docker builder cache and rebuilt the containers again
```bash
docker compose down
docker builder prune -f
docker compose up --build --pull always
```

## 11. Wrong REACT_APP_API_URL config in frontend
**File:** `frontend directory`  
**Problem:**
- The current value localhost:8000 will point the frontend to its own container and look for port 8000 which will fail. Since that container has no port 8000

**Fix **
- Point the frontend to the api container api:8000. Because by docker compose use the service name as its hostname
```bash
from 
REACT_APP_API_URL=http://localhost:8000
into
REACT_APP_API_URL=http://api:8000
```


## 11. Linting errors in the python files
**File:** `api/main.py and worker/worker.py directory`  
**Problem:**
- All these files had linting errors some empty

**Fix **
- I had to add 2 blank spaces between route functions ensured cursor stays at next line of a code
```bash
from 
REACT_APP_API_URL=http://localhost:8000
into
REACT_APP_API_URL=http://api:8000