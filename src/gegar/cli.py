"""CLI interface for gegar."""

import argparse
import sys

from gegar import __version__
from gegar.config import get_config_path, init_config, load_config, CONFIG_TEMPLATE
from gegar.daemon import start_daemon, stop_daemon, get_status


def cmd_start(args):
    """Start the mouse jiggler daemon."""
    init_config()
    print(start_daemon())


def cmd_stop(args):
    """Stop the mouse jiggler daemon."""
    print(stop_daemon())


def cmd_status(args):
    """Show daemon status."""
    print(get_status())


def cmd_config(args):
    """Show or edit configuration."""
    config_path = init_config()

    if args.config_action == "path":
        print(config_path)
    elif args.config_action == "show":
        config = load_config()
        print(f"Config file: {config_path}")
        print(f"  interval = {config['interval']}  # seconds")
        print(f"  distance = {config['distance']}  # pixels")
        print(f"  pattern  = \"{config['pattern']}\"")
        print(f"  duration = {config['duration']}  # seconds (0 = forever)")
    elif args.config_action == "edit":
        import subprocess
        editor = _get_editor()
        subprocess.run([editor, str(config_path)])
    elif args.config_action == "reset":
        config_path.write_text(CONFIG_TEMPLATE)
        print(f"Config reset to defaults: {config_path}")
    else:
        # Default: show config
        config = load_config()
        print(f"Config file: {config_path}")
        print(f"  interval = {config['interval']}  # seconds")
        print(f"  distance = {config['distance']}  # pixels")
        print(f"  pattern  = \"{config['pattern']}\"")
        print(f"  duration = {config['duration']}  # seconds (0 = forever)")


def _get_editor() -> str:
    """Get the user's preferred editor."""
    import os
    return os.environ.get("EDITOR", os.environ.get("VISUAL", "nano" if sys.platform != "win32" else "notepad"))


def main():
    parser = argparse.ArgumentParser(
        prog="gegar",
        description="A cross-platform mouse jiggler that runs in the background.",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"gegar {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    # start
    start_parser = subparsers.add_parser("start", help="Start the mouse jiggler")

    # stop
    stop_parser = subparsers.add_parser("stop", help="Stop the mouse jiggler")

    # status
    status_parser = subparsers.add_parser("status", help="Check if jiggler is running")

    # config
    config_parser = subparsers.add_parser("config", help="View or edit configuration")
    config_parser.add_argument(
        "config_action",
        nargs="?",
        default="show",
        choices=["show", "path", "edit", "reset"],
        help="show (default), path, edit, or reset",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    commands = {
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "config": cmd_config,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
