"""
Configuration validation and compatibility advisor for StackForge CLI.
"""
from typing import List, Tuple
from stackforge.core.config import StackConfig, BACKENDS, FRONTENDS, DATABASES, PIPELINES

class ConfigValidator:
    @staticmethod
    def validate(config: StackConfig) -> Tuple[List[str], List[str]]:
        """
        Validates configuration and returns (errors, warnings).
        errors: Block generation.
        warnings: Advisory notices for the developer.
        """
        errors = []
        warnings = []

        # Name validation
        if not config.project_name or not config.project_name.strip():
            errors.append("Project name cannot be empty.")
        elif any(c in config.project_name for c in r'\/:*?"<>| '):
            errors.append("Project name contains invalid filesystem characters or spaces. Use hyphens or underscores.")

        # Backend validation
        if config.backend not in BACKENDS:
            errors.append(f"Unknown backend '{config.backend}'. Available: {list(BACKENDS.keys())}")

        # Frontend validation
        if config.frontend not in FRONTENDS:
            errors.append(f"Unknown frontend '{config.frontend}'. Available: {list(FRONTENDS.keys())}")

        # Database validation
        if config.database not in DATABASES:
            errors.append(f"Unknown database '{config.database}'. Available: {list(DATABASES.keys())}")

        # Pipeline validation
        if config.pipeline not in PIPELINES:
            errors.append(f"Unknown pipeline '{config.pipeline}'. Available: {list(PIPELINES.keys())}")

        # Architecture warnings
        if config.frontend == "nextjs" and config.backend != "none":
            warnings.append(
                "Next.js has built-in API routes. Setting up an external backend creates a decoupled microservice architecture."
            )

        if config.database == "sqlite" and config.k8s:
            warnings.append(
                "SQLite is an embedded file-based database and may encounter file locking issues when scaled horizontally in Kubernetes pods. Consider PostgreSQL for clustered workloads."
            )

        if not config.docker and (config.k8s or config.helm):
            warnings.append(
                "Kubernetes and Helm manifests are enabled, but Docker containerization is turned off. A Docker image is normally required to run in Kubernetes."
            )

        return errors, warnings
