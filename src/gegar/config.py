"""Configuration management for gegar."""

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib


DEFAULT_CONFIG = {
    "interval": 30,          # seconds between jiggles
    "distance": 5,           # pixels to move
    "pattern": "circle",     # movement pattern: circle, random, square
    "duration": 0,           # 0 = run forever, otherwise seconds
}

CONFIG_TEMPLATE = """\
# gegar configuration file

# Seconds between each mouse movement
interval = 30

# Pixels to move the mouse
distance = 5

# Movement pattern: "circle", "random", "square"
pattern = "circle"

# Duration in seconds (0 = run forever until stopped)
duration = 0
"""


def get_config_dir() -> Path:
    """Get the platform-appropriate config directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "gegar"


def get_config_path() -> Path:
    """Get the path to the config file."""
    return get_config_dir() / "config.toml"


def get_pid_path() -> Path:
    """Get the path to the PID file."""
    if sys.platform == "win32":
        return get_config_dir() / "gegar.pid"
    else:
        runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
        return Path(runtime_dir) / "gegar.pid"


def init_config() -> Path:
    """Create default config file if it doesn't exist. Returns the path."""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        config_path.write_text(CONFIG_TEMPLATE)
    return config_path


def load_config() -> dict:
    """Load configuration from file, falling back to defaults."""
    config_path = get_config_path()
    config = DEFAULT_CONFIG.copy()

    if config_path.exists():
        with open(config_path, "rb") as f:
            user_config = tomllib.load(f)
        config.update(user_config)

    return config
