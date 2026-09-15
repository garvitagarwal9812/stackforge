"""
Curated industry-standard architecture presets for rapid scaffolding.
"""
from typing import Dict, Any

PRESETS: Dict[str, Dict[str, Any]] = {
    "fastapi-cloud": {
        "name": "FastAPI Cloud-Native Microservice",
        "description": "FastAPI (Python) + PostgreSQL + Redis Cache + Docker + Kubernetes + GitLab CI/CD",
        "tags": ["Python", "FastAPI", "Postgres", "Redis", "GitLab CI", "K8s", "Helm"],
        "config": {
            "backend": "fastapi",
            "frontend": "none",
            "database": "postgresql",
            "pipeline": "gitlab_ci",
            "docker": True,
            "k8s": True,
            "helm": True,
            "terraform": False,
            "monitoring": True,
            "include_tests": True,
            "include_linter": True,
        }
    },
    "mern-stack": {
        "name": "MERN Stack Enterprise",
        "description": "React (Vite/TS) + Express (TypeScript) + MongoDB + GitHub Actions + Docker",
        "tags": ["React", "Express", "TypeScript", "MongoDB", "GitHub Actions", "Docker"],
        "config": {
            "backend": "express_ts",
            "frontend": "react_vite",
            "database": "mongodb",
            "pipeline": "github_actions",
            "docker": True,
            "k8s": True,
            "helm": True,
            "terraform": False,
            "monitoring": True,
            "include_tests": True,
            "include_linter": True,
        }
    },
    "pern-stack": {
        "name": "PERN Modern Stack",
        "description": "React (Vite/TS) + Express (TypeScript) + PostgreSQL + GitHub Actions + Docker",
        "tags": ["React", "Express", "Postgres", "GitHub Actions", "Docker"],
        "config": {
            "backend": "express_ts",
            "frontend": "react_vite",
            "database": "postgresql",
            "pipeline": "github_actions",
            "docker": True,
            "k8s": True,
            "helm": True,
            "terraform": True,
            "monitoring": True,
            "include_tests": True,
            "include_linter": True,
        }
    },
    "go-high-throughput": {
        "name": "Go High-Throughput REST Engine",
        "description": "Go (Gin) + PostgreSQL + Docker + Kubernetes + Terraform + GitHub Actions",
        "tags": ["Go", "Gin", "Postgres", "Docker", "Terraform", "GitHub Actions"],
        "config": {
            "backend": "go_gin",
            "frontend": "none",
            "database": "postgresql",
            "pipeline": "github_actions",
            "docker": True,
            "k8s": True,
            "helm": True,
            "terraform": True,
            "monitoring": True,
            "include_tests": True,
            "include_linter": True,
        }
    },
    "rust-axum-service": {
        "name": "Rust High-Safety Microservice",
        "description": "Rust (Axum/Tokio) + PostgreSQL + Azure Pipelines + Docker + K8s",
        "tags": ["Rust", "Axum", "Tokio", "Postgres", "Azure DevOps", "Docker"],
        "config": {
            "backend": "rust_axum",
            "frontend": "none",
            "database": "postgresql",
            "pipeline": "azure_devops",
            "docker": True,
            "k8s": True,
            "helm": True,
            "terraform": False,
            "monitoring": True,
            "include_tests": True,
            "include_linter": True,
        }
    },
    "nextjs-enterprise": {
        "name": "Next.js Fullstack Cloud App",
        "description": "Next.js 14/15 App Router + PostgreSQL + Prisma + GitHub Actions + Docker",
        "tags": ["Next.js", "React", "TypeScript", "Postgres", "GitHub Actions"],
        "config": {
            "backend": "none",
            "frontend": "nextjs",
            "database": "postgresql",
            "pipeline": "github_actions",
            "docker": True,
            "k8s": True,
            "helm": False,
            "terraform": True,
            "monitoring": True,
            "include_tests": True,
            "include_linter": True,
        }
    },
    "spring-enterprise": {
        "name": "Spring Boot Enterprise Banking / Cloud",
        "description": "Spring Boot (Java 21) + PostgreSQL + Jenkinsfile + Docker + K8s + Helm",
        "tags": ["Java", "Spring Boot", "Postgres", "Jenkins", "Kubernetes", "Helm"],
        "config": {
            "backend": "spring_boot",
            "frontend": "none",
            "database": "postgresql",
            "pipeline": "jenkins",
            "docker": True,
            "k8s": True,
            "helm": True,
            "terraform": False,
            "monitoring": True,
            "include_tests": True,
            "include_linter": True,
        }
    },
    "quick-mvp": {
        "name": "Quick Prototype / MVP",
        "description": "FastAPI + React Vite + SQLite + GitHub Actions + Docker Compose",
        "tags": ["FastAPI", "React", "SQLite", "Docker Compose", "Fast Setup"],
        "config": {
            "backend": "fastapi",
            "frontend": "react_vite",
            "database": "sqlite",
            "pipeline": "github_actions",
            "docker": True,
            "k8s": False,
            "helm": False,
            "terraform": False,
            "monitoring": False,
            "include_tests": True,
            "include_linter": True,
        }
    },
}
