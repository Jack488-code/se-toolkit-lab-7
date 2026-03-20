"""Handler for /help command."""


def handle_help(user_input: str = "") -> str:
    """Handle the /help command.

    Args:
        user_input: Optional user input (not used for /help).

    Returns:
        List of available commands.
    """
    return (
        "📚 Available commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/health - Check backend connection status\n"
        "/labs - View available labs\n"
        "/scores <lab_id> - Get your scores for a specific lab\n\n"
        "You can also ask questions in plain text (Task 3)."
    )
