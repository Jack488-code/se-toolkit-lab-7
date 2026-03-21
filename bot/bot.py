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
    handle_enrollment_count,
    handle_pass_rates,
    handle_lowest_pass_rate,
    handle_task_count,
    handle_interaction_stats,
)
from services import create_llm_client


# Command router - maps commands to handlers
COMMAND_HANDLERS = {
    "/start": handle_start,
    "/help": handle_help,
    "/health": handle_health,
    "/labs": handle_labs,
    "/scores": handle_scores,
}

# LLM tool handlers - mapped by tool name
TOOL_HANDLERS = {
    "handle_start": handle_start,
    "handle_help": handle_help,
    "handle_health": handle_health,
    "handle_labs": handle_labs,
    "handle_scores": handle_scores,
    "get_enrollment_count": handle_enrollment_count,
    "get_pass_rates": handle_pass_rates,
    "get_lab_with_lowest_pass_rate": handle_lowest_pass_rate,
    "get_task_count": handle_task_count,
    "get_interaction_stats": handle_interaction_stats,
}


def process_command(command: str, use_llm: bool = True) -> str:
    """Process a command and return the response.

    Args:
        command: The command string (e.g., "/start" or "what labs are available").
        use_llm: Whether to use LLM for intent routing.

    Returns:
        The handler's response text.
    """
    # Parse command and arguments
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    # Direct command handler
    handler = COMMAND_HANDLERS.get(cmd)
    if handler:
        return handler(arg)

    # Use LLM for intent routing on plain text queries
    if use_llm:
        llm_client = create_llm_client()
        import asyncio
        handler_name, arguments = asyncio.run(llm_client.get_intent(command))
        
        if handler_name and handler_name in TOOL_HANDLERS:
            handler = TOOL_HANDLERS[handler_name]
            # Pass lab_id if provided in arguments
            if arguments and "lab_id" in arguments:
                return handler(arguments["lab_id"])
            return handler(arg)

    # Fallback: pattern matching (only if LLM fails)
    cmd_lower = command.lower()
    
    if any(p in cmd_lower for p in ["score", "scores", "grade", "progress", "completion"]):
        import re
        match = re.search(r"lab-?\d+", cmd_lower)
        if match:
            lab_id = match.group().replace(" ", "")
            return handle_scores(lab_id)
        return handle_scores(arg)
    
    if any(p in cmd_lower for p in ["hello", "hi", "welcome", "start"]):
        return handle_start(arg)
    if any(p in cmd_lower for p in ["help", "commands", "what can"]):
        return handle_help(arg)
    if any(p in cmd_lower for p in ["health", "status", "running", "backend"]):
        return handle_health(arg)
    if any(p in cmd_lower for p in ["lab", "labs", "available"]):
        return handle_labs(arg)

    return f"❓ Unknown command: {cmd}\nUse /help to see available commands."


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
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        CallbackQueryHandler,
        ContextTypes,
        MessageHandler,
        filters,
    )

    config = load_config()

    if not config.bot_token:
        print("Error: BOT_TOKEN not set. Set it in .env.bot.secret or environment.")
        sys.exit(1)

    # Create inline keyboard for main menu
    def get_main_keyboard() -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton("📋 Labs", callback_data="labs"),
                InlineKeyboardButton("📊 Scores", callback_data="scores"),
            ],
            [
                InlineKeyboardButton("💚 Health", callback_data="health"),
                InlineKeyboardButton("❓ Help", callback_data="help"),
            ],
            [
                InlineKeyboardButton("📚 Enrollment", callback_data="enrollment"),
                InlineKeyboardButton("📈 Pass Rates", callback_data="pass_rates"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    # Handler wrapper for Telegram
    async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Wrap handler for Telegram."""
        command = "/" + context.args[0] if context.args else update.message.text
        full_command = f"{command} {' '.join(context.args[1:])}" if context.args else command
        response = process_command(full_command)
        await update.message.reply_text(response, reply_markup=get_main_keyboard())

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle plain text messages with LLM routing."""
        message = update.message.text
        response = process_command(message)
        await update.message.reply_text(response)

    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline keyboard button clicks."""
        query = update.callback_query
        await query.answer()
        
        action = query.data
        if action == "labs":
            response = handle_labs("")
        elif action == "scores":
            response = "Send me a lab ID (e.g., lab-01) to see scores"
        elif action == "health":
            response = handle_health("")
        elif action == "help":
            response = handle_help("")
        elif action == "enrollment":
            response = handle_enrollment_count("")
        elif action == "pass_rates":
            response = handle_pass_rates("")
        else:
            response = "Unknown action"
        
        await query.edit_message_text(response, reply_markup=get_main_keyboard())

    # Create application
    application = Application.builder().token(config.bot_token).build()

    # Add command handlers
    for cmd in COMMAND_HANDLERS:
        application.add_handler(CommandHandler(cmd[1:], handle_command))

    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Add message handler for plain text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

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
