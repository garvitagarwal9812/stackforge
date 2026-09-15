"""
Core scaffolding and file generation engine for StackForge CLI.
"""
from typing import Dict, List, Tuple
import os
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from stackforge.core.config import StackConfig
from stackforge.templates import (
    get_backend_files,
    get_frontend_files,
    get_database_files,
    get_pipeline_files,
    get_devops_files,
    get_tooling_files
)

class ProjectGenerator:
    def __init__(self, config: StackConfig, console: Console = None):
        self.config = config
        self.console = console or Console()

    def compile_blueprint(self) -> Dict[str, str]:
        """
        Gathers all template files based on configuration into a unified file dictionary.
        Keys are relative paths, values are file contents.
        """
        blueprint: Dict[str, str] = {}

        # 1. Backend source files
        blueprint.update(get_backend_files(self.config))

        # 2. Frontend source files
        blueprint.update(get_frontend_files(self.config))

        # 3. Database schemas & init scripts
        blueprint.update(get_database_files(self.config))

        # 4. CI/CD pipeline automation workflows
        blueprint.update(get_pipeline_files(self.config))

        # 5. DevOps infrastructure (Docker, K8s, Helm, Terraform, Monitoring)
        blueprint.update(get_devops_files(self.config))

        # 6. Tooling & Root files (Makefile, README, .gitignore, .env)
        blueprint.update(get_tooling_files(self.config))

        return blueprint

    def generate(self, dry_run: bool = False) -> Tuple[List[str], Dict[str, str]]:
        """
        Compiles the blueprint and writes all files to the target output directory.
        Shows an animated terminal progress bar.
        """
        blueprint = self.compile_blueprint()
        created_files = []
        target_root = os.path.abspath(self.config.output_dir)

        if dry_run:
            return list(blueprint.keys()), blueprint

        with Progress(
            SpinnerColumn(spinner_name="dots12", style="magenta"),
            TextColumn("[bold cyan]{task.description}[/bold cyan]"),
            BarColumn(bar_width=30, style="cyan", complete_style="spring_green1"),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task(f"Forging {self.config.project_name}...", total=len(blueprint))

            for rel_path, content in blueprint.items():
                full_path = os.path.join(target_root, rel_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)

                created_files.append(full_path)
                progress.update(task, advance=1, description=f"Writing {os.path.basename(rel_path)}...")
                time.sleep(0.015)  # Smooth terminal animation effect

        return created_files, blueprint
