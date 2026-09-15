"""
Theme and color styling definitions for StackForge CLI.
"""
from rich.theme import Theme

THEMES = {
    "cyberpunk": Theme({
        "info": "cyan bold",
        "warning": "yellow bold",
        "danger": "red bold",
        "success": "spring_green1 bold",
        "accent": "magenta bold",
        "subtle": "bright_black",
        "highlight": "bright_yellow bold",
        "header": "deep_pink1 bold",
        "pipeline": "cyan1",
        "stack": "chartreuse1",
    }),
    "matrix": Theme({
        "info": "green bold",
        "warning": "bright_green",
        "danger": "red bold",
        "success": "bright_green bold",
        "accent": "spring_green3",
        "subtle": "dark_green",
        "highlight": "green1 bold",
        "header": "green3 bold",
        "pipeline": "spring_green2",
        "stack": "chartreuse2",
    }),
    "nord": Theme({
        "info": "bright_blue bold",
        "warning": "yellow",
        "danger": "bright_red bold",
        "success": "bright_cyan bold",
        "accent": "bright_magenta",
        "subtle": "white",
        "highlight": "bright_white bold",
        "header": "steel_blue bold",
        "pipeline": "sky_blue2",
        "stack": "turquoise2",
    })
}

DEFAULT_THEME = "cyberpunk"
