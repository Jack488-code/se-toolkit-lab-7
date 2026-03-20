#!/usr/bin/env python3
"""Telegram bot entry point with --test mode support."""

import argparse
import sys
from pathlib import Path

# Add bot directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)


# Command router - maps commands to handlers
COMMAND_HANDLERS = {
    "/start": handle_start,
    "/help": handle_help,
    "/health": handle_health,
    "/labs": handle_labs,
    "/scores": handle_scores,
}


def process_command(command: str) -> str:
    """Process a command and return the response.

    Args:
        command: The command string (e.g., "/start" or "/scores lab-04").

    Returns:
        The handler's response text.
    """
    # Parse command and arguments
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    # Get handler
    handler = COMMAND_HANDLERS.get(cmd)

    if handler is None:
        return f"❓ Unknown command: {cmd}\nUse /help to see available commands."

    # Call handler with argument
    return handler(arg)


def run_test_mode(command: str) -> None:
    """Run the bot in test mode - process a single command and exit.

    Args:
        command: The command to test.
    """
    # Load config (validates .env.bot.secret exists)
    config = load_config()

    # Process command
    response = process_command(command)

    # Print response to stdout
    print(response)


def run_telegram_mode() -> None:
    """Run the bot in Telegram mode - connect to Telegram API."""
    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
        MessageHandler,
        filters,
    )

    config = load_config()

    if not config.bot_token:
        print("Error: BOT_TOKEN not set. Set it in .env.bot.secret or environment.")
        sys.exit(1)

    # Handler wrapper for Telegram
    async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Wrap handler for Telegram."""
        # Get command with arguments
        command = "/" + context.args[0] if context.args else update.message.text
        full_command = f"{command} {' '.join(context.args[1:])}" if context.args else command

        response = process_command(full_command)
        await update.message.reply_text(response)

    # Create application
    application = Application.builder().token(config.bot_token).build()

    # Add command handlers
    for cmd in COMMAND_HANDLERS:
        application.add_handler(CommandHandler(cmd[1:], handle_command))

    # Add message handler for plain text (Task 3 - LLM)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command))

    # Start bot
    print(f"Starting bot... (BOT_TOKEN: {config.bot_token[:10]}...)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SE Toolkit Lab 7 Telegram Bot")
    parser.add_argument(
        "--test",
        type=str,
        metavar="COMMAND",
        help="Run in test mode with the given command (e.g., '/start')",
    )

    args = parser.parse_args()

    if args.test:
        # Test mode - process single command and exit
        run_test_mode(args.test)
    else:
        # Telegram mode - run the bot
        run_telegram_mode()


if __name__ == "__main__":
    main()
