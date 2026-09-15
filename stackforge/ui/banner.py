"""
ASCII Art Banners, Headers, and Cards for StackForge CLI.
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from stackforge import __version__

BANNER_TEXT = r"""
  ___ _____ _   ___ _  _______ ___  ___  ____ ___ 
 / __|_   _/_\ / __| |/ / __/ _ \| _ \/ __| __| |
 \__ \ | |/ _ \ (__| ' <| _| (_) |   / (_ | _|| |
 |___/ |_/_/ \_\___|_|\_\_| \___/|_|_\\___|___|_|
"""

SUBTITLE = "» PRODUCTION-GRADE PROJECT ARCHITECTURE & DEVOPS PIPELINE FORGE «"

def get_banner_panel(theme_name: str = "cyberpunk") -> Panel:
    """Returns a rich styled panel containing the ASCII logo and system tags."""
    text = Text()
    text.append(BANNER_TEXT, style="bold magenta")
    text.append("\n" + SUBTITLE.center(56) + "\n", style="cyan bold")
    text.append(f"  v{__version__}  |  Garvit Agarwal Edition  |  Zero-Config Scaffolding\n", style="bright_black italic")

    badge_table = Table.grid(padding=(0, 1))
    badge_table.add_row(
        Text("[Backends: FastAPI | Express | Go | Rust | Django]", style="spring_green1"),
        Text("[CI/CD: GitHub | GitLab | Azure | Jenkins]", style="cyan1"),
    )
    badge_table.add_row(
        Text("[Frontends: React | Next.js | Vue | Svelte]", style="deep_pink1"),
        Text("[DevOps: Docker | K8s | Helm | Terraform]", style="bright_yellow"),
    )

    content = Table.grid(padding=0)
    content.add_row(Align.center(text))
    content.add_row(Align.center(badge_table))

    return Panel(
        content,
        border_style="bright_magenta",
        padding=(0, 2),
        title="[bold bright_white on magenta] STACKFORGE CLI [/bold bright_white on magenta]",
        subtitle="[bright_black]Type Ctrl+C at any time to exit[/bright_black]"
    )

def print_banner(console: Console, theme_name: str = "cyberpunk"):
    """Render the main banner to the terminal console."""
    console.print(get_banner_panel(theme_name))
    console.print()

def print_section_header(console: Console, step_num: int, title: str, description: str):
    """Render a clean step header."""
    header_text = Text()
    header_text.append(f" STEP {step_num} ", style="bold black on cyan")
    header_text.append(f" {title.upper()} ", style="bold bright_white")
    header_text.append(f"— {description}", style="bright_black")
    console.print(header_text)
    console.print()

def print_summary_card(console: Console, config_dict: dict):
    """Display configured stack summary before generation."""
    table = Table(title="[bold cyan]Target Project Configuration Specification[/bold cyan]", border_style="cyan")
    table.add_column("Category", style="bold magenta", width=22)
    table.add_column("Selection", style="bright_green", width=35)
    table.add_column("DevOps Artifacts Generated", style="bright_white")

    table.add_row("Project Name", config_dict.get("project_name", "my-project"), "Directory root & metadata")
    table.add_row("Backend Framework", config_dict.get("backend", "None"), "API server, models, healthcheck")
    table.add_row("Frontend Framework", config_dict.get("frontend", "None"), "UI app, client-side routing, assets")
    table.add_row("Database / ORM", config_dict.get("database", "None"), "Schema, migration scripts, container")
    table.add_row("CI/CD Pipeline", config_dict.get("pipeline", "None"), "Automated workflow configs")
    table.add_row("Containerization", "Docker & Compose" if config_dict.get("docker", True) else "Disabled", "Dockerfile & multi-service compose")
    table.add_row("Kubernetes / Helm", "Included" if config_dict.get("k8s", False) else "Disabled", "Deployments, Services, Ingress, Helm Chart")
    table.add_row("Terraform IaC", "Included" if config_dict.get("terraform", False) else "Disabled", "Cloud infrastructure provisioning")
    table.add_row("Testing & Quality", "Pre-configured", "Linters, test runners, pre-commit hooks")

    console.print(Panel(table, border_style="cyan", padding=(0, 1)))
