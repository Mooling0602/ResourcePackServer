#!/usr/bin/env python3
import shutil
import subprocess

STEPS = [
    ("ty", ["ty", "check", "src"]),
    ("ruff", ["ruff", "check", "src"]),
    ("ruff", ["ruff", "format", "--check", "src"])
]


def run(name: str, cmd: list[str]) -> int:
    print(f"----- {name} -----")
    if shutil.which(cmd[0]) is None:
        print(
            f"'{cmd[0]}' not found. Please install with `uv sync` or your package manager."
        )
        return 0
    result = subprocess.run(cmd, check=False)
    return result.returncode


def main() -> None:
    failures = 0
    for name, cmd in STEPS:
        if run(name, cmd) != 0:
            failures += 1
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()