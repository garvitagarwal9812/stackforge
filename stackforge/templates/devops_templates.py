"""
DevOps infrastructure templates: Docker Compose, Kubernetes, Helm, Terraform, and Prometheus.
"""
from typing import Dict
from stackforge.core.config import StackConfig

def get_devops_files(config: StackConfig) -> Dict[str, str]:
    files = {}
    name = config.project_name
    backend = config.backend
    frontend = config.frontend
    db = config.database

    # 1. DOCKER & DOCKER COMPOSE
    if config.docker:
        files[".dockerignore"] = """node_modules
dist
build
.git
.env
__pycache__
*.pyc
.pytest_cache
target
.DS_Store
"""
        # Compose Services
        services = []
        volumes = []

        # Backend service
        if backend != "none":
            services.append(f"""  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: {name}-backend
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://postgres:postgres@database:5432/{name}
      - REDIS_URL=redis://cache:6379/0
    restart: unless-stopped
    depends_on:
      - database
""")

        # Frontend service
        if frontend != "none":
            depends_block = "\n    depends_on:\n      - backend" if backend != "none" else ""
            services.append(f"""  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: {name}-frontend
    ports:
      - "3000:80"
    restart: unless-stopped{depends_block}
""")

        # Database service
        if db == "postgresql":
            services.append(f"""  database:
    image: postgres:16-alpine
    container_name: {name}-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: {name}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped
""")
            volumes.append("  pgdata:")
        elif db == "mongodb":
            services.append(f"""  database:
    image: mongo:7.0
    container_name: {name}-mongo
    ports:
      - "27017:27017"
    volumes:
      - mongodata:/data/db
      - ./database/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    restart: unless-stopped
""")
            volumes.append("  mongodata:")
        elif db == "mysql":
            services.append(f"""  database:
    image: mysql:8.0
    container_name: {name}-mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: {name}
    ports:
      - "3306:3306"
    volumes:
      - mysqldata:/var/lib/mysql
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped
""")
            volumes.append("  mysqldata:")

        # Redis Cache service
        services.append(f"""  cache:
    image: redis:7-alpine
    container_name: {name}-redis
    ports:
      - "6379:6379"
    restart: unless-stopped
""")

        vol_block = ("volumes:\n" + "\n".join(volumes)) if volumes else ""

        files["docker-compose.yml"] = f"""version: '3.8'

# Local Development Stack for {name}
services:
{"".join(services)}
{vol_block}
"""

        files["docker-compose.prod.yml"] = f"""version: '3.8'

# Production Hardened Stack for {name}
services:
  backend:
    image: ghcr.io/myorg/{name}-backend:latest
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    env_file:
      - .env.production
"""

    # 2. KUBERNETES MANIFESTS
    if config.k8s:
        files["k8s/namespace.yaml"] = f"""apiVersion: v1
kind: Namespace
metadata:
  name: {name}-prod
  labels:
    environment: production
    managed-by: stackforge
"""
        files["k8s/configmap.yaml"] = f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {name}-config
  namespace: {name}-prod
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "info"
  PORT: "8000"
"""
        files["k8s/secret.yaml"] = f"""apiVersion: v1
kind: Secret
metadata:
  name: {name}-secrets
  namespace: {name}-prod
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@postgres-service:5432/{name}"
  JWT_SECRET: "replace-with-vault-managed-secret-key"
"""
        files["k8s/backend-deployment.yaml"] = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}-backend
  namespace: {name}-prod
  labels:
    app: {name}
    tier: backend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: {name}
      tier: backend
  template:
    metadata:
      labels:
        app: {name}
        tier: backend
    spec:
      containers:
      - name: backend
        image: ghcr.io/myorg/{name}-backend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
        envFrom:
        - configMapRef:
            name: {name}-config
        - secretRef:
            name: {name}-secrets
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
"""
        files["k8s/backend-service.yaml"] = f"""apiVersion: v1
kind: Service
metadata:
  name: {name}-backend-svc
  namespace: {name}-prod
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: {name}
    tier: backend
"""
        files["k8s/ingress.yaml"] = f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {name}-ingress
  namespace: {name}-prod
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api.{name}.example.com
    secretName: {name}-tls-cert
  rules:
  - host: api.{name}.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {name}-backend-svc
            port:
              number: 80
