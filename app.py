from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
from rich.columns import Columns
from rich.rule import Rule
from rich import box
import json
import sys
import os

from agent.graph import ask
from agent.parser import parse_tool_call
from tools.dispatcher import execute
from tools.browser import search
from config import set_model, list_models, get_model, MODELS

console = Console()
history = []

# Set to True to see tool calls and their outputs
VERBOSE = False


def print_banner():
    """Print the startup banner."""
    banner_text = Text()
    banner_text.append("AI Agent", style="bold bright_cyan")
    banner_text.append(" v0.8", style="dim")

    banner = Panel(
        banner_text,
        subtitle=f"[dim]Model: {get_model()}[/dim]",
        box=box.DOUBLE,
        border_style="bright_cyan",
        padding=(0, 2),
    )
    console.print(banner)
    console.print()


def print_help():
    """Print available commands."""
    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        box=box.SIMPLE_HEAVY,
        border_style="dim",
    )
    table.add_column("Command", style="bold yellow")
    table.add_column("Description", style="white")

    table.add_row("/model <name>", "Switch model (fast, heavy, reason, or full name)")
    table.add_row("/models", "List available models and presets")
    table.add_row("/search <query>", "Search the internet directly")
    table.add_row("/verbose", "Toggle tool call visibility")
    table.add_row("/clear", "Clear conversation history")
    table.add_row("/help", "Show this help message")
    table.add_row("/exit", "Exit the agent")

    console.print(table)
    console.print()


def print_search_results(query: str, results: dict):
    """Display search results in a styled table."""
    if not results.get("success"):
        console.print(f"[red]✗ Search failed:[/red] {results.get('error', 'Unknown error')}\n")
        return

    items = results.get("results", [])

    if not items:
        console.print("[yellow]No results found.[/yellow]\n")
        return

    table = Table(
        title=f"🔍 Search: {query}",
        show_header=True,
        header_style="bold bright_cyan",
        box=box.ROUNDED,
        border_style="dim",
        show_lines=True,
        padding=(0, 1),
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="bold white", max_width=50)
    table.add_column("URL", style="dim cyan", max_width=40)

    for i, item in enumerate(items, 1):
        title = item.get("title", "")[:50]
        url = item.get("url", "")[:40]
        table.add_row(str(i), title, url)

    console.print(table)

    # Show snippets below
    console.print()
    for i, item in enumerate(items, 1):
        snippet = item.get("snippet", "")
        if snippet:
            console.print(f"  [bold]{i}.[/bold] {snippet[:150]}")
            console.print()


def print_tool_activity(tool_call: dict):
    """Show a minimal one-line indicator of tool activity."""
    tool_name = tool_call.get("tool", "unknown")
    detail = ""

    if tool_name == "terminal":
        detail = tool_call.get("command", "")
    elif tool_name == "read_file":
        detail = tool_call.get("path", "")
    elif tool_name == "write_file":
        detail = tool_call.get("path", "")
    elif tool_name == "search":
        detail = tool_call.get("query", "")
    elif tool_name == "browse":
        detail = tool_call.get("url", "")
    elif tool_name in ("git_commit", "git_checkout", "git_branch"):
        detail = tool_call.get("message", "") or tool_call.get("branch", "") or tool_call.get("name", "")
    elif tool_name == "git_push":
        detail = f"{tool_call.get('remote', 'origin')}/{tool_call.get('branch', '')}"
    else:
        detail = ""

    if detail:
        console.print(f"  [dim]⚡ {tool_name}:[/dim] [dim italic]{detail}[/dim italic]")
    else:
        console.print(f"  [dim]⚡ {tool_name}[/dim]")


def print_tool_call(tool_call: dict):
    """Display a tool call in a styled panel (verbose mode)."""
    tool_name = tool_call.get("tool", "unknown")

    display = dict(tool_call)
    if "content" in display and len(str(display["content"])) > 200:
        display["content"] = str(display["content"])[:200] + "..."

    json_str = json.dumps(display, indent=2)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)

    panel = Panel(
        syntax,
        title=f"[bold yellow]⚡ Tool Call: {tool_name}[/bold yellow]",
        border_style="yellow",
        box=box.ROUNDED,
        padding=(0, 1),
    )
    console.print(panel)


def print_tool_output(output: dict):
    """Display tool output in a styled panel (verbose mode)."""
    success = output.get("success", False)
    style = "green" if success else "red"
    icon = "✓" if success else "✗"

    display = dict(output)
    for key, value in display.items():
        if isinstance(value, str) and len(value) > 1000:
            display[key] = value[:1000] + "\n... (truncated)"

    json_str = json.dumps(display, indent=2, default=str)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)

    panel = Panel(
        syntax,
        title=f"[bold {style}]{icon} Output[/bold {style}]",
        border_style=style,
        box=box.ROUNDED,
        padding=(0, 1),
    )
    console.print(panel)


