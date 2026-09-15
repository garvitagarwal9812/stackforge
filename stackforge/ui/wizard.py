"""
Interactive Terminal Wizard for StackForge CLI.
Guides the developer step-by-step through choosing tech stacks, CI/CD pipelines, and DevOps tooling.
"""
from typing import Optional, Dict, Any, List
import os
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from stackforge.core.config import (
    StackConfig, BACKENDS, FRONTENDS, DATABASES, PIPELINES
)
from stackforge.presets.default_presets import PRESETS
from stackforge.ui.banner import print_section_header, print_summary_card
from stackforge.core.validator import ConfigValidator

class TerminalWizard:
    def __init__(self, console: Console):
        self.console = console

    def run(self) -> Optional[StackConfig]:
        """
        Runs the interactive prompt loop and returns a valid StackConfig.
        """
        self.console.clear()
        from stackforge.ui.banner import print_banner
        print_banner(self.console)

        # Mode Selection
        self.console.print("[bold cyan]What would you like to build today?[/bold cyan]\n")
        modes = [
            ("1", "🎯 Interactive Custom Stack Wizard", "Step-by-step selection of backend, frontend, DB, CI/CD, & DevOps"),
            ("2", "⚡ Browse & Load Curated Presets", "Instant production-ready architectures (FastAPI Cloud, MERN, Go, Rust, etc.)"),
            ("3", "📁 Load Configuration File", "Load stack architecture from a local stackforge.json"),
            ("q", "❌ Exit", "Cancel and quit"),
        ]

        for key, name, desc in modes:
            self.console.print(f"  [bold magenta][{key}][/bold magenta] [bold bright_white]{name}[/bold bright_white] [bright_black]— {desc}[/bright_black]")
        self.console.print()

        mode_choice = Prompt.ask(
            "[bold cyan]Select an option[/bold cyan]",
            choices=["1", "2", "3", "q"],
            default="1",
            console=self.console
        )

        if mode_choice == "q":
            self.console.print("[yellow]Scaffolding aborted. See you next time![/yellow]")
            return None
        elif mode_choice == "2":
            return self._select_preset_flow()
        elif mode_choice == "3":
            return self._load_file_flow()
        else:
            return self._custom_wizard_flow()

    def _select_preset_flow(self) -> Optional[StackConfig]:
        """Preset browsing and selection flow."""
        self.console.print("\n[bold cyan]Available Production-Ready Architecture Presets:[/bold cyan]\n")

        table = Table(border_style="cyan")
        table.add_column("#", style="bold magenta", width=4)
        table.add_column("Preset Name", style="bold bright_white", width=26)
        table.add_column("Description", style="bright_black", width=42)
        table.add_column("Key Technologies", style="spring_green1")

        preset_keys = list(PRESETS.keys())
        for idx, key in enumerate(preset_keys, 1):
            p = PRESETS[key]
            table.add_row(str(idx), p["name"], p["description"], " • ".join(p["tags"][:4]))

        self.console.print(table)
        self.console.print()

        choice = Prompt.ask(
            "[bold cyan]Choose a preset number (or 'b' for back)[/bold cyan]",
            choices=[str(i) for i in range(1, len(preset_keys) + 1)] + ["b"],
            default="1",
            console=self.console
        )

        if choice == "b":
            return self.run()

        selected_key = preset_keys[int(choice) - 1]
        preset_data = PRESETS[selected_key]
        self.console.print(f"\n[green]Selected: [bold]{preset_data['name']}[/bold][/green]")

        proj_name = Prompt.ask(
            "[bold cyan]Enter target project folder/name[/bold cyan]",
            default=selected_key.replace("-", "_"),
            console=self.console
        )

        config_dict = preset_data["config"].copy()
        config_dict["project_name"] = proj_name
        config_dict["output_dir"] = f"./{proj_name}"

        return self._review_and_confirm(StackConfig.from_dict(config_dict))

    def _load_file_flow(self) -> Optional[StackConfig]:
        """Load configuration from JSON file."""
        filepath = Prompt.ask(
            "[bold cyan]Enter path to stackforge.json[/bold cyan]",
            default="stackforge.json",
            console=self.console
        )
        if not os.path.exists(filepath):
            self.console.print(f"[red]File '{filepath}' not found![/red]")
            if Confirm.ask("Try again?", default=True, console=self.console):
                return self._load_file_flow()
            return None

        try:
            config = StackConfig.load_from_file(filepath)
            self.console.print(f"[green]Successfully loaded configuration from {filepath}![/green]")
            return self._review_and_confirm(config)
        except Exception as e:
            self.console.print(f"[red]Failed to parse configuration: {e}[/red]")
            return None

    def _custom_wizard_flow(self) -> Optional[StackConfig]:
        """Full interactive step-by-step wizard."""
        config = StackConfig()

        # Step 1: Project Metadata
        self.console.print()
        print_section_header(self.console, 1, "Project Identity", "Name, author, and description")
        config.project_name = Prompt.ask("[cyan]Project name[/cyan]", default="my-devops-stack", console=self.console)
        config.project_description = Prompt.ask("[cyan]Short description[/cyan]", default="Scalable service with automated CI/CD", console=self.console)
        config.author = Prompt.ask("[cyan]Author / Organization[/cyan]", default="DevOps Team", console=self.console)
        config.output_dir = f"./{config.project_name}"

        # Step 2: Backend Framework
        self.console.print()
        print_section_header(self.console, 2, "Backend Architecture", "Core API / microservice server")
        backend_keys = list(BACKENDS.keys())
        for idx, key in enumerate(backend_keys, 1):
            info = BACKENDS[key]
            self.console.print(f"  [bold magenta][{idx}][/bold magenta] [bold bright_white]{info['name']}[/bold bright_white]\n      [bright_black]{info['description']}[/bright_black]")
        
        backend_idx = Prompt.ask(
            "\n[cyan]Select backend framework[/cyan]",
            choices=[str(i) for i in range(1, len(backend_keys) + 1)],
            default="1",
            console=self.console
        )
        config.backend = backend_keys[int(backend_idx) - 1]

        # Step 3: Frontend Framework
        self.console.print()
        print_section_header(self.console, 3, "Frontend User Interface", "Web application client or headless")
        frontend_keys = list(FRONTENDS.keys())
        for idx, key in enumerate(frontend_keys, 1):
            info = FRONTENDS[key]
            self.console.print(f"  [bold magenta][{idx}][/bold magenta] [bold bright_white]{info['name']}[/bold bright_white]\n      [bright_black]{info['description']}[/bright_black]")

        frontend_idx = Prompt.ask(
            "\n[cyan]Select frontend framework[/cyan]",
            choices=[str(i) for i in range(1, len(frontend_keys) + 1)],
            default="1",
            console=self.console
        )
        config.frontend = frontend_keys[int(frontend_idx) - 1]

        # Step 4: Database & Storage
        self.console.print()
        print_section_header(self.console, 4, "Data Persistence & Caching", "Primary database and session layer")
        db_keys = list(DATABASES.keys())
        for idx, key in enumerate(db_keys, 1):
            info = DATABASES[key]
            self.console.print(f"  [bold magenta][{idx}][/bold magenta] [bold bright_white]{info['name']}[/bold bright_white] [bright_black]— {info['description']}[/bright_black]")

        db_idx = Prompt.ask(
            "\n[cyan]Select database system[/cyan]",
            choices=[str(i) for i in range(1, len(db_keys) + 1)],
            default="1",
            console=self.console
        )
        config.database = db_keys[int(db_idx) - 1]

        # Step 5: CI/CD Pipeline Selection
        self.console.print()
        print_section_header(self.console, 5, "CI/CD Pipeline Automation", "Continuous integration and deployment engine")
        pipeline_keys = list(PIPELINES.keys())
        for idx, key in enumerate(pipeline_keys, 1):
            info = PIPELINES[key]
            self.console.print(f"  [bold magenta][{idx}][/bold magenta] [bold bright_white]{info['name']}[/bold bright_white]\n      [bright_black]{info['description']}[/bright_black]")

        pipe_idx = Prompt.ask(
            "\n[cyan]Select target CI/CD pipeline[/cyan]",
            choices=[str(i) for i in range(1, len(pipeline_keys) + 1)],
            default="1",
            console=self.console
        )
        config.pipeline = pipeline_keys[int(pipe_idx) - 1]

        # Step 6: DevOps Infrastructure & Tooling
        self.console.print()
        print_section_header(self.console, 6, "DevOps & Infrastructure As Code", "Containerization, orchestration, and monitoring")
        config.docker = Confirm.ask("[cyan]Generate Dockerfile & Docker Compose (dev + prod)?[/cyan]", default=True, console=self.console)
        config.k8s = Confirm.ask("[cyan]Generate Kubernetes Manifests (Deployments, Ingress, Services)?[/cyan]", default=True, console=self.console)
        if config.k8s:
            config.helm = Confirm.ask("[cyan]Generate Helm Chart packaging?[/cyan]", default=True, console=self.console)
        else:
            config.helm = False
        config.terraform = Confirm.ask("[cyan]Generate Terraform Cloud IaC scripts?[/cyan]", default=False, console=self.console)
        config.monitoring = Confirm.ask("[cyan]Include Prometheus & Grafana monitoring configuration?[/cyan]", default=True, console=self.console)
        config.include_tests = Confirm.ask("[cyan]Include pre-configured unit & integration test suites?[/cyan]", default=True, console=self.console)
        config.include_linter = Confirm.ask("[cyan]Include Linters, Formatters & Git Pre-commit Hooks?[/cyan]", default=True, console=self.console)

        return self._review_and_confirm(config)

    def _review_and_confirm(self, config: StackConfig) -> Optional[StackConfig]:
        """Displays summary, checks validation, and prompts final confirmation."""
        self.console.print()
        errors, warnings = ConfigValidator.validate(config)

        if errors:
            self.console.print(Panel(
                "\n".join([f"❌ {e}" for e in errors]),
                title="[bold red]Validation Errors[/bold red]",
                border_style="red"
            ))
            return None

        if warnings:
            self.console.print(Panel(
                "\n".join([f"⚠️  {w}" for w in warnings]),
                title="[bold yellow]Architecture Advisory Notices[/bold yellow]",
                border_style="yellow"
            ))

        print_summary_card(self.console, config.to_dict())

        # Option to save config preset
        if Confirm.ask("\n[cyan]Save this configuration to 'stackforge.json' for team reuse?[/cyan]", default=False, console=self.console):
            save_path = f"{config.project_name}.stackforge.json"
            config.save_to_file(save_path)
            self.console.print(f"[green]Saved preset specification to {save_path}[/green]")

        if Confirm.ask("\n[bold green]Ready to forge project files to disk?[/bold green]", default=True, console=self.console):
            return config
        else:
            self.console.print("[yellow]Generation cancelled.[/yellow]")
            return None
