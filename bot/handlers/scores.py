"""Handler for /scores command."""


def handle_scores(user_input: str = "") -> str:
    """Handle the /scores command.

    Args:
        user_input: Optional lab ID (e.g., "lab-04").

    Returns:
        Scores for the specified lab (placeholder for Task 1).
    """
    if user_input:
        return f"📊 Scores for {user_input}: (placeholder - will fetch from backend in Task 2)"
    return (
        "📊 Scores command usage:\n\n"
        "/scores <lab_id> - Get scores for a specific lab\n\n"
        "Example: /scores lab-04"
    )
