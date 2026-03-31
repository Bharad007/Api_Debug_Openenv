"""
Thin wrapper for OpenEnv validator.
Imports and re-exports the actual app from the package.
"""

from api_debug_openenv.server.app import app, main

__all__ = ["app", "main"]
