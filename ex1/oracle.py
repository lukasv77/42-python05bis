#!/usr/bin/env python3


import os


DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///matrix.db",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "",
}
MODES: tuple[str, ...] = ("development", "production")
LOG_LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
REQUIRED_IN_PRODUCTION: tuple[str, ...] = (
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
)
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


def load_env_file() -> bool:
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("[WARNING] python-dotenv is not installed: "
              "pip install -r ex1/requirements.txt")
        return False
    dotenv_file = os.path.join(BASE_DIR, ".env")
    if not os.path.isfile(dotenv_file):
        print("[WARNING] No .env file found, create one with: "
              "cp ex1/.env.example ex1/.env")
        return False
    load_dotenv(dotenv_file)
    return True


def get_config() -> dict[str, str]:
    config: dict[str, str] = {}
    for key, default in DEFAULTS.items():
        config[key] = os.getenv(key, default)
    if config["MATRIX_MODE"] not in MODES:
        print(f"[WARNING] Unknown MATRIX_MODE '{config['MATRIX_MODE']}', "
              "using development")
        config["MATRIX_MODE"] = "development"
    config["LOG_LEVEL"] = config["LOG_LEVEL"].upper()
    if config["LOG_LEVEL"] not in LOG_LEVELS:
        print(f"[WARNING] Unknown LOG_LEVEL '{config['LOG_LEVEL']}', "
              "using INFO")
        config["LOG_LEVEL"] = "INFO"
    return config


def get_sources(overrides: set[str]) -> dict[str, str]:
    sources: dict[str, str] = {}
    for key in DEFAULTS:
        if key in overrides:
            sources[key] = "environment"
        elif key in os.environ:
            sources[key] = ".env file"
        else:
            sources[key] = "default"
    return sources


def describe_database(url: str) -> str:
    if not url:
        return "Not configured"
    if url.startswith("sqlite") or "localhost" in url or "127.0.0.1" in url:
        return "Connected to local instance"
    return "Connected to remote instance"


def describe_api(api_key: str) -> str:
    if not api_key:
        return "Missing API key"
    return "Authenticated"


def describe_network(endpoint: str) -> str:
    if not endpoint:
        return "Offline"
    return "Online"


def show_config(config: dict[str, str]) -> None:
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {describe_database(config['DATABASE_URL'])}")
    print(f"API Access: {describe_api(config['API_KEY'])}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Remote Network: {describe_network(config['ZION_ENDPOINT'])}")


def show_development(sources: dict[str, str]) -> None:
    print("\nDevelopment details (where each value comes from):")
    for key, source in sources.items():
        print(f"  {key}: {source}")


def check_production(config: dict[str, str]) -> None:
    print("\nProduction checks:")
    problems = 0
    for key in REQUIRED_IN_PRODUCTION:
        if not config[key]:
            print(f"[ERROR] {key} is required in production")
            problems += 1
    if config["LOG_LEVEL"] == "DEBUG":
        print("[WARNING] DEBUG logging should not be used in production")
        problems += 1
    if problems == 0:
        print("[OK] Production configuration is complete")


def is_hardcoded(secret: str) -> bool:
    if len(secret) < 8:
        return False
    with open(os.path.abspath(__file__), encoding="utf-8") as file:
        return secret in file.read()


def is_env_ignored() -> bool:
    gitignore = os.path.join(BASE_DIR, ".gitignore")
    try:
        with open(gitignore, encoding="utf-8") as file:
            lines = [line.strip() for line in file]
    except OSError:
        return False
    return ".env" in lines


def security_check(config: dict[str, str], overrides: set[str]) -> None:
    print("\nConfiguration security check:")
    if is_hardcoded(config["API_KEY"]):
        print("[WARNING] API key found in the source code")
    else:
        print("[OK] No hardcoded secrets detected")
    if is_env_ignored():
        print("[OK] .env file properly ignored by git")
    else:
        print("[WARNING] .env is not listed in ex1/.gitignore")
    if overrides:
        print("[OK] Production overrides active: "
              f"{', '.join(sorted(overrides))}")
    else:
        print("[OK] Production overrides available")


def main() -> None:
    print("\nORACLE STATUS: Consulting the configuration...\n")
    overrides = {key for key in DEFAULTS if key in os.environ}
    load_env_file()
    config = get_config()
    sources = get_sources(overrides)
    missing = [key for key, source in sources.items() if source == "default"]
    if missing:
        print(f"[WARNING] Missing configuration: {', '.join(missing)} "
              "- using default values")
    print()
    show_config(config)
    if config["MATRIX_MODE"] == "development":
        show_development(sources)
    else:
        check_production(config)
    security_check(config, overrides)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