def print_ai_response(text: str):
    """Display AI response in a styled panel."""
    panel = Panel(
        Markdown(text),
        title="[bold bright_cyan]🤖 AI[/bold bright_cyan]",
        border_style="bright_cyan",
        box=box.ROUNDED,
        padding=(0, 1),
    )
    console.print(panel)


def print_models_info():
    """Display model information."""
    info = list_models()

    table = Table(
        title="Model Configuration",
        show_header=True,
        header_style="bold bright_cyan",
        box=box.ROUNDED,
        border_style="dim",
    )
    table.add_column("Preset", style="bold yellow")
    table.add_column("Model", style="white")
    table.add_column("Status", style="dim")

    active = info.get("active", "")
    installed = info.get("models", [])

    for preset, model in info.get("presets", MODELS).items():
        is_active = "● active" if model == active else ""
        is_installed = "✓ installed" if any(model in m for m in installed) else "✗ not pulled"
        status = is_active if is_active else is_installed
        status_style = "bold green" if is_active else ("green" if "installed" in status else "red")
        table.add_row(preset, model, f"[{status_style}]{status}[/{status_style}]")

    console.print(table)

    if installed:
        console.print(f"\n[dim]All installed models:[/dim]")
        for m in installed:
            marker = " [bold green]●[/bold green]" if m == active or active in m else "  "
            console.print(f"  {marker} {m}")
    console.print()


def handle_command(user_input: str) -> bool:
    """Handle slash commands. Returns True if should continue loop."""
    global VERBOSE
    cmd = user_input.strip().lower()

    if cmd in ("/exit", "/quit", "/q"):
        console.print("\n[dim]Goodbye! 👋[/dim]\n")
        sys.exit(0)

    elif cmd == "/clear":
        history.clear()
        console.print("[green]✓ History cleared.[/green]\n")
        return True

    elif cmd == "/help":
        print_help()
        return True

    elif cmd == "/verbose":
        VERBOSE = not VERBOSE
        state = "ON" if VERBOSE else "OFF"
        console.print(f"[green]✓ Verbose mode:[/green] [bold]{state}[/bold]\n")
        return True

    elif cmd == "/models":
        print_models_info()
        return True

    elif cmd.startswith("/model "):
        name = user_input.strip()[7:].strip()
        new_model = set_model(name)
        console.print(f"[green]✓ Switched to:[/green] [bold]{new_model}[/bold]\n")
        return True

    elif cmd.startswith("/search "):
        query = user_input.strip()[8:].strip()
        if not query:
            console.print("[red]Usage:[/red] /search <query>\n")
            return True

        with console.status("[bold bright_cyan]Searching...[/bold bright_cyan]", spinner="dots"):
            results = search(query)

        print_search_results(query, results)
        return True

    elif cmd == "/search":
        console.print("[red]Usage:[/red] /search <query>\n")
        return True

    else:
        console.print("[red]Unknown command.[/red] Type [bold]/help[/bold] for available commands.\n")
        return True

    return False


def get_user_input() -> str:
    """Get input from user with styled prompt."""
    try:
        console.print()
        user = console.input("[bold bright_green]You >[/bold bright_green] ")
        return user
    except (KeyboardInterrupt, EOFError):
        console.print("\n\n[dim]Goodbye! 👋[/dim]\n")
        sys.exit(0)


def run_agent_loop(user_message: str):
    """Run the agent tool-calling loop."""
    history.append({
        "role": "user",
        "content": user_message
    })

    while True:
        # Show thinking spinner
        with console.status("[bold bright_cyan]Thinking...[/bold bright_cyan]", spinner="dots"):
            reply = ask(history)

        tool = parse_tool_call(reply)

        # AI answered normally (no tool call)
        if tool is None:
            print_ai_response(reply)
            history.append({
                "role": "assistant",
                "content": reply
            })
            break

        # AI wants to call a tool
        if VERBOSE:
            print_tool_call(tool)
        else:
            print_tool_activity(tool)

        # Execute the tool with spinner
        with console.status("[bold yellow]Executing...[/bold yellow]", spinner="dots2"):
            output = execute(tool)

        if VERBOSE:
            print_tool_output(output)

        # Add to history and continue the loop
        history.append({
            "role": "assistant",
            "content": reply
        })

        history.append({
            "role": "user",
            "content": f"""
The requested tool has already been executed.

Tool Output:

{json.dumps(output, indent=4)}

If the task is complete,
respond normally.

Otherwise call another tool.
"""
        })


def main():
    """Main entry point."""
    os.system("cls" if os.name == "nt" else "clear")

    print_banner()
    print_help()

    console.print(Rule(style="dim"))
    console.print()

    while True:
        user_input = get_user_input()

        if not user_input.strip():
            continue

        # Handle slash commands
        if user_input.strip().startswith("/"):
            handle_command(user_input)
            continue

        # Run the agent
        console.print()
        run_agent_loop(user_input)


if __name__ == "__main__":
    main()
