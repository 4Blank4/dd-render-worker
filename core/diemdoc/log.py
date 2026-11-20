"""Logging thống nhất cho toàn hệ thống. Có prefix, màu, và mức độ."""

from __future__ import annotations

import os
import sys

_NO_COLOR = bool(os.environ.get("NO_COLOR")) or not sys.stdout.isatty()

_C = {
    "reset": "\033[0m", "dim": "\033[2m", "bold": "\033[1m",
    "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
    "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m",
}


def _c(name: str, text: str) -> str:
    return text if _NO_COLOR else f"{_C[name]}{text}{_C['reset']}"


def log(msg: str, tag: str = "diemdoc") -> None:
    print(f"{_c('dim', '[' + tag + ']')} {msg}")


def ok(msg: str) -> None:
    print(f"{_c('dim', '[ok]')} {_c('green', msg)}")


def warn(msg: str) -> None:
    print(f"{_c('dim', '[warn]')} {_c('yellow', msg)}")


def err(msg: str) -> None:
    print(f"{_c('dim', '[error]')} {_c('red', msg)}", file=sys.stderr)


def step(title: str) -> None:
    width = 66
    print()
    print(_c("cyan", "─" * width))
    print(_c("bold", f"  {title}"))
    print(_c("cyan", "─" * width))


def banner(title: str, sub: str = "") -> None:
    print()
    print(_c("magenta", "═" * 66))
    print(_c("bold", f"  {title}"))
    if sub:
        print(_c("dim", f"  {sub}"))
    print(_c("magenta", "═" * 66))


def die(msg: str, code: int = 1):
    err(msg)
    sys.exit(code)