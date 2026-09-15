"""
File tree visualizer, syntax highlighter, and completion reporter for StackForge CLI.
"""
from typing import Dict, List
import os
from rich.console import Console
from rich.tree import Tree
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from stackforge.core.config import StackConfig

def display_file_tree(console: Console, file_dict: Dict[str, str], root_name: str = "project"):
    """
    Renders a directory tree from a dictionary of file paths {relative_path: content}.
    """
    root_tree = Tree(f"[bold cyan]📁 {root_name}/[/bold cyan]")
    dir_nodes = {"": root_tree}

    # Sort paths so folders appear organized
    sorted_paths = sorted(file_dict.keys())

    for path in sorted_paths:
        parts = path.replace("\\", "/").split("/")
        current_path = ""
        current_node = root_tree

        for i, part in enumerate(parts):
            parent_path = current_path
            current_path = f"{current_path}/{part}" if current_path else part

            if i == len(parts) - 1:
                # File
                icon = "📄"
                color = "bright_white"
                if part.endswith((".yml", ".yaml")):
                    icon = "⚡"
                    color = "bright_yellow"
                elif part.endswith((".py", ".ts", ".js", ".go", ".rs", ".java")):
                    icon = "💻"
                    color = "spring_green1"
                elif "docker" in part.lower():
                    icon = "🐳"
                    color = "sky_blue2"
                elif part.endswith(".tf"):
                    icon = "☁️"
                    color = "bright_magenta"
                elif part.endswith(".md"):
                    icon = "📝"
                    color = "bright_cyan"

                current_node.add(f"[{color}]{icon} {part}[/{color}]")
            else:
                # Directory
                if current_path not in dir_nodes:
                    new_dir_node = current_node.add(f"[bold blue]📁 {part}/[/bold blue]")
                    dir_nodes[current_path] = new_dir_node
                    current_node = new_dir_node
                else:
                    current_node = dir_nodes[current_path]

    console.print(Panel(root_tree, title="[bold green]📦 Generated Architecture Blueprint[/bold green]", border_style="green"))

def preview_key_file(console: Console, relative_path: str, content: str):
    """
    Renders syntax-highlighted preview of a generated file.
    """
    ext = os.path.splitext(relative_path)[1].lstrip(".")
    lexer_map = {
        "yml": "yaml",
        "yaml": "yaml",
        "py": "python",
        "ts": "typescript",
        "js": "javascript",
        "go": "go",
        "rs": "rust",
        "tf": "terraform",
        "json": "json",
        "md": "markdown",
        "sh": "bash",
    }
    lexer = lexer_map.get(ext, "yaml" if "dockerfile" in relative_path.lower() else "text")

    # Limit preview length for terminal comfort
    lines = content.splitlines()
    preview_content = "\n".join(lines[:45])
    if len(lines) > 45:
        preview_content += f"\n\n# ... [{len(lines) - 45} more lines omitted for preview] ..."

    syntax = Syntax(preview_content, lexer, theme="monokai", line_numbers=True, word_wrap=True)
    console.print(Panel(
        syntax,
        title=f"[bold yellow]🔍 Preview: {relative_path}[/bold yellow]",
        subtitle="[bright_black]Live Syntax Highlighted[/bright_black]",
        border_style="yellow"
    ))

def print_next_steps(console: Console, config: StackConfig, target_dir: str):
    """
    Outputs quick start commands for the developer to run immediately.
    """
    title_text = Text("🚀 Project Generated Successfully!", style="bold spring_green1")
    
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bright_magenta bold", width=18)
    table.add_column(style="bright_white")

    table.add_row("Target Directory:", f"[cyan]{os.path.abspath(target_dir)}[/cyan]")
    table.add_row("Stack Profile:", f"[yellow]{config.backend}[/yellow] + [yellow]{config.frontend}[/yellow] + [yellow]{config.database}[/yellow]")
    table.add_row("CI/CD Pipeline:", f"[spring_green1]{config.pipeline}[/spring_green1]")

    steps_text = Text()
    steps_text.append("\nRun the following commands to kick off your project:\n\n", style="bold bright_white")
    steps_text.append(f"  1. Navigate to directory:\n     ", style="dim")
    steps_text.append(f"cd {config.project_name}\n\n", style="bold cyan")

    if config.docker:
        steps_text.append(f"  2. Start local containers (Database, Backend, Services):\n     ", style="dim")
        steps_text.append("docker compose up -d\n\n", style="bold cyan")

    steps_text.append(f"  3. Initialize Git and commit starter code:\n     ", style="dim")
    steps_text.append("git init && git add . && git commit -m \"feat: initial architecture scaffold via StackForge\"\n\n", style="bold cyan")

    if config.backend == "fastapi":
        steps_text.append(f"  4. Launch Python Backend locally:\n     ", style="dim")
        steps_text.append("cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload\n\n", style="bold cyan")
    elif config.backend == "express_ts":
        steps_text.append(f"  4. Launch Express TypeScript Backend locally:\n     ", style="dim")
        steps_text.append("cd backend && npm install && npm run dev\n\n", style="bold cyan")
    elif config.backend == "go_gin":
        steps_text.append(f"  4. Launch Go Backend:\n     ", style="dim")
        steps_text.append("cd backend && go run main.go\n\n", style="bold cyan")
    elif config.backend == "rust_axum":
        steps_text.append(f"  4. Launch Rust Service:\n     ", style="dim")
        steps_text.append("cd backend && cargo run\n\n", style="bold cyan")

    if config.frontend not in ("none", ""):
        steps_text.append(f"  5. Launch Frontend UI:\n     ", style="dim")
        steps_text.append("cd frontend && npm install && npm run dev\n\n", style="bold cyan")

    content = Table.grid()
    content.add_row(table)
    content.add_row(steps_text)

    console.print()
    console.print(Panel(
        content,
        title="[bold black on spring_green1] SUCCESS [/bold black on spring_green1]",
        border_style="spring_green1",
        padding=(1, 2)
    ))