"""
        files["k8s/hpa.yaml"] = f"""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {name}-backend-hpa
  namespace: {name}-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {name}-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
"""

    # 3. HELM CHARTS
    if config.helm:
        files["helm/Chart.yaml"] = f"""apiVersion: v2
name: {name}
description: Production Helm Chart for {name} deployed via StackForge
type: application
version: 0.1.0
appVersion: "1.0.0"
maintainers:
  - name: {config.author}
"""
        files["helm/values.yaml"] = f"""# Default values for {name}
replicaCount: 2

image:
  repository: ghcr.io/myorg/{name}-backend
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: {name}.local
      paths:
        - path: /
          pathType: ImplementationSpecific

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
"""
        files["helm/templates/_helpers.tpl"] = f"""{{{{/*
Expand the name of the chart.
*/}}}}
{{{{- define "{name}.name" -}}}}
{{{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}}}
{{{{- end }}}}
"""
        files["helm/templates/deployment.yaml"] = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{{{ include "{name}.name" . }}}}
  labels:
    app: {{{{ include "{name}.name" . }}}}
spec:
  replicas: {{{{ .Values.replicaCount }}}}
  selector:
    matchLabels:
      app: {{{{ include "{name}.name" . }}}}
  template:
    metadata:
      labels:
        app: {{{{ include "{name}.name" . }}}}
    spec:
      containers:
        - name: {{{{ .Chart.Name }}}}
          image: "{{{{ .Values.image.repository }}}}:{{{{ .Values.image.tag }}}}"
          imagePullPolicy: {{{{ .Values.image.pullPolicy }}}}
          ports:
            - containerPort: {{{{ .Values.service.targetPort }}}}
          resources:
            {{{{- toYaml .Values.resources | nindent 12 }}}}
"""
        files["helm/templates/service.yaml"] = f"""apiVersion: v1
kind: Service
metadata:
  name: {{{{ include "{name}.name" . }}}}
spec:
  type: {{{{ .Values.service.type }}}}
  ports:
    - port: {{{{ .Values.service.port }}}}
      targetPort: {{{{ .Values.service.targetPort }}}}
  selector:
    app: {{{{ include "{name}.name" . }}}}
"""

    # 4. TERRAFORM CLOUD INFRASTRUCTURE
    if config.terraform:
        files["terraform/main.tf"] = f"""# Terraform Cloud Provisioning for {name}
terraform {{
  required_version = ">= 1.5.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

# VPC & Networking
resource "aws_vpc" "main" {{
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {{
    Name = "{name}-vpc"
  }}
}}

# Container Registry (ECR)
resource "aws_ecr_repository" "backend" {{
  name                 = "{name}-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {{
    scan_on_push = true
  }}
}}
"""
        files["terraform/variables.tf"] = """variable "aws_region" {
  type        = string
  description = "Target AWS deployment region"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Target deployment tier"
  default     = "production"
}
"""
        files["terraform/outputs.tf"] = """output "ecr_repository_url" {
  description = "Docker Image Repository URL"
  value       = aws_ecr_repository.backend.repository_url
}
"""
        files["terraform/terraform.tfvars.example"] = """aws_region  = "us-east-1"
environment = "production"
"""

    # 5. PROMETHEUS & GRAFANA MONITORING
    if config.monitoring:
        files["monitoring/prometheus.yml"] = f"""global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: '{name}-backend'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['backend:8000']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
"""
        files["monitoring/grafana/dashboards/overview.json"] = f"""{{
  "title": "{name} - Service Health & Metrics",
  "tags": ["stackforge", "microservices"],
  "timezone": "browser",
  "panels": [
    {{
      "title": "API Request Rate (RPS)",
      "type": "graph",
      "gridPos": {{ "x": 0, "y": 0, "w": 12, "h": 8 }}
    }},
    {{
      "title": "Response Latency (p95)",
      "type": "graph",
      "gridPos": {{ "x": 12, "y": 0, "w": 12, "h": 8 }}
    }}
  ],
  "schemaVersion": 36
}}
"""

    return files
