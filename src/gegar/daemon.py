"""Daemon/background process management for gegar."""

import os
import signal
import subprocess
import sys
import threading

from gegar.config import get_pid_path, load_config
from gegar.jiggler import run_jiggler


def is_running() -> tuple[bool, int | None]:
    """Check if gegar daemon is running. Returns (is_running, pid)."""
    pid_path = get_pid_path()
    if not pid_path.exists():
        return False, None

    pid = int(pid_path.read_text().strip())

    # Check if process is alive
    try:
        os.kill(pid, 0)  # Signal 0 = check existence
        return True, pid
    except (OSError, ProcessLookupError):
        # Stale PID file
        pid_path.unlink(missing_ok=True)
        return False, None


def start_daemon() -> str:
    """Start the jiggler as a background process."""
    running, pid = is_running()
    if running:
        return f"⚡ gegar is already running (PID: {pid})"

    # Spawn a detached subprocess running the daemon entry point
    python = sys.executable
    cmd = [python, "-m", "gegar.daemon"]

    if sys.platform == "win32":
        # Windows: use CREATE_NO_WINDOW flag
        CREATE_NO_WINDOW = 0x08000000
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW,
        )
    else:
        # Unix: detach from terminal
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )

    # Write PID file
    pid_path = get_pid_path()
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    pid_path.write_text(str(proc.pid))

    config = load_config()
    return (
        f"✅ gegar started\n"
        f"   PID:      {proc.pid}\n"
        f"   Pattern:  {config['pattern']}\n"
        f"   Interval: {config['interval']}s\n"
        f"   Distance: {config['distance']}px"
    )


def stop_daemon() -> str:
    """Stop the running jiggler daemon."""
    running, pid = is_running()
    if not running:
        return "💤 gegar is not running"

    try:
        if sys.platform == "win32":
            os.kill(pid, signal.SIGTERM)
        else:
            os.kill(pid, signal.SIGTERM)

        # Wait briefly for process to exit
        import time
        for _ in range(20):
            try:
                os.kill(pid, 0)
                time.sleep(0.1)
            except (OSError, ProcessLookupError):
                break

        # Clean up PID file
        get_pid_path().unlink(missing_ok=True)
        return f"🛑 gegar stopped (PID: {pid})"
    except (OSError, ProcessLookupError):
        get_pid_path().unlink(missing_ok=True)
        return f"🛑 gegar stopped (PID: {pid})"


def get_status() -> str:
    """Get the current status of the daemon."""
    running, pid = is_running()
    if running:
        config = load_config()
        return (
            f"🟢 gegar is running\n"
            f"   PID:      {pid}\n"
            f"   Pattern:  {config['pattern']}\n"
            f"   Interval: {config['interval']}s\n"
            f"   Distance: {config['distance']}px\n"
            f"   Duration: {'forever' if config['duration'] == 0 else str(config['duration']) + 's'}"
        )
    else:
        return "🔴 gegar is not running"


def daemon_main():
    """Entry point for the daemon process. Runs the jiggler until terminated."""
    config = load_config()
    stop_event = threading.Event()

    def handle_signal(signum, frame):
        stop_event.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    run_jiggler(
        interval=config["interval"],
        distance=config["distance"],
        pattern=config["pattern"],
        duration=config["duration"],
        stop_event=stop_event,
    )

    # Clean up PID file on exit
    get_pid_path().unlink(missing_ok=True)


if __name__ == "__main__":
    daemon_main()
