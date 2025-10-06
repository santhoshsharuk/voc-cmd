# ===================================================================
#           VOXCMD - FINAL VERSION WITH SYNTAX FIX
# ===================================================================
import os
import sys
import json
import shutil
import typer
import subprocess
from pathlib import Path
from typing import List

# AI Import
import google.generativeai as genai

# Rich Import for beautiful terminal output
from rich.console import Console
from rich.markdown import Markdown

# NEW: Import the codecs library to fix the newline issue
import codecs

# Typer App Initialization
app = typer.Typer(
    help="A powerful AI assistant and file manager for your terminal, powered by Gemini 1.5 Flash."
)

# JSON Configuration File Setup
CONFIG_DIR = Path.home() / ".voxcmd"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Initialize the rich console
console = Console()


def get_gemini_client():
    # ... (This function remains unchanged)
    if not CONFIG_FILE.exists():
        typer.secho("ERROR: Gemini API key not found.", fg=typer.colors.RED)
        typer.echo("Please set your key using the command:")
        typer.secho("  voxcmd set-api-key YOUR_API_KEY", fg=typer.colors.YELLOW)
        return None
    try:
        with open(str(CONFIG_FILE), "r") as f: data = json.load(f)
        api_key = data.get("api_key")
        if not api_key:
            typer.secho("ERROR: 'api_key' not found in the config file.", fg=typer.colors.RED); return None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        return model
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED); return None


# --- COMMANDS ---

@app.command()
def set_api_key(api_key: str = typer.Argument(..., help="Your Google Gemini API key.")):
    # ... (This function remains unchanged)
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {"api_key": api_key}
        with open(str(CONFIG_FILE), "w") as f: json.dump(data, f, indent=4)
        typer.secho(f"✅ API key saved successfully to {CONFIG_FILE}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ Failed to save API key: {e}", fg=typer.colors.RED)


# --- UPDATED create-file COMMAND ---
@app.command("create-file")
def create_file(
    filepath: Path = typer.Argument(..., help="The full path for the new file (e.g., 'app.py')."),
    content: str = typer.Option("", "--content", "-c", help="The content to write into the file.")
):
    """
    Creates a new file and writes content to it. Decodes escape sequences like \\n.
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # --- THE FIX ---
        # Decode the content string to process escape sequences like '\n' into real newlines.
        decoded_content = codecs.decode(content, 'unicode_escape')
        
        filepath.write_text(decoded_content, encoding='utf-8')
        
        typer.secho(f"✅ Successfully created file: {filepath}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ Failed to create file: {e}", fg=typer.colors.RED)


@app.command()
def ask(query: List[str] = typer.Argument(..., help="Your request in natural language.")):
    # ... (This function remains unchanged, its prompt is already correct)
    full_query = " ".join(query)
    model = get_gemini_client()
    if not model: raise typer.Exit()
    prompt = f"""
    You are 'Vox', a powerful AI assistant in a CLI called 'voxcmd'.
    You have two modes: Conversational and Command Translation.

    1. **Command Translation Mode:** If the user's request can be fulfilled by a `voxcmd` command, your ONLY output MUST be the precise command.

    2. **Conversational Mode:** For any other request, your response MUST start with `CHAT: ` followed by a Markdown-formatted answer.

    **Available `voxcmd` commands:**
    - `hello <name> [--times NUMBER]`
    - `goodbye`
    - `view <filepath>`
    - `delete <path>`
    - `open-path <path>`
    - `find <name>`
    - `create-file <filepath> --content "..."`

    **CRITICAL EXAMPLES:**
    User request: "create a python file called app.py that prints hello"
    Your output: create-file app.py --content "print('Hello, World!')"

    User request: "what is python"
    Your output: CHAT: Python is a high-level, interpreted programming language...
    ---
    Now, process the following user request: "{full_query}"
    Your output:
    """
    with console.status("🤖 Thinking with Gemini 1.5 Flash...", spinner="dots"):
        response = model.generate_content(prompt)
    generated_text = response.text.strip()

    if generated_text.startswith("CHAT:"):
        chat_content = generated_text.lstrip("CHAT: ").strip()
        console.print(Markdown(chat_content))
    else:
        generated_command = generated_text
        typer.echo("✨ AI suggests this command:")
        console.print(Markdown(f"```bash\n{generated_command}\n```"))
        execute = typer.confirm("\nDo you want to execute this command?")
        if not execute:
            typer.echo("Execution cancelled."); raise typer.Exit()
        try:
            subprocess.run(f"voxcmd {generated_command}", shell=True, check=True)
        except Exception as e:
            typer.secho(f"\nAn error occurred during execution: {e}", fg=typer.colors.RED)

# --- Other commands are unchanged ---
@app.command()
def hello(name: str, times: int = typer.Option(1, "--times", "-t")): typer.echo(f"Hello, {name}!")
@app.command()
def goodbye(): typer.echo("Goodbye!")
@app.command()
def view(filepath: Path): typer.echo(filepath.read_text(encoding='utf-8'))
@app.command()
def delete(path: Path):
    if not path.exists(): typer.secho(f"Error: Path '{path}' does not exist.", fg=typer.colors.RED); raise typer.Exit(1)
    target_type = "directory" if path.is_dir() else "file"
    if typer.confirm(f"Are you sure you want to delete the {target_type} '{path}'?"):
        if path.is_dir(): shutil.rmtree(path)
        else: path.unlink()
        typer.echo(f"{target_type.capitalize()} '{path}' has been deleted.")
@app.command("open-path")
def open_path(path: Path):
    if sys.platform == "win32": os.startfile(path)
    else: subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", path], check=True)
@app.command()
def find(name: str):
    found_paths = list(Path('.').glob(f'**/{name}'))
    if not found_paths: typer.echo("No matching files or directories found."); return
    typer.secho("Found paths:", fg=typer.colors.GREEN)
    for p in found_paths: typer.echo(f"- {p}{' [DIR]' if p.is_dir() else ''}")

if __name__ == "__main__":
    app()