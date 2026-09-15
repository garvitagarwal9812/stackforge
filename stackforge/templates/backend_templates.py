"""
Backend source code templates for FastAPI, Express TypeScript, Go Gin, Rust Axum, Django, and Spring Boot.
"""
from typing import Dict
from stackforge.core.config import StackConfig

def get_backend_files(config: StackConfig) -> Dict[str, str]:
    files = {}
    backend = config.backend
    name = config.project_name
    db = config.database

    if backend == "none":
        return files

    if backend == "fastapi":
        files["backend/requirements.txt"] = """fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pydantic>=2.9.0
pydantic-settings>=2.5.0
sqlalchemy>=2.0.35
psycopg2-binary>=2.9.9
redis>=5.1.0
pytest>=8.3.0
pytest-asyncio>=0.24.0
httpx>=0.27.2
"""
        files["backend/app/__init__.py"] = '"""Application package."""\n__version__ = "1.0.0"\n'
        files["backend/app/core/config.py"] = f"""from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "{name}"
    API_V1_STR: str = "/api/v1"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/{name}"
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
"""
        files["backend/app/api/v1/endpoints/health.py"] = f"""from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health", tags=["Monitoring"])
def health_check():
    return {{
        "status": "healthy",
        "service": "{name}-backend",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }}
"""
        files["backend/app/api/v1/endpoints/items.py"] = """from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ItemSchema(BaseModel):
    id: int
    name: str
    description: str

items_db = [
    {"id": 1, "name": "Cloud Native Architecture", "description": "Microservice scaffolded with StackForge"},
    {"id": 2, "name": "CI/CD Pipeline", "description": "Automated build, test and deployment"}
]

@router.get("/items", response_model=List[ItemSchema], tags=["Items"])
def list_items():
    return items_db

@router.post("/items", response_model=ItemSchema, tags=["Items"])
def create_item(item: ItemSchema):
    items_db.append(item.model_dump())
    return item
"""
        files["backend/app/main.py"] = f"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import health, items

