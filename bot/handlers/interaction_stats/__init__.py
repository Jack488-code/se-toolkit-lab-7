"""Handler for interaction stats."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_interaction_stats(user_input: str = "") -> str:
    """Handle interaction stats query."""
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)
    
    stats = asyncio.run(client.get_interaction_stats())
    
    total = stats.get("total_interactions", 0)
    return f"💬 Total interactions: {total}"
