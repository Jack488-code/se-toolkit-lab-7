"""Handler for pass rates."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_pass_rates(user_input: str = "") -> str:
    """Handle pass rates query."""
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)
    
    pass_rates = asyncio.run(client.get_pass_rates())
    
    if not pass_rates:
        return "📊 No pass rate data available."
    
    lines = ["📊 Lab Pass Rates:\n"]
    for lab in pass_rates[:10]:  # Limit to 10 labs
        lab_name = lab.get("lab_name", f"Lab {lab.get('lab_id', '?')}")
        rate = lab.get("pass_rate", 0)
        lines.append(f"• {lab_name}: {rate:.1f}%")
    
    return "\n".join(lines)
