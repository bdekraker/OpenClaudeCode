import os
import subprocess
import click

# Define sensitive tools requiring permission
SENSITIVE_TOOLS = ["write_file", "run_command", "git_commit"]

tools = [
    {
        "name": "list_directory",
        "description": "Lists files and directories in the given path",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "read_file",
        "description": "Reads the content of the file",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Writes content to the file",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"]
        }
    },
    {
        "name": "run_command",
        "description": "Runs a shell command and returns the output",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]
        }
    },
    {
        "name": "git_status",
        "description": "Shows the current status of a git repository",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Path to git repository", "default": "."}},
            "required": []
        }
    },
    {
        "name": "git_commit",
        "description": "Commits staged changes with a message",
        "input_schema": {
            "type": "object",
            "properties": {"message": {"type": "string", "description": "Commit message"}},
            "required": ["message"]
        }
    },
    {
        "name": "search_files",
        "description": "Searches for a pattern in files within a directory",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Text to search for"},
                "path": {"type": "string", "description": "Directory to search", "default": "."}
            },
            "required": ["pattern"]
        }
    }
]

def execute_tool(tool_name, tool_input, approved_tools=None):
    """Execute the specified tool with given input, checking for permissions."""
    if approved_tools is None:
        approved_tools = []
    
    try:
        # Check permissions for sensitive tools
        if tool_name in SENSITIVE_TOOLS and tool_name not in approved_tools:
            if not click.confirm(f"Allow {tool_name} operation?"):
                return "Permission denied"
        
        if tool_name == "list_directory":
            path = tool_input["path"]
            if not os.path.isdir(path):
                return f"Error: '{path}' is not a directory"
            return "\n".join(os.listdir(path))
        elif tool_name == "read_file":
            path = tool_input["path"]
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        elif tool_name == "write_file":
            path = tool_input["path"]
            content = tool_input["content"]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"File '{path}' written successfully"
        elif tool_name == "run_command":
            command = tool_input["command"]
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = (result.stdout + result.stderr).strip()
            return output if output else "Command executed (no output)"
        elif tool_name == "git_status":
            path = tool_input.get("path", ".")
            if not os.path.isdir(path):
                return f"Error: '{path}' is not a directory"
            result = subprocess.run(["git", "-C", path, "status"], capture_output=True, text=True)
            output = (result.stdout + result.stderr).strip()
            return output if output else "No git status available"
        elif tool_name == "git_commit":
            message = tool_input["message"]
            if not message:
                return "Error: Commit message cannot be empty"
            # Check if there are staged changes
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if not status.stdout.strip():
                return "Error: No changes staged for commit"
            result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
            output = (result.stdout + result.stderr).strip()
            return output if output else "Commit successful"
        elif tool_name == "search_files":
            pattern = tool_input["pattern"]
            path = tool_input.get("path", ".")
            if not os.path.isdir(path):
                return f"Error: '{path}' is not a directory"
            results = []
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            for line_num, line in enumerate(f, 1):
                                if pattern in line:
                                    results.append(f"{file_path}:{line_num}: {line.strip()}")
                    except (UnicodeDecodeError, IOError):
                        continue  # Skip binary files or unreadable files
            return "\n".join(results) if results else f"No matches found for '{pattern}' in '{path}'"
        return f"Error: Unknown tool '{tool_name}'"
    except FileNotFoundError as e:
        return f"Error: File or directory not found - {str(e)}"
    except PermissionError:
        return "Error: Permission denied to access the resource"
    except subprocess.SubprocessError as e:
        return f"Error: Command failed - {str(e)}"
    except KeyError as e:
        return f"Error: Missing required input - {str(e)}"
    except Exception as e:
        return f"Error: An unexpected issue occurred - {str(e)}"