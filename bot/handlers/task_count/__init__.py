"""Handler for task count."""

import asyncio
from config import load_config
from services import create_lms_client


def handle_task_count(user_input: str = "") -> str:
    """Handle task count query."""
    config = load_config()
    client = create_lms_client(config.lms_api_url, config.lms_api_key)
    
    # Try to extract lab_id from input
    lab_id = user_input if user_input else None
    
    count = asyncio.run(client.get_task_count(lab_id))
    
    if lab_id:
        return f"📝 Tasks in {lab_id}: {count}"
    return f"📝 Total tasks in course: {count}"
