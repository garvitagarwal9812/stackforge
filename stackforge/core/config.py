"""
Configuration models and stack definitions for StackForge CLI.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json
import os

BACKENDS = {
    "fastapi": {
        "name": "FastAPI (Python)",
        "description": "High-performance async Python API with Pydantic v2 & OpenAPI docs",
        "lang": "python",
        "default_port": 8000,
        "default_test": "pytest",
    },
    "express_ts": {
        "name": "Express.js (TypeScript)",
        "description": "Standard modern Node.js backend with TypeScript, Zod validation & Jest",
        "lang": "typescript",
        "default_port": 5000,
        "default_test": "jest",
    },
    "nestjs": {
        "name": "NestJS (TypeScript)",
        "description": "Enterprise-grade scalable architectural framework with dependency injection",
        "lang": "typescript",
        "default_port": 3000,
        "default_test": "jest",
    },
    "go_gin": {
        "name": "Go (Gin Gonic)",
        "description": "Blazing fast minimalist REST framework written in Go with GORM support",
        "lang": "go",
        "default_port": 8080,
        "default_test": "go test",
    },
    "rust_axum": {
        "name": "Rust (Axum)",
        "description": "Ultra-safe, zero-cost abstraction asynchronous web framework built on Tokio",
        "lang": "rust",
        "default_port": 8080,
        "default_test": "cargo test",
    },
    "django": {
        "name": "Django REST Framework (Python)",
        "description": "Batteries-included web framework with powerful ORM & admin interface",
        "lang": "python",
        "default_port": 8000,
        "default_test": "pytest-django",
    },
    "spring_boot": {
        "name": "Spring Boot (Java 21)",
        "description": "Battle-tested enterprise Java framework with Maven & JPA/Hibernate",
        "lang": "java",
        "default_port": 8080,
        "default_test": "mvn test",
    },
    "none": {
        "name": "None (Frontend Only / Fullstack Next.js)",
        "description": "No standalone backend; frontend handles API routes or is static",
        "lang": "none",
        "default_port": 0,
        "default_test": "",
    },
}

FRONTENDS = {
    "react_vite": {
        "name": "React 18 + Vite (TypeScript)",
        "description": "Lightning-fast modern React SPA with Vite, TailwindCSS & Axios",
        "lang": "typescript",
        "default_port": 5173,
    },
    "nextjs": {
        "name": "Next.js 14/15 (App Router)",
        "description": "Fullstack React framework with SSR, Server Components & SEO optimization",
        "lang": "typescript",
        "default_port": 3000,
    },
    "vue_vite": {
        "name": "Vue 3 + Vite (TypeScript)",
        "description": "Modern Composition API with Pinia state management & Vite tooling",
        "lang": "typescript",
        "default_port": 5173,
    },
    "sveltekit": {
        "name": "SvelteKit 2 (TypeScript)",
        "description": "Cybernetically enhanced web apps with minimal boilerplate and tiny bundle size",
        "lang": "typescript",
        "default_port": 5173,
    },
    "none": {
        "name": "None (Headless API / Microservice)",
        "description": "No frontend user interface; backend service only",
        "lang": "none",
        "default_port": 0,
    },
}

DATABASES = {
    "postgresql": {
        "name": "PostgreSQL 16",
        "description": "Robust relational database with ORM schemas and migration scripts",
        "port": 5432,
    },
    "mongodb": {
        "name": "MongoDB 7.0",
        "description": "Document-oriented NoSQL database for flexible schema designs",
        "port": 27017,
    },
    "redis": {
        "name": "Redis 7.2 (Caching & Queues)",
        "description": "In-memory key-value store for caching, session management and task queues",
        "port": 6379,
    },
    "sqlite": {
        "name": "SQLite 3",
        "description": "Zero-configuration serverless embedded database, ideal for prototypes",
        "port": 0,
    },
    "mysql": {
        "name": "MySQL 8.0",
        "description": "Industry-standard open-source relational database",
        "port": 3306,
    },
    "none": {
        "name": "None (Stateless Service)",
        "description": "No local database container configured",
        "port": 0,
    },
}

PIPELINES = {
    "github_actions": {
        "name": "GitHub Actions",
        "description": "Multi-stage CI/CD: Linting, Unit Testing, Docker build & push, K8s deploy, CodeQL",
        "files": [".github/workflows/ci.yml", ".github/workflows/cd.yml", ".github/workflows/security.yml"],
    },
    "gitlab_ci": {
        "name": "GitLab CI/CD",
        "description": "GitLab multi-stage pipeline (.gitlab-ci.yml) with artifact caching and registry push",
        "files": [".gitlab-ci.yml"],
    },
    "azure_devops": {
        "name": "Azure Pipelines",
        "description": "Azure DevOps pipeline definition (azure-pipelines.yml) with agent pool integration",
        "files": ["azure-pipelines.yml"],
    },
    "jenkins": {
        "name": "Jenkinsfile",
        "description": "Declarative multi-branch Jenkinsfile pipeline with Docker agents & stage gates",
        "files": ["Jenkinsfile"],
    },
    "circleci": {
        "name": "CircleCI",
        "description": "CircleCI 2.1 pipeline with official orbs and parallel test runners",
        "files": [".circleci/config.yml"],
    },
}

@dataclass
class StackConfig:
    project_name: str = "my-awesome-stack"
    project_description: str = "Production-ready service generated with StackForge"
    author: str = "Garvit Agarwal"
    license: str = "MIT"
    backend: str = "fastapi"
    frontend: str = "react_vite"
    database: str = "postgresql"
    pipeline: str = "github_actions"
    docker: bool = True
    k8s: bool = True
    helm: bool = True
    terraform: bool = False
    monitoring: bool = True
    include_tests: bool = True
    include_linter: bool = True
    output_dir: str = "./my-awesome-stack"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StackConfig":
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)

    def save_to_file(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> "StackConfig":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
