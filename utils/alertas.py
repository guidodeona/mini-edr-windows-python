from rich.console import Console
from rich.theme import Theme
from .logger import log_event

# Tema personalizado para una estética "Cyberpunk/Pro"
custom_theme = Theme({
    "info": "cyan",
    "warning": "bold yellow",
    "danger": "bold red blink",
    "success": "bold green",
    "header": "bold magenta underline",
    "panel": "blue"
})

console = Console(theme=custom_theme)

def print_alert(msg, level="info"):
    """
    Imprime una alerta estilizada usando Rich y registra el evento.
    """
    icons = {
        "info": "ℹ️ ",
        "warning": "⚠️ ",
        "danger": "🚨 ",
        "success": "✅ "
    }
    
    icon = icons.get(level, "")
    # Usamos el estilo definido en el tema
    console.print(f"{icon} [{level}]{msg}[/{level}]")
    
    log_event(msg)

def get_console():
    return console
