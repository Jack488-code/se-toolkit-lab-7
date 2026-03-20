"""Handler for /health command."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_health(user_input: str = "") -> str:
    """Handle the /health command.

    Args:
        user_input: Optional user input (not used for /health).

    Returns:
        Backend health status.
    """
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)

    # Run async health check
    result = asyncio.run(client.health_check())

    if result["status"] == "ok":
        return f"🟢 Backend status: OK\n\n{result['message']}"
    else:
        return f"🔴 Backend status: Error\n\n{result['message']}"
