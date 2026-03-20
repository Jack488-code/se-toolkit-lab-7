"""Handler for /scores command."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_scores(user_input: str = "") -> str:
    """Handle the /scores command.

    Args:
        user_input: Lab ID (e.g., "lab-04").

    Returns:
        Scores for the specified lab.
    """
    if not user_input:
        return (
            "📊 Scores command usage:\n\n"
            "/scores <lab_id> - Get scores for a specific lab\n\n"
            "Example: /scores lab-04"
        )

    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)

    # Run async fetch
    result = asyncio.run(client.get_scores(user_input))

    if result is None:
        return f"📊 No scores found for lab: {user_input}\n\nCheck the lab ID and try again."

    # Format scores
    lines = [f"📊 Scores for {user_input}:\n"]
    lines.append(f"Total items: {result['total_items']}\n")

    for item in result["items"]:
        item_name = item.get("name", "Unknown")
        item_id = item.get("id", "N/A")
        lines.append(f"• {item_name} (ID: {item_id})")

    if result["total_items"] > 5:
        lines.append(f"\n... and {result['total_items'] - 5} more items")

    return "\n".join(lines)
