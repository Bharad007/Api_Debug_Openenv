"""
Root-level OpenEnv compatibility entrypoint.

This file is required by the OpenEnv multi-mode validator.
It delegates to the packaged implementation.
"""

import uvicorn
from api_debug_openenv.server.app import app as packed_app
from api_debug_openenv.server.app import main as packed_main

# Expose the ASGI app
app = packed_app


def main():
    """
    Required OpenEnv CLI entrypoint.
    """
    packed_main()


if __name__ == "__main__":
    main()