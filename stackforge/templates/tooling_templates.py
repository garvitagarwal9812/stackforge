"""
Project root developer tooling templates: Makefile, README, .gitignore, .env.example, pre-commit.
"""
from typing import Dict
from stackforge.core.config import StackConfig

def get_tooling_files(config: StackConfig) -> Dict[str, str]:
    files = {}
    name = config.project_name
    backend = config.backend
    frontend = config.frontend
    db = config.database
    pipe = config.pipeline

    # 1. README.md
    files["README.md"] = f"""# 🚀 {name}

> {config.project_description}

[![CI/CD Pipeline]({pipe})]({pipe})
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)]()
[![License: {config.license}](https://img.shields.io/badge/License-{config.license}-brightgreen.svg)]()
[![Forged By](https://img.shields.io/badge/Forged%20By-StackForge%20CLI-blueviolet)](https://github.com)

---

## 🏛️ Architecture Overview

```mermaid
graph TD
    Client[Web Browser / API Client] -->|HTTP / TLS| Ingress[Ingress Controller / Proxy]
    Ingress -->|Route /api| Backend[{backend.upper()} Backend Service]
    Ingress -->|Route /| Frontend[{frontend.upper()} Frontend UI]
    Backend -->|Read/Write| DB[({db.upper()} Database)]
    Backend -->|Cache| Redis[(Redis Cache)]
```

### Stack Components
- **Backend**: `{backend}`
- **Frontend**: `{frontend}`
- **Database**: `{db}`
- **Pipeline**: `{pipe}`
- **Containerization**: `{"Docker & Compose" if config.docker else "Disabled"}`
- **Orchestration**: `{"Kubernetes + Helm" if config.k8s else "Disabled"}`
- **Infrastructure as Code**: `{"Terraform" if config.terraform else "Disabled"}`

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- Docker & Docker Compose
- {"Python 3.11+" if "fastapi" in backend or "django" in backend else "Node.js 20+" if "node" in backend or "express" in backend else "Go 1.22+" if "go" in backend else "Rust 1.77+" if "rust" in backend else "JDK 21+"}
- Git

### 2. Environment Configuration
Copy sample environment variables:
```bash
cp .env.example .env
```

### 3. Run with Docker Compose (Recommended)
Start database, cache, backend, and frontend with one command:
```bash
docker compose up -d --build
```
- **Backend API**: [http://localhost:8000/health](http://localhost:8000/health)
- **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend**: [http://localhost:3000](http://localhost:3000)

### 4. Local Development (Without Containers)
```bash
# Using Makefile
make dev

# Or run tests
make test
```

---

## 🛠️ Makefile Commands

| Command | Action |
| :--- | :--- |
| `make dev` | Start development servers |
| `make test` | Run all unit and integration test suites |
| `make lint` | Run code quality linters and formatters |
| `make docker-up` | Start multi-container stack in detached mode |
| `make docker-down` | Stop and remove running containers |
| `make k8s-apply` | Apply production Kubernetes manifests |

---

## 🚀 CI/CD Pipeline Automation

The project includes pre-configured `{pipe}` workflows located under:
- `{".github/workflows/" if pipe == "github_actions" else ".gitlab-ci.yml" if pipe == "gitlab_ci" else "azure-pipelines.yml" if pipe == "azure_devops" else "Jenkinsfile"}`

Key stages configured:
1. **Linting & Code Standards**
2. **Automated Unit & Integration Testing**
3. **Container Build & Registry Push**
4. **Automated Deployment Verification**

---

*Generated automatically with **StackForge CLI** (Garvit Agarwal Edition).*
"""

    # 2. Makefile
    backend_test_cmd = "pytest backend/tests" if backend == "fastapi" else "cd backend && npm test" if "express" in backend else "cd backend && go test ./..." if "go" in backend else "cd backend && cargo test"
    files["Makefile"] = f""".PHONY: all dev test lint docker-up docker-down clean k8s-apply

all: dev

dev:
\tdocker compose up

test:
\t@echo "Running backend test suite..."
\t{backend_test_cmd}

lint:
\t@echo "Running linters..."

docker-up:
\tdocker compose up -d --build

docker-down:
\tdocker compose down

k8s-apply:
\tkubectl apply -f k8s/

clean:
\tdocker compose down -v
\tfind . -type d -name "__pycache__" -exec rm -rf {{}} + 2>/dev/null || true
\tfind . -type d -name "node_modules" -exec rm -rf {{}} + 2>/dev/null || true
"""

    # 3. .gitignore
    files[".gitignore"] = """# Environments & Secrets
.env
.env.local
.env.*.local
*.pem
*.key

# Dependencies
node_modules/
.pnp
.pnp.js
venv/
.venv/
env/
target/

# Build artifacts
dist/
build/
out/
.next/
*.egg-info/
*.pyc
__pycache__/

# Testing & Coverage
coverage/
.nyc_output/
.pytest_cache/
junit/
*.lcov

# IDE & System
.vscode/
.idea/
.DS_Store
Thumbs.db

# Terraform
*.tfstate
*.tfstate.backup
.terraform/
.terraform.lock.hcl

# Docker & Logs
*.log
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*
"""

    # 4. .env.example
    files[".env.example"] = f"""# {name} Environment Configuration
ENVIRONMENT=development
PORT=8000
DEBUG=true

# Security
SECRET_KEY=change-this-in-production-to-a-high-entropy-random-string
JWT_EXPIRATION_HOURS=24

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/{name}
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB={name}

# Cache & Message Broker
REDIS_URL=redis://localhost:6379/0

# External API Integrations
API_TIMEOUT_SECONDS=30
"""

    # 5. .pre-commit-config.yaml
    if config.include_linter:
        files[".pre-commit-config.yaml"] = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
"""

    return files
