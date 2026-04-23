#  Job Processing System - DevOps Stage 2

## Prerequisites

- Docker Desktop (v24+)
- Docker Compose (v2+)
- Git
- 4GB RAM minimum


## Quick Start

1. **Clone the repository:**
```bash
   git clone https://github.com/YOUR-USERNAME/hng14-stage2-devops
   cd hng14-stage2-devops
```

2. **Copy environment variables:**
```bash
   cp .env.example .env
   # Edit .env with your values if needed
```

3. **Start the stack:**
```bash
   docker compose up --build
```

4. **Verify it's running:**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Health: http://localhost:8000/health


## What Success Looks Like

```bash
   docker compose ps

```
- all services will be healthy and available



