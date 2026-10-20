#!/usr/bin/env python3

import os
import site
import sys


def is_in_venv() -> bool:
    return sys.prefix != sys.base_prefix


def show_global() -> None:
    print("\nLABORATORY STATUS: You are working in the open\n"
          "\n"
          f"Current Python: {sys.executable}\n"
          "Virtual Environment: None detected\n"
          "\n"
          "WARNING: You are in the global environment!\n"
          "Every reagent you install here leaks into the whole system.\n"
          "\n"
          "To seal the laboratory, run:\n"
          "python3 -m venv lab_env\n"
          "source lab_env/bin/activate # On Unix\n"
          "lab_env\\Scripts\\activate # On Windows\n"
          "\n"
          "Then run this program again.")


def show_venv() -> None:
    venv_path: str = sys.prefix
    venv_name: str = os.path.basename(venv_path)
    site_packages: list[str] = [p for p in site.getsitepackages()
                                if os.path.isdir(p)]
    print("\nLABORATORY STATUS: The laboratory is sealed\n"
          "\n"
          f"Current Python: {sys.executable}\n"
          f"Virtual Environment: {venv_name}\n"
          f"Environment Path: {venv_path}\n"
          "\n"
          "SUCCESS: You are working in an isolated environment!\n"
          "Safe to install reagents without affecting\n"
          "the global system.\n"
          "\n"
          "Reagent installation path:")
    for p in site_packages:
        print(p)
    global_packages: list[str] = [
        p for p in site.getsitepackages([sys.base_prefix])
        if os.path.isdir(p)
    ]
    print("\nGlobal installation path (outside the laboratory):")
    for p in global_packages:
        print(p)


if __name__ == "__main__":
    if is_in_venv():
        show_venv()
    else:
        show_global()
