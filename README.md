# VoxCmd

A powerful AI assistant and file manager for your terminal, powered by Google Gemini 1.5 Flash.

## Features

- 🤖 **AI-Powered Assistant**: Chat with AI or get command suggestions
- 📁 **File Management**: Create, view, delete, and find files easily
- 🚀 **Natural Language Commands**: Describe what you want, get the right command
- 🎨 **Rich Terminal Output**: Beautiful formatting with Rich library
- ⚡ **Fast and Lightweight**: Built with Typer for optimal performance

## Installation

```bash
pip install voxcmd
```

## Quick Start

1. **Set your Gemini API key**:
   ```bash
   voxcmd set-api-key YOUR_GEMINI_API_KEY
   ```

2. **Start using VoxCmd**:
   ```bash
   # Ask the AI anything
   voxcmd ask "create a python file that prints hello world"
   
   # View files
   voxcmd view myfile.txt
   
   # Create files directly
   voxcmd create-file app.py --content "print('Hello World!')"
   ```

## Available Commands

- `voxcmd ask "your question"` - Ask the AI assistant anything
- `voxcmd set-api-key <key>` - Configure your Gemini API key
- `voxcmd create-file <path> --content "..."` - Create files with content
- `voxcmd view <filepath>` - Display file contents
- `voxcmd delete <path>` - Delete files or directories
- `voxcmd find <name>` - Find files by name
- `voxcmd open-path <path>` - Open files/directories in default application
- `voxcmd hello <name>` - Say hello (example command)
- `voxcmd goodbye` - Say goodbye

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Use it with `voxcmd set-api-key YOUR_KEY`

## Development & Release Process

This project uses automated publishing to PyPI via GitHub Actions.

### For Maintainers

**Releasing a new version:**

1. Update the version number in `pyproject.toml`
2. Commit your changes: `git commit -am "Release v1.x.x"`
3. Create and push a version tag: 
   ```bash
   git tag v1.x.x
   git push origin v1.x.x
   ```
4. The GitHub Action will automatically build and publish to PyPI

**Manual Release:**
Alternatively, create a [GitHub Release](https://github.com/santhoshsharuk/voc-cmd/releases) and the package will be published automatically.

### Setting up PyPI Token (for maintainers)

The automated publishing requires a PyPI API token stored as a GitHub secret:

1. Go to [PyPI Account Settings](https://pypi.org/account/) → API tokens
2. Create a new token scoped to this project
3. In your GitHub repository, go to Settings → Secrets and variables → Actions
4. Create a new secret named `PYPI_API_TOKEN` with your token value

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.