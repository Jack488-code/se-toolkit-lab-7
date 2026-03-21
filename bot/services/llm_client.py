"""LLM client for intent routing."""

import httpx
import json
from typing import Optional
from config import load_config


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "handle_start",
            "description": "Show welcome message and introduce the bot. Use when user greets or starts conversation.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_help",
            "description": "Show list of available commands and how to use the bot.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_health",
            "description": "Check backend health status and show item count from database.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_labs",
            "description": "List all available labs with their titles and IDs.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_scores",
            "description": "Get scores, completion rate, and attempts for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab_id": {"type": "string", "description": "Lab identifier like lab-01, lab-04"}
                },
                "required": ["lab_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_enrollment_count",
            "description": "Get total number of enrolled students in the course.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get pass rates statistics for all labs.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_lab_with_lowest_pass_rate",
            "description": "Find the lab with the lowest pass rate.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_task_count",
            "description": "Get total number of tasks in the course or for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab_id": {"type": "string", "description": "Optional lab ID to filter tasks"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_interaction_stats",
            "description": "Get statistics about student interactions with the system.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]


class LLMClient:
    """Client for Qwen LLM API."""

    def __init__(self, api_key: str, base_url: str, model: str, timeout: float = 30.0):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def get_intent(self, user_message: str) -> tuple:
        """Get intent from LLM - which handler to call."""
        url = f"{self.base_url}/chat/completions"
        
        system_prompt = """You are an intent router for a Telegram bot. Analyze the user message and select the appropriate tool.

Available tools:
- handle_start: Welcome new users
- handle_help: Show available commands
- handle_health: Check backend status
- handle_labs: List all labs
- handle_scores: Get scores for a specific lab (requires lab_id)
- get_enrollment_count: Get number of enrolled students
- get_pass_rates: Get pass rates for all labs
- get_lab_with_lowest_pass_rate: Find lab with lowest pass rate
- get_task_count: Count tasks
- get_interaction_stats: Get interaction statistics

Respond with ONLY the tool name and arguments in JSON format.
Example: {"name": "handle_labs", "arguments": {}}
Example: {"name": "handle_scores", "arguments": {"lab_id": "lab-04"}}
"""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "tools": TOOLS,
            "tool_choice": "auto",
            "temperature": 0.1,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=self._get_headers(), json=payload)
                response.raise_for_status()
                data = response.json()
                
                choices = data.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    tool_calls = message.get("tool_calls", [])
                    if tool_calls:
                        tool = tool_calls[0]
                        function = tool.get("function", {})
                        handler_name = function.get("name")
                        arguments = function.get("arguments", {})
                        if isinstance(arguments, str):
                            arguments = json.loads(arguments)
                        return handler_name, arguments
                
                return None, None
                
        except Exception as e:
            print(f"LLM error: {e}")
            return None, None


def create_llm_client() -> LLMClient:
    """Create LLM client from config."""
    config = load_config()
    return LLMClient(
        api_key=config.llm_api_key,
        base_url=config.llm_api_base_url,
        model=config.llm_api_model,
    )
