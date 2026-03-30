"""
Compatibility shim for OpenEnv validator.

Delegates root-level server/app.py to the packaged implementation.
"""

from api_debug_openenv.server.app import app, main

__all__ = ["app", "main"]