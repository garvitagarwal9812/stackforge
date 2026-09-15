"""
Command-Line Interface (CLI) Dispatcher for StackForge.
Supports both fully interactive terminal wizard and headless command-line flags.
"""
import sys
import os
from typing import Optional

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import click
from rich.console import Console
from rich.table import Table

from stackforge import __version__
from stackforge.core.config import StackConfig, BACKENDS, FRONTENDS, DATABASES, PIPELINES
from stackforge.core.generator import ProjectGenerator
from stackforge.core.validator import ConfigValidator
from stackforge.presets.default_presets import PRESETS
from stackforge.ui.banner import print_banner, get_banner_panel
from stackforge.ui.colors import THEMES, DEFAULT_THEME
from stackforge.ui.viewer import display_file_tree, preview_key_file, print_next_steps
from stackforge.ui.wizard import TerminalWizard

def get_console(theme_name: str = DEFAULT_THEME) -> Console:
    theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
    return Console(theme=theme, legacy_windows=False)

@click.command(help="StackForge CLI: Terminal-based Project Boilerplate & CI/CD Pipeline Generator")
@click.option("--name", "-n", default=None, help="Project name and target directory")
@click.option("--preset", "-p", default=None, type=click.Choice(list(PRESETS.keys()), case_sensitive=False), help="Use a curated production preset")
@click.option("--list-presets", is_flag=True, help="List all available production architecture presets")
@click.option("--backend", "-b", default=None, type=click.Choice(list(BACKENDS.keys()), case_sensitive=False), help="Backend framework")
@click.option("--frontend", "-f", default=None, type=click.Choice(list(FRONTENDS.keys()), case_sensitive=False), help="Frontend framework")
@click.option("--db", "-d", default=None, type=click.Choice(list(DATABASES.keys()), case_sensitive=False), help="Database system")
@click.option("--pipeline", "-c", default=None, type=click.Choice(list(PIPELINES.keys()), case_sensitive=False), help="Target CI/CD pipeline")
@click.option("--docker/--no-docker", default=True, help="Include Dockerfile and Docker Compose")
@click.option("--k8s/--no-k8s", default=True, help="Include Kubernetes manifests")
@click.option("--helm/--no-helm", default=True, help="Include Helm chart packaging")
@click.option("--terraform/--no-terraform", default=False, help="Include Terraform IaC")
@click.option("--monitoring/--no-monitoring", default=True, help="Include Prometheus & Grafana monitoring")
@click.option("--out", "-o", default=None, help="Target output directory")
@click.option("--config", "-C", default=None, type=click.Path(exists=True), help="Load configuration from JSON file")
@click.option("--dry-run", is_flag=True, help="Simulate generation and show file blueprint without writing")
@click.option("--preview", is_flag=True, help="Preview sample generated files in terminal with syntax highlighting")
@click.option("--theme", default=DEFAULT_THEME, type=click.Choice(list(THEMES.keys())), help="Terminal color theme")
@click.version_option(version=__version__, prog_name="StackForge CLI")
def main(
    name: Optional[str],
    preset: Optional[str],
    list_presets: bool,
    backend: Optional[str],
    frontend: Optional[str],
    db: Optional[str],
    pipeline: Optional[str],
    docker: bool,
    k8s: bool,
    helm: bool,
    terraform: bool,
    monitoring: bool,
    out: Optional[str],
    config: Optional[str],
    dry_run: bool,
    preview: bool,
    theme: str
):
    console = get_console(theme)

    # 1. Handle --list-presets flag
    if list_presets:
        print_banner(console, theme)
        table = Table(title="[bold cyan]⚡ Available StackForge Production Presets[/bold cyan]", border_style="cyan")
        table.add_column("Preset ID", style="bold magenta", width=22)
        table.add_column("Name", style="bold bright_white", width=28)
        table.add_column("Description", style="bright_black", width=46)
        table.add_column("Key Technologies", style="spring_green1")

        for key, val in PRESETS.items():
            table.add_row(key, val["name"], val["description"], " • ".join(val["tags"][:4]))

        console.print(table)
        console.print("\n[dim]Generate any preset with: [bold cyan]stackforge --preset <id>[/bold cyan][/dim]\n")
        return

    # 2. Determine configuration source
    stack_config: Optional[StackConfig] = None

    if config:
        try:
            stack_config = StackConfig.load_from_file(config)
            console.print(f"[green]Loaded configuration from {config}[/green]")
        except Exception as e:
            console.print(f"[red]Error loading config file: {e}[/red]")
            sys.exit(1)

    elif preset:
        preset_info = PRESETS[preset]
        cfg_dict = preset_info["config"].copy()
        proj_name = name or preset.replace("-", "_")
        cfg_dict["project_name"] = proj_name
        cfg_dict["output_dir"] = out or f"./{proj_name}"
        stack_config = StackConfig.from_dict(cfg_dict)
        console.print(f"[green]Using preset: [bold]{preset_info['name']}[/bold][/green]")

    elif any([backend, frontend, db, pipeline]):
        # Direct CLI flag specification
        proj_name = name or "my-stack"
        stack_config = StackConfig(
            project_name=proj_name,
            backend=backend or "fastapi",
            frontend=frontend or "react_vite",
            database=db or "postgresql",
            pipeline=pipeline or "github_actions",
            docker=docker,
            k8s=k8s,
            helm=helm,
            terraform=terraform,
            monitoring=monitoring,
            output_dir=out or f"./{proj_name}"
        )

    else:
        # No direct flags provided: Launch interactive wizard!
        wizard = TerminalWizard(console)
        try:
            stack_config = wizard.run()
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user.[/yellow]")
            sys.exit(0)

    if not stack_config:
        return

    # Apply overrides if provided via flags
    if name:
        stack_config.project_name = name
    if out:
        stack_config.output_dir = out

    # Validate configuration
    errors, warnings = ConfigValidator.validate(stack_config)
    if errors:
        for err in errors:
            console.print(f"[red bold]Error:[/red bold] {err}")
        sys.exit(1)

    for warn in warnings:
        console.print(f"[yellow]Warning:[/yellow] {warn}")

    # Generate or simulate
    generator = ProjectGenerator(stack_config, console)

    if dry_run:
        console.print("\n[bold yellow]🔍 DRY RUN SIMULATION MODE[/bold yellow]")
        _, blueprint = generator.generate(dry_run=True)
        display_file_tree(console, blueprint, root_name=stack_config.project_name)
        console.print(f"[dim]Total {len(blueprint)} files would be created under {stack_config.output_dir}[/dim]\n")
        return

    console.print()
    created_files, blueprint = generator.generate(dry_run=False)

    console.print()
    display_file_tree(console, blueprint, root_name=stack_config.project_name)

    # Optional syntax-highlighted preview of pipeline & dockerfile
    if preview:
        pipeline_file = None
        for path in blueprint.keys():
            if "workflows" in path or "gitlab-ci" in path or "azure-pipelines" in path or "Jenkinsfile" in path:
                pipeline_file = path
                break
        if pipeline_file:
            preview_key_file(console, pipeline_file, blueprint[pipeline_file])

        if "docker-compose.yml" in blueprint:
            preview_key_file(console, "docker-compose.yml", blueprint["docker-compose.yml"])

    print_next_steps(console, stack_config, stack_config.output_dir)

if __name__ == "__main__":
    main()
