# main.py
import click
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from api import query_anthropic
from tools import tools, execute_tool, SENSITIVE_TOOLS
from config import load_config  # Import load_config

console = Console()

def process_conversation(messages, approved_tools, model=None, max_tokens=None):
    """Handle a conversation turn, including tool calls."""
    try:
        while True:
            with console.status("[bold green]Processing...", spinner="dots"):
                try:
                    response = query_anthropic(messages, tools=tools, model=model, max_tokens=max_tokens)
                    assistant_message = {"role": "assistant", "content": response.content}
                    messages.append(assistant_message)
                    
                    # Display response
                    for block in response.content:
                        if block.type == "text":
                            console.print(Panel(block.text, title="Assistant", border_style="blue"))
                        elif block.type == "tool_use":
                            console.print(f"[bold yellow]Using tool:[/] {block.name}")
                    
                    # Handle tool uses
                    tool_uses = [block for block in response.content if block.type == "tool_use"]
                    if not tool_uses:
                        break
                    for tool_use in tool_uses:
                        result = execute_tool(tool_use.name, tool_use.input, approved_tools)
                        console.print(Panel(f"Tool result: {result}", title=f"Tool: {tool_use.name}", border_style="green"))
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use.id,
                                    "content": str(result)
                                }
                            ]
                        })
                except ValueError as e:
                    console.print(f"[red]Input Error:[/] {str(e)}")
                    break
                except RuntimeError as e:
                    console.print(f"[red]API Error:[/] {str(e)}")
                    break
                except Exception as e:
                    console.print(f"[red]Unexpected Error in Tool Execution:[/] {str(e)}")
                    break
    except Exception as e:
        console.print(f"[red]Conversation Error:[/] {str(e)}")

def run_repl(messages, approved_tools, model=None, max_tokens=None):
    """Run an interactive REPL session."""
    console.print(Panel("Welcome to OpenClaude!\nType /help for commands or /exit to quit.", title="OpenClaude", border_style="green"))
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/]", console=console, default="")
            if user_input.lower() == "/exit":
                console.print("[yellow]Goodbye![/]")
                break
            elif user_input.lower() == "/help":
                tool_list = "\n".join(f"- {tool['name']}: {tool['description']}" for tool in tools)
                console.print(Panel(
                    "Commands:\n- /exit: Exit the REPL\n- /help: Show this help\n- /permissions: Manage tool permissions\n\n"
                    "Available Tools:\n" + tool_list + "\n\n"
                    "Configuration: Edit config.json to set model, max_tokens, and default approved tools.",
                    title="Help", border_style="magenta"
                ))
            elif user_input.lower() == "/permissions":
                manage_permissions(approved_tools)
            else:
                messages.append({"role": "user", "content": user_input})
                process_conversation(messages, approved_tools, model, max_tokens)
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting REPL...[/]")
            break
        except Exception as e:
            console.print(f"[red]REPL Error:[/] {str(e)}")

def manage_permissions(approved_tools):
    """Allow users to view and modify approved tools."""
    console.print(Panel("Manage Permissions", title="Permissions", border_style="cyan"))
    console.print("Sensitive tools that can be pre-approved:")
    for tool in SENSITIVE_TOOLS:
        status = "Approved" if tool in approved_tools else "Not approved"
        console.print(f"- {tool}: {status}")
    console.print("\nTo approve a tool, type 'approve <tool_name>'")
    console.print("To revoke approval, type 'revoke <tool_name>'")
    console.print("Type 'done' to exit permissions menu")
    
    while True:
        action = Prompt.ask("[bold cyan]Permissions[/]", console=console, default="")
        if action.lower() == "done":
            break
        parts = action.split()
        if len(parts) == 2 and parts[0] in ["approve", "revoke"]:
            tool = parts[1]
            if tool not in SENSITIVE_TOOLS:
                console.print(f"[red]Error:[/] '{tool}' is not a sensitive tool")
                continue
            if parts[0] == "approve":
                if tool not in approved_tools:
                    approved_tools.append(tool)
                    console.print(f"[green]Approved:[/] {tool}")
                else:
                    console.print(f"[yellow]{tool} is already approved[/]")
            elif parts[0] == "revoke":
                if tool in approved_tools:
                    approved_tools.remove(tool)
                    console.print(f"[green]Revoked:[/] {tool}")
                else:
                    console.print(f"[yellow]{tool} is not approved[/]")
        else:
            console.print("[red]Invalid command. Use 'approve <tool>' or 'revoke <tool>'[/]")

@click.command()
@click.option('--model', help='Specify the Claude model to use')
@click.option('--max-tokens', type=int, help='Set the maximum number of tokens')
@click.option('-p', '--print', 'print_flag', is_flag=True, help='Run one-off query and exit')
@click.argument('query', required=False)
def claude(model, max_tokens, print_flag, query):
    """Python-based Claude Code for Windows."""
    config = load_config()
    approved_tools = [tool for tool in config.get("default_approved_tools", []) if tool in SENSITIVE_TOOLS]
    messages = []
    try:
        if query:
            user_message = {"role": "user", "content": query}
            if not sys.stdin.isatty():
                piped_input = sys.stdin.read()
                user_message["content"] = f"Piped input:\n{piped_input}\n\nQuery: {query}"
            messages.append(user_message)
            process_conversation(messages, approved_tools, model, max_tokens)
            if not print_flag:
                run_repl(messages, approved_tools, model, max_tokens)
        else:
            run_repl(messages, approved_tools, model, max_tokens)
    except Exception as e:
        console.print(f"[red]Startup Error:[/] {str(e)}")

if __name__ == "__main__":
    claude()