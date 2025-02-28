# OpenClaudeCode

**OpenClaudeCode** is a simple yet powerful Python tool that brings Anthropic's Claude AI to your terminal. Think of it as your personal coding assistant! You can ask it questions, run commands, manage files, or even handle Git tasks—all from a command-line interface (CLI) or an interactive session (REPL). Whether you're a developer or just curious about AI, OpenClaudeCode makes it easy to get started.



https://github.com/user-attachments/assets/a8ae2d40-50d7-42fe-a7bf-4a139d5993b7



---

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
  - [Interactive REPL](#interactive-repl)
  - [Examples](#examples)
- [Permissions](#permissions)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

![image](https://github.com/user-attachments/assets/98812858-5dfc-47d9-8601-6c616244e096)


## Installation

Getting OpenClaudeCode up and running is straightforward. Here’s how:

1. **Clone the Repository**:  
   Open your terminal and type:
   ```bash
   git clone https://github.com/bdekraker/OpenClaudeCode.git
   ```
2. **Navigate to the Project Folder**:
   ```bash
   cd OpenClaudeCode
   ```
3. **Install Required Libraries**:  
   Make sure you have Python 3.6 or higher installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If there’s no requirements.txt yet, install these packages: anthropic, keyring, click, and rich.*

4. **Set Up Your Anthropic API Key**:  
   The first time you run OpenClaudeCode, it will ask for your Anthropic API key. Enter it when prompted—it’ll be saved securely so you won’t need to type it again.

---

## Configuration

OpenClaudeCode uses a file called `config.json` to store settings. You can tweak these to suit your needs:

- **model**: The Claude model to use (e.g., `"claude-3-5-sonnet-20240620"`).
- **max_tokens**: How long the AI’s responses can be (e.g., `1000`).
- **default_approved_tools**: Tools you’re okay with running without extra confirmation (e.g., `["write_file"]`).

Example `config.json`:

```json
{
    "model": "claude-3-5-sonnet-20240620",
    "max_tokens": 1000,
    "default_approved_tools": ["read_file"]
}
```

If you don’t create this file, OpenClaudeCode will use default settings (a specific Claude model, 1000 tokens, and no pre-approved tools).

---

## Usage

You can use OpenClaudeCode in two ways: quick commands via the CLI or an interactive REPL for ongoing chats.


### Interactive REPL

Start an interactive session by running:

```bash
python main.py
```

You’ll see a welcome message, and then you can type commands or questions.

REPL Commands:

- `/help`: See a list of tools and tips.
- `/permissions`: Control which tools can run automatically.
- `/exit`: Quit the session.


### Command-Line Interface

Run a single command like this:

```bash
python main.py "show me the files in this folder"
```

The AI will respond and then exit.

Extra Options:

- `--model`: Pick a different Claude model (e.g., `--model claude-3-7-sonnet-latest`).
- `--max-tokens`: Limit response length (e.g., `--max-tokens 500`).
- `-p` or `--print`: Run the command and exit without opening the REPL.

  ![image](https://github.com/user-attachments/assets/3247afaf-ad15-484f-b550-eb7f4a42e7f7)


### Examples

Here are some things you can do with OpenClaudeCode:

- **List Files**:  
  *Type*: `list files in this folder`  
  *Output*: A list of files and folders in your current directory.

- **Read a File**:  
  *Type*: `read the content of notes.txt`  
  *Output*: The text inside `notes.txt`.

- **Write to a File**:  
  *Type*: `write "Hello, OpenClaudeCode!" to hello.txt`  
  If `write_file` isn’t pre-approved, it’ll ask for permission first.

- **Run a Command**:  
  *Type*: `run the command "echo Hi there"`  
  *Output*: `Hi there` (or whatever the command returns).

- **Check Git Status**:  
  *Type*: `show git status`  
  *Output*: The current status of your Git repository.

- **Search Files**:  
  *Type*: `search for "error" in this folder`  
  *Output*: Lines containing “error” from files in the folder, with file names and line numbers.

---

## Permissions

Some actions (like writing files or running commands) are “sensitive” because they change things on your computer. OpenClaudeCode will ask for your approval unless you pre-approve them.

### How to Manage Permissions

- **Pre-Approve**: Add tools to `default_approved_tools` in `config.json`.
- **In the REPL**:
  - Type `/permissions`
  - Then: approve `write_file` (or revoke `write_file`)
  - Type `done` to finish.

---

## Troubleshooting

- **“Invalid API Key”**: Double-check your Anthropic API key when prompted.
- **Tool Fails**: Make sure files or paths exist (e.g., `notes.txt` for reading).
- **Config Issues**: If `config.json` doesn’t work, delete it to reset to defaults.

Need more help? Visit the [GitHub Issues](https://github.com/bdekraker/OpenClaudeCode/issues) page.

---

## Contributing

Love OpenClaudeCode and want to help? Here’s how:

1. Fork this repository.
2. Create a branch:
   ```bash
   git checkout -b my-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Added cool feature"
   ```
4. Push it:
   ```bash
   git push origin my-feature
   ```
5. Open a pull request on GitHub.

---

## License

This project is licensed under the **GNU GENERAL PUBLIC LICENSE (GPL)**. See the [LICENSE](LICENSE) file for details.

---


