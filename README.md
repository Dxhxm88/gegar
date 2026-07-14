# gegar

A cross-platform CLI mouse jiggler that runs in the background. Keeps your computer awake by simulating small mouse movements.

## Installation

```bash
pip install -e .
```

Or install directly:

```bash
pip install .
```

### What's the difference?

- **`pip install -e .`** — Editable install. Links to your source folder so any code changes take effect immediately without reinstalling. Use this during development.
- **`pip install .`** — Standard install. Copies the code into your Python environment. You'd need to reinstall after making changes. Use this for a final/permanent install.

## Usage

```bash
# Start the jiggler (runs in background)
gegar start

# Check if it's running
gegar status

# Stop it
gegar stop

# View configuration
gegar config show

# Show config file path
gegar config path

# Edit config in your default editor
gegar config edit

# Reset config to defaults
gegar config reset
```

## Configuration

Config file location:
- **macOS**: `~/Library/Application Support/gegar/config.toml`
- **Linux**: `~/.config/gegar/config.toml`
- **Windows**: `%APPDATA%\gegar\config.toml`

Default settings:

```toml
# Seconds between each mouse movement
interval = 30

# Pixels to move the mouse
distance = 5

# Movement pattern: "circle", "random", "square"
pattern = "circle"

# Duration in seconds (0 = run forever until stopped)
duration = 0
```

### Patterns

| Pattern  | Description                                    |
|----------|------------------------------------------------|
| `circle` | Moves in a small circle, returns to start      |
| `random` | Random offset and back                         |
| `square` | Moves in a square path, returns to start       |

## Prerequisites

- Python 3.8+ installed on your system

That's it. All dependencies (like `pynput` for mouse control) are installed automatically when you run `pip install`.

### `pip` command not found?

If `pip` doesn't work, try one of these:

```bash
# Use pip3 instead (common on macOS/Linux)
pip3 install -e .

# Or use Python's built-in pip module
python3 -m pip install -e .
```

On some Linux distros, pip isn't bundled by default:

```bash
# Debian/Ubuntu
sudo apt install python3-pip

# Fedora
sudo dnf install python3-pip
```

### `gegar` command not recognized after install?

This means the Python scripts directory isn't on your PATH. Fix it permanently:

**macOS/Linux (zsh):**

```bash
echo 'export PATH="$PATH:$(python3 -m site --user-base)/bin"' >> ~/.zshrc
source ~/.zshrc
```

**macOS/Linux (bash):**

```bash
echo 'export PATH="$PATH:$(python3 -m site --user-base)/bin"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**

```powershell
# Find where scripts are installed
python -m site --user-site
# Add the Scripts folder (replace "site-packages" with "Scripts" in that path) to your system PATH
```

**Alternative:** You can always run gegar via Python directly without PATH changes:

```bash
python3 -m gegar status
```

## Supported Platforms

- macOS
- Linux
- Windows

## How it works

`gegar start` spawns a background process that periodically moves the mouse according to your config. The process runs independently of your terminal — you can close the terminal and it keeps running. Use `gegar stop` to kill it.

## License

MIT
