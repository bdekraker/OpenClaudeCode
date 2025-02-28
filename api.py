from anthropic import Anthropic
from auth import get_api_key
from config import load_config  # Import load_config to access configuration

config = load_config()  # Load configuration at module level

def query_anthropic(messages, tools=None, model=None, max_tokens=None):
    """Send messages to the Anthropic API and return the response.

    Args:
        messages: A list of message dictionaries to send to the API.
        tools: Optional list of tools to include in the request.
        model: Optional string specifying the Anthropic model to use; defaults to config value.
        max_tokens: Optional integer specifying the maximum tokens; defaults to config value.

    Returns:
        The API response object.

    Raises:
        ValueError: If the messages input is invalid.
        RuntimeError: If the API request fails (e.g., network or authentication issues).
    """
    try:
        # Input validation
        if not messages or not isinstance(messages, list):
            raise ValueError("Messages must be a non-empty list")
        
        # Initialize the client with the API key
        client = Anthropic(api_key=get_api_key())
        
        # Use provided values or fall back to configuration defaults
        selected_model = model or config.get("model", "claude-3-5-sonnet-20240620")
        selected_max_tokens = max_tokens or config.get("max_tokens", 1000)
        
        # Send the request to the Anthropic API
        response = client.messages.create(
            model=selected_model,
            messages=messages,
            tools=tools,
            max_tokens=selected_max_tokens,
        )
        return response
    
    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"API request failed: {str(e)}")