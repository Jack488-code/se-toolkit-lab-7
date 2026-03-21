"""Handler for lowest pass rate lab."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_lowest_pass_rate(user_input: str = "") -> str:
    """Handle lowest pass rate query."""
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)
    
    result = asyncio.run(client.get_lowest_pass_rate_lab())
    
    if not result:
        return "📊 No pass rate data available."
    
    lab_name = result.get("lab_name", f"Lab {result.get('lab_id', '?')}")
    rate = result.get("pass_rate", 0)
    
    return f"📉 Lab with lowest pass rate: {lab_name} ({rate:.1f}%)"
