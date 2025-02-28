import keyring
import click

SERVICE_NAME = "claude-code-py"

def get_api_key():
    """Retrieve or prompt for the Anthropic API key and store it securely."""
    api_key = keyring.get_password(SERVICE_NAME, "api_key")
    if not api_key:
        api_key = click.prompt("Enter your Anthropic API key", hide_input=True)
        keyring.set_password(SERVICE_NAME, "api_key", api_key)
    return api_key