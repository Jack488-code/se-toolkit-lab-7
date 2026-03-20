"""Handler for /start command."""


def handle_start(user_input: str = "") -> str:
    """Handle the /start command.

    Args:
        user_input: Optional user input (not used for /start).

    Returns:
        Welcome message.
    """
    return (
        "👋 Welcome to the SE Toolkit Lab 7 Bot!\n\n"
        "I can help you check your lab scores, view available labs, "
        "and answer questions about the course.\n\n"
        "Use /help to see all available commands."
    )
