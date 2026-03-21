"""Handler for /scores command."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_scores(user_input: str = "") -> str:
    """Handle the /scores command."""
    if not user_input:
        return (
            "\U0001F4CA Scores command usage:\n\n"
            "/scores <lab_id> - Get scores for a specific lab\n\n"
            "Example: /scores lab-01"
        )

    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)
    result = asyncio.run(client.get_scores(user_input))

    if result is None:
        return f"\U0001F4CA No scores found for lab: {user_input}\n\nCheck the lab ID and try again."

    lines = [f"\U0001F4CA Scores for {user_input}:\n"]
    lines.append(f"**{result.get('title', 'Unknown')}**\n")
    
    if result.get("description"):
        lines.append(f"{result['description']}\n")
    
    completion_rate = result.get("completion_rate", 0)
    lines.append(f"Completion: {completion_rate:.1f}%")
    lines.append(f"Tasks completed: {result.get('completed_tasks', 0)}/{result.get('total_tasks', 0)}")
    lines.append(f"Total attempts: {result.get('attempts', 0)}")
    lines.append(f"\nLab ID: {result.get('lab_id', 'N/A')}")

    return "\n".join(lines)
