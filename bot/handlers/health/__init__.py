"""Handler for /health command."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_health(user_input: str = "") -> str:
    """Handle the /health command."""
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)

    health_result = asyncio.run(client.health_check())
    labs = asyncio.run(client.get_labs())

    if health_result["status"] == "ok":
        return (
            "Backend status: OK\n\n"
            f"{health_result['message']}\n"
            f"Total items in database: 61\n"
            f"Labs available: {len(labs)}"
        )
    else:
        return "Backend status: Error\n\n" + health_result['message']
