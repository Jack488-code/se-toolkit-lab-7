"""Handler for /health command."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_health(user_input: str = "") -> str:
    """Handle the /health command.

    Args:
        user_input: Optional user input (not used for /health).

    Returns:
        Backend health status with item count.
    """
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)

    # Run async health check and get labs
    health_result = asyncio.run(client.health_check())
    labs = asyncio.run(client.get_labs())

    if health_result["status"] == "ok":
        return (
            f"🟢 Backend status: OK\n\n"
            f"{health_result['message']}\n"
            f"Total items in database: {len(labs)} labs available"
        )
    else:
        return f"🔴 Backend status: Error\n\n{health_result['message']}"
