"""Handler for /labs command."""


def handle_labs(user_input: str = "") -> str:
    """Handle the /labs command.

    Args:
        user_input: Optional user input (not used for /labs).

    Returns:
        List of available labs (placeholder for Task 1).
    """
    return (
        "📋 Available labs (placeholder - will fetch from backend in Task 2):\n\n"
        "Lab 01 - Introduction\n"
        "Lab 02 - Setup\n"
        "Lab 03 - Basic Commands\n"
        "Lab 04 - API Integration\n"
        "Lab 05 - Advanced Features\n"
        "Lab 06 - LLM Integration\n"
        "Lab 07 - Telegram Bot"
    )