app = FastAPI(
    title="{name} API",
    description="High-performance backend forged with StackForge",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(items.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {{
        "message": "Welcome to {name} API",
        "docs": "/docs",
        "health": f"{{settings.API_V1_STR}}/health"
    }}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
"""
        files["backend/tests/test_main.py"] = """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
"""
        files["backend/Dockerfile"] = """FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim as runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    elif backend == "express_ts":
        files["backend/package.json"] = f"""{{
  "name": "{name}-backend",
  "version": "1.0.0",
  "description": "Express TypeScript API scaffolded with StackForge",
  "main": "dist/index.js",
  "scripts": {{
    "dev": "nodemon --exec ts-node src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "lint": "eslint src/**/*.ts"
  }},
  "dependencies": {{
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.21.0",
    "helmet": "^7.1.0",
    "morgan": "^1.10.0",
    "zod": "^3.23.8"
  }},
  "devDependencies": {{
    "@types/cors": "^2.8.17",
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.13",
    "@types/morgan": "^1.9.9",
    "@types/node": "^22.7.4",
    "@types/supertest": "^6.0.2",
    "jest": "^29.7.0",
    "nodemon": "^3.1.7",
    "supertest": "^7.0.0",
    "ts-jest": "^29.2.5",
    "ts-node": "^10.9.2",
    "typescript": "^5.6.2"
  }}
}}
"""
        files["backend/tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}
"""
        files["backend/src/index.ts"] = f"""import express, {{ Request, Response }} from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.get('/health', (req: Request, res: Response) => {{
  res.json({{
    status: 'healthy',
    service: '{name}-backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  }});
}});

app.get('/api/v1/items', (req: Request, res: Response) => {{
  res.json([
    {{ id: 1, name: 'Cloud Architecture', framework: 'Express TS' }},
    {{ id: 2, name: 'DevOps Pipeline', tool: 'StackForge' }}
  ]);
}});

app.listen(PORT, () => {{
  console.log(`🚀 Server listening on port ${{PORT}}`);
}});

export default app;
"""
        files["backend/tests/health.test.ts"] = """import request from 'supertest';
import app from '../src/index';

describe('Health Check API', () => {
  it('should return status healthy', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toEqual(200);
    expect(res.body.status).toEqual('healthy');
  });
});
"""
        files["backend/Dockerfile"] = """FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json tsconfig.json ./
RUN npm ci
COPY src ./src
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist

EXPOSE 5000
CMD ["node", "dist/index.js"]
"""

    elif backend == "go_gin":
        files["backend/go.mod"] = f"""module {name}-backend

go 1.22

require (
    github.com/gin-gonic/gin v1.10.0
)
"""
        files["backend/main.go"] = f"""package main

import (
    "net/http"
    "time"
    "github.com/gin-gonic/gin"
)

type HealthResponse struct {{
    Status    string    `json:"status"`
    Service   string    `json:"service"`
    Timestamp time.Time `json:"timestamp"`
    Version   string    `json:"version"`
}}

func main() {{
    r := gin.Default()

    r.GET("/health", func(c *gin.Context) {{
        c.JSON(http.StatusOK, HealthResponse{{
            Status:    "healthy",
            Service:   "{name}-backend",
            Timestamp: time.Now().UTC(),
            Version:   "1.0.0",
        }})
    }})

    r.GET("/api/v1/items", func(c *gin.Context) {{
        c.JSON(http.StatusOK, gin.H{{
            "items": []string{{"Fast Execution", "Type Safe", "Gin Web Framework"}},
        }})
    }})

    r.Run(":8080")
}}
"""
        files["backend/Dockerfile"] = f"""FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /server main.go

FROM scratch
COPY --from=builder /server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
"""

    elif backend == "rust_axum":
        files["backend/Cargo.toml"] = f"""[package]
name = "{name}-backend"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.7"
tokio = {{ version = "1.0", features = ["full"] }}
serde = {{ version = "1.0", features = ["derive"] }}
serde_json = "1.0"
tower-http = {{ version = "0.5", features = ["cors", "trace"] }}
chrono = {{ version = "0.4", features = ["serde"] }}
"""
        files["backend/src/main.rs"] = f"""use axum::{{
    routing::get,
    Json, Router,
}};
use serde::Serialize;
use std::net::SocketAddr;
use chrono::Utc;

#[derive(Serialize)]
struct HealthResponse {{
    status: &'static str,
    service: &'static str,
    timestamp: String,
    version: &'static str,
}}

async fn health_check() -> Json<HealthResponse> {{
    Json(HealthResponse {{
        status: "healthy",
        service: "{name}-backend",
        timestamp: Utc::now().to_rfc3339(),
        version: "1.0.0",
    }})
}}

#[tokio::main]
async fn main() {{
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/", get(|| async {{ "Welcome to {name} Rust Service!" }}));

    let addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    println!("🦀 Rust Axum listening on {{}}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}}
"""
        files["backend/Dockerfile"] = """FROM rust:1.77-slim as builder
WORKDIR /usr/src/app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=builder /usr/src/app/target/release/*-backend /usr/local/bin/server
EXPOSE 8080
CMD ["server"]
"""

    elif backend == "django":
        files["backend/requirements.txt"] = """django>=5.1.0
djangorestframework>=3.15.2
django-cors-headers>=4.4.0
psycopg2-binary>=2.9.9
gunicorn>=23.0.0
pytest-django>=4.9.0
"""
        files["backend/core/settings.py"] = f"""import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-stackforge-secret-key-change-in-prod'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
CORS_ALLOW_ALL_ORIGINS = True
WSGI_APPLICATION = 'core.wsgi.application'
"""
        files["backend/core/urls.py"] = """from django.urls import path
from django.http import JsonResponse

def health_view(request):
    return JsonResponse({"status": "healthy", "service": "django-backend"})

urlpatterns = [
    path('health/', health_view),
]
"""
        files["backend/Dockerfile"] = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
"""

    elif backend == "spring_boot":
        files["backend/pom.xml"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.3</version>
    </parent>
    <groupId>com.stackforge</groupId>
    <artifactId>{name}-backend</artifactId>
    <version>1.0.0</version>
    <properties>
        <java.version>21</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
    </dependencies>
</project>
"""
        files["backend/src/main/java/com/stackforge/app/Application.java"] = """package com.stackforge.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
"""
        files["backend/Dockerfile"] = """FROM maven:3.9-eclipse-temurin-21-alpine AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
"""

    return files
