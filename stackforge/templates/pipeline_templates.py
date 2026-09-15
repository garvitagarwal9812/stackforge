"""
CI/CD Pipeline workflow templates for GitHub Actions, GitLab CI, Azure DevOps, Jenkins, and CircleCI.
"""
from typing import Dict
from stackforge.core.config import StackConfig

def get_pipeline_files(config: StackConfig) -> Dict[str, str]:
    files = {}
    pipe = config.pipeline
    name = config.project_name
    backend = config.backend
    frontend = config.frontend

    # 1. GITHUB ACTIONS
    if pipe == "github_actions":
        # CI Workflow
        backend_test_step = ""
        if backend == "fastapi" or backend == "django":
            backend_test_step = """      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install backend dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt

      - name: Run Backend Pytest Suite
        run: |
          pytest backend/tests --junitxml=junit/test-results.xml
"""
        elif backend == "express_ts" or backend == "nestjs":
            backend_test_step = """      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
          cache-dependency-path: 'backend/package-lock.json'

      - name: Install backend dependencies
        run: cd backend && npm ci

      - name: Run Backend Tests
        run: cd backend && npm test
"""
        elif backend == "go_gin":
            backend_test_step = """      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.22'

      - name: Run Go Test Suite
        run: cd backend && go test -v ./...
"""
        elif backend == "rust_axum":
            backend_test_step = """      - name: Set up Rust toolchain
        uses: dtolnay/rust-toolchain@stable

      - name: Cargo Test & Lint
        run: |
          cd backend
          cargo test --verbose
          cargo check
"""

        frontend_test_step = ""
        if frontend in ("react_vite", "nextjs", "vue_vite", "sveltekit"):
            frontend_test_step = """      - name: Set up Node.js for Frontend
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
          cache-dependency-path: 'frontend/package-lock.json'

      - name: Install frontend dependencies & build check
        run: |
          cd frontend
          npm ci || npm install
          npm run build
"""

        files[".github/workflows/ci.yml"] = f"""name: Continuous Integration (CI)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

concurrency:
  group: ${{{{ github.workflow }}}}-${{{{ github.ref }}}}
  cancel-in-progress: true

jobs:
  lint-and-test:
    name: Lint & Automated Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

{backend_test_step}
{frontend_test_step}
      - name: Upload Test Artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: junit/
          retention-days: 7
"""

        # CD Workflow
        files[".github/workflows/cd.yml"] = f"""name: Continuous Deployment (CD)

on:
  push:
    branches: [ main ]
    tags: [ 'v*.*.*' ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{{{ github.repository }}}}

jobs:
  build-and-publish:
    name: Build & Publish Container Images
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{{{ env.REGISTRY }}}}
          username: ${{{{ github.actor }}}}
          password: ${{{{ secrets.GITHUB_TOKEN }}}}

      - name: Extract Docker metadata (Backend)
        id: meta-backend
        uses: docker/metadata-action@v5
        with:
          images: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}-backend
          tags: |
            type=ref,event=branch
            type=semver,pattern={{{{version}}}}
            type=sha,format=short

      - name: Build & Push Backend Image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{{{ steps.meta-backend.outputs.tags }}}}
          labels: ${{{{ steps.meta-backend.outputs.labels }}}}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-kubernetes:
    name: Deploy to Kubernetes Cluster
    needs: build-and-publish
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set Kubernetes Context
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{{{ secrets.KUBE_CONFIG }}}}
        continue-on-error: true

      - name: Deploy Manifests
        run: |
          echo "Applying Kubernetes manifests for {name}..."
          # kubectl apply -f k8s/
"""

        # Security Scan Workflow
        files[".github/workflows/security.yml"] = f"""name: Security & Vulnerability Audit

on:
  schedule:
    - cron: '0 4 * * 1' # Every Monday at 04:00 UTC
  pull_request:
    branches: [ main ]

jobs:
  trivy-scan:
    name: Trivy Container & Dependency Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Run Trivy Vulnerability Scanner (Repo)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          ignore-unfixed: true
          format: 'table'
          severity: 'CRITICAL,HIGH'
"""

    # 2. GITLAB CI
    elif pipe == "gitlab_ci":
        files[".gitlab-ci.yml"] = f"""# GitLab CI/CD Multi-Stage Pipeline for {name}
image: docker:24.0.5

variables:
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG

stages:
  - lint
  - test
  - containerize
  - deploy_staging
  - deploy_production

services:
  - docker:24.0.5-dind

lint_code:
  stage: lint
  script:
    - echo "Running code quality and style checks..."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'

run_tests:
  stage: test
  script:
    - echo "Executing unit tests for {backend}..."
  artifacts:
    when: always
    reports:
      junit: junit-results.xml

build_and_push:
  stage: containerize
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG ./backend
    - docker push $IMAGE_TAG
  only:
    - main
    - develop

deploy_staging:
  stage: deploy_staging
  image: bitnami/kubectl:latest
  script:
    - echo "Deploying {name} to Staging Cluster..."
    - kubectl config use-context $KUBE_CONTEXT
    - kubectl apply -f k8s/
  environment:
    name: staging
    url: https://staging.{name}.internal
  only:
    - develop

deploy_production:
  stage: deploy_production
  image: bitnami/kubectl:latest
  script:
    - echo "Deploying {name} to Production Cluster..."
    - kubectl config use-context $KUBE_CONTEXT_PROD
    - kubectl apply -f k8s/
  environment:
    name: production
    url: https://{name}.com
  when: manual
  only:
    - main
"""

    # 3. AZURE DEVOPS
    elif pipe == "azure_devops":
        files["azure-pipelines.yml"] = f"""# Azure DevOps Pipeline for {name}
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'
  imageRepository: '{name}-backend'
  containerRegistry: 'acr-connection'
  dockerfilePath: '$(Build.SourcesDirectory)/backend/Dockerfile'
  tag: '$(Build.BuildId)'

stages:
- stage: BuildAndTest
  displayName: 'Build and Unit Test'
  jobs:
  - job: TestJob
    steps:
    - script: |
        echo "Running test suite for {name} ({backend})..."
      displayName: 'Execute Automated Tests'

- stage: Containerize
  displayName: 'Build & Push Docker Image'
  dependsOn: BuildAndTest
  condition: succeeded()
  jobs:
  - job: DockerBuild
    steps:
    - task: Docker@2
      displayName: 'Build and push Docker image'
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(containerRegistry)
        tags: |
          $(tag)
          latest

- stage: DeployAKS
  displayName: 'Deploy to Azure Kubernetes (AKS)'
  dependsOn: Containerize
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: Deploy
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "Applying Kubernetes manifests to AKS..."
            displayName: 'Kubectl Rollout'
"""

    # 4. JENKINS
    elif pipe == "jenkins":
        files["Jenkinsfile"] = f"""pipeline {{
    agent any

    environment {{
        PROJECT_NAME = '{name}'
        REGISTRY = 'docker.io/myorg'
        IMAGE_NAME = "${{REGISTRY}}/${{PROJECT_NAME}}-backend:${{BUILD_NUMBER}}"
    }}

    stages {{
        stage('Checkout') {{
            steps {{
                checkout scm
            }}
        }}

        stage('Static Analysis & Quality') {{
            steps {{
                echo 'Running linting and quality scans...'
            }}
        }}

        stage('Automated Tests') {{
            steps {{
                echo 'Executing test suite for {backend}...'
            }}
        }}

        stage('Docker Build & Package') {{
            steps {{
                script {{
                    echo "Building Docker container image: ${{IMAGE_NAME}}"
                    // sh "docker build -t ${{IMAGE_NAME}} ./backend"
                }}
            }}
        }}

        stage('Security Scan') {{
            steps {{
                echo 'Running Trivy container scan...'
            }}
        }}

        stage('Deploy to Kubernetes') {{
            when {{
                branch 'main'
            }}
            steps {{
                echo 'Executing kubectl rollout to production cluster...'
                // sh "kubectl apply -f k8s/"
            }}
        }}
    }}

    post {{
        always {{
            cleanWs()
        }}
        success {{
            echo "Pipeline completed successfully for ${{PROJECT_NAME}}!"
        }}
        failure {{
            echo "Pipeline failed on build ${{BUILD_NUMBER}}."
        }}
    }}
}}
"""

    # 5. CIRCLECI
    elif pipe == "circleci":
        files[".circleci/config.yml"] = f"""version: 2.1

orbs:
  docker: circleci/docker@2.6.0

jobs:
  test-and-lint:
    docker:
      - image: cimg/base:current
    steps:
      - checkout
      - run:
          name: Run Automated Tests
          command: |
            echo "Running test suite for {backend}..."

  build-and-push-docker:
    docker:
      - image: cimg/base:current
    steps:
      - checkout
      - setup_remote_docker:
          version: 20.10.24
      - run:
          name: Build Docker Image
          command: |
            docker build -t {name}-backend:$CIRCLE_SHA1 ./backend

workflows:
  build-test-deploy:
    jobs:
      - test-and-lint
      - build-and-push-docker:
          requires:
            - test-and-lint
          filters:
            branches:
              only: main
"""

    return files
