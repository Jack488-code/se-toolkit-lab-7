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

    # Format scores with percentage and attempts
    lines = [f"📊 Scores for {user_input}:\n"]
    lines.append(f"**{result.get('title', 'Unknown')}**\n")
    
    description = result.get("description", "")
    if description:
        lines.append(f"{description}\n")
    
    # Show completion rate as percentage
    completion_rate = result.get("completion_rate", 0)
    lines.append(f"Completion: {completion_rate:.1f}%")
    
    # Show task progress
    completed = result.get("completed_tasks", 0)
    total = result.get("total_tasks", 0)
    lines.append(f"Tasks completed: {completed}/{total}")
    
    # Show attempts
    attempts = result.get("attempts", 0)
    lines.append(f"Total attempts: {attempts}")
    
    lines.append(f"\nLab ID: {result.get('lab_id', 'N/A')}")

    return "\n".join(lines)
