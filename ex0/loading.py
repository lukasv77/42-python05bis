#!/usr/bin/env python3

import importlib

REAGENTS: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
}


def load_reagent(name: str) -> str | None:
    try:
        reagent = importlib.import_module(name)
    except ImportError:
        return None
    return str(reagent.__version__)


def main() -> None:
    print("\nREAGENT STATUS: Loading reagents...\n")
    print("Checking dependencies:")

    is_missing = False
    for module, info in REAGENTS.items():
        version = load_reagent(module)
        if version is not None:
            print(f"[OK] {module} ({version}) - {info}")
        else:
            print(f"[MISSING] {module}")
            is_missing = True

    print("\npip vs Poetry:\n"
          "  requirements.txt declares what to install; "
          "pip resolves it at install time.\n"
          "  pyproject.toml declares the same constraints, "
          "and Poetry pins the resolved\n"
          "  versions in poetry.lock so every install is identical.\n")

    if is_missing:
        print("Missing reagents! Install them with:\n"
              "  pip:    pip install -r ex0/requirements.txt\n"
              "  Poetry: cd ex0 && poetry install")
    else:
        print("All reagents present and accounted for.")


if __name__ == "__main__":
    main()
