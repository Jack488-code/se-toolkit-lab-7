"""Handler for enrollment count."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_enrollment_count(user_input: str = "") -> str:
    """Handle enrollment count query."""
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)
    
    count = asyncio.run(client.get_enrollment_count())
    
    return f"📚 Total enrolled students: {count}"
