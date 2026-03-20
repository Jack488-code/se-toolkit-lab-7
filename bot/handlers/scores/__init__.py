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
            "Example: /scores lab-01"
        )

    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)

    # Run async fetch
    result = asyncio.run(client.get_scores(user_input))

    if result is None:
        return f"📊 No scores found for lab: {user_input}\n\nCheck the lab ID and try again."

    # Format scores
    lines = [f"📊 Scores for {user_input}:\n"]
    lines.append(f"**{result.get('title', 'Unknown')}**\n")
    
    description = result.get("description", "")
    if description:
        lines.append(f"{description}\n")
    
    lines.append(f"Lab ID: {result.get('lab_id', 'N/A')}")

    return "\n".join(lines)
