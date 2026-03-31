"""
Thin wrapper for OpenEnv validator.
Imports and re-exports the actual app from the package.
"""

from api_debug_openenv.server.app import app, main as _main

__all__ = ["app", "main"]


def main():
    """OpenEnv multi-mode entrypoint."""
    return _main()


if __name__ == "__main__":
    main()
