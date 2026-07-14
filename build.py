#!/usr/bin/env python3
"""Build script for creating gegar standalone binary using PyInstaller."""

import platform
import subprocess
import sys


def build():
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Normalize architecture names
    if machine in ("amd64", "x86_64"):
        machine = "x86_64"
    elif machine in ("arm64", "aarch64"):
        machine = "arm64"

    # Binary name (add .exe on Windows)
    name = "gegar"
    if system == "windows":
        suffix = f"-windows-{machine}"
    elif system == "darwin":
        suffix = f"-macos-{machine}"
    else:
        suffix = f"-linux-{machine}"

    output_name = f"{name}{suffix}"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", output_name,
        "--clean",
    ]

    # Platform-specific hidden imports for pynput
    if system == "darwin":
        cmd += [
            "--hidden-import", "pynput.mouse._darwin",
            "--hidden-import", "pynput.keyboard._darwin",
            "--hidden-import", "pynput._util.darwin",
        ]
    elif system == "windows":
        cmd += [
            "--hidden-import", "pynput.mouse._win32",
            "--hidden-import", "pynput.keyboard._win32",
            "--hidden-import", "pynput._util.win32",
        ]
    else:  # Linux
        cmd += [
            "--hidden-import", "pynput.mouse._xorg",
            "--hidden-import", "pynput.keyboard._xorg",
            "--hidden-import", "pynput._util.xorg",
        ]

    cmd.append("src/gegar/cli.py")

    print(f"Building {output_name} for {system} ({machine})...")
    result = subprocess.run(cmd, check=True)

    if result.returncode == 0:
        ext = ".exe" if system == "windows" else ""
        print(f"\n✅ Binary built: dist/{output_name}{ext}")
    else:
        print("\n❌ Build failed")
        sys.exit(1)


if __name__ == "__main__":
    build()
