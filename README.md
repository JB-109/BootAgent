# BootAgent

**BootAgent** is an AI-powered coding assistant that uses Google's Gemini API to autonomously interact with your codebase through function calling.

## What It Does

- 📂 Reads and analyzes files in your project
- ✍️ Writes and modifies code files
- ▶️ Executes Python scripts
- 🤖 Uses AI to understand your requests and take appropriate actions

## Installation

```bash
# Install dependencies
uv sync

# Create .env file from example
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

## Configuration

Create a `.env` file with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

```bash
uv run main.py "your prompt here"
```

### Interactive Mode

```bash
uv run main.py
```

You'll be prompted to enter your request.

### Verbose Mode

```bash
uv run main.py "your prompt" --verbose
```

Shows detailed function calls and token usage.

## Examples

```bash
# List files in the working directory
uv run main.py "get all the files info in the working directory"

# Calculate using existing functions
uv run main.py "what is the 100th fibonacci number, calculate using the provided functions"

# Create or modify code
uv run main.py "create a function to calculate factorial"
```

## How It Works

1. You provide a prompt (via command line or interactively)
2. The AI analyzes your request and decides which functions to call
3. Functions execute and return results
4. The AI processes results and provides a response
5. The loop continues until the task is complete (max 15 iterations)

## Available Functions

- `get_files_info` - List files and directories
- `get_file_content` - Read file contents
- `run_python_file` - Execute Python scripts
- `write_files` - Create or modify files

## Project Structure

```
BootAgent/
├── main.py              # Entry point and orchestration loop
├── config.py            # System prompt configuration
├── functions/           # Function implementations and schemas
├── calculator/          # Working directory for AI operations
└── .env                 # API key configuration
```

## License

MIT
