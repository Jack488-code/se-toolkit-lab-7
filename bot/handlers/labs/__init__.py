"""Handler for /labs command."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_labs(user_input: str = "") -> str:
    """Handle the /labs command.

    Args:
        user_input: Optional user input (not used for /labs).

    Returns:
        List of available labs from backend.
    """
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)

    # Run async fetch
    labs = asyncio.run(client.get_labs())

    if not labs:
        return (
            "📋 Available labs:\n\n"
            "No labs found or backend is unavailable.\n"
            "Make sure the backend is running and data is synced."
        )

    # Format labs list
    lines = ["📋 Available labs:\n"]
    for lab in labs:
        lab_id = lab.get("id", "unknown")
        lab_name = lab.get("name", f"Lab {lab_id}")
        lines.append(f"• **{lab_id}**: {lab_name}")

    return "\n".join(lines)
