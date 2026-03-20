# Development Plan for SE Toolkit Lab 7 Telegram Bot

## Overview

This document outlines the development plan for building a Telegram bot that integrates with the Learning Management System (LMS) backend and uses LLM for natural language understanding.

## Architecture

The bot follows a **layered architecture** with clear separation of concerns:

1. **Entry Point (`bot.py`)**: Handles Telegram connection and `--test` mode. Routes commands to appropriate handlers.

2. **Handlers Layer (`handlers/`)**: Contains command-specific logic. Each handler is a pure function that takes input and returns text. This separation allows testing without Telegram.

3. **Services Layer (`services/`)**: External API clients (LMS backend, LLM). Handles HTTP requests, authentication, and error handling.

4. **Configuration (`config.py`)**: Loads environment variables using Pydantic Settings.

## Task 1: Project Scaffold (Current)

- Create directory structure: `bot/`, `handlers/`, `services/`
- Implement `--test` mode for offline testing
- Create placeholder handlers for `/start`, `/help`, `/health`, `/labs`, `/scores`
- Set up `pyproject.toml` with dependencies
- Create `.env.bot.example` and `.env.bot.secret`

## Task 2: Backend Integration

- Create `services/api_client.py` for LMS API communication
- Implement Bearer token authentication
- Update `/health` to check backend connectivity
- Update `/labs` to fetch real lab data from backend
- Update `/scores` to fetch user scores from backend
- Handle API errors gracefully (timeouts, 401, 500)

## Task 3: LLM Intent Routing

- Create `services/llm_client.py` for Qwen API
- Implement tool descriptions for each command
- Use LLM to route natural language queries to appropriate handlers
- Example: "what labs are available" → `handle_labs()`
- Improve tool descriptions for better LLM accuracy

## Task 4: Docker Deployment

- Create `bot/Dockerfile`
- Update `docker-compose.yml` to include bot service
- Configure networking between containers
- Use `host.docker.internal` for external API access
- Deploy and test on VM

## Testing Strategy

- **Unit tests**: Test handlers in isolation
- **Test mode**: `uv run bot.py --test "/command"` for manual testing
- **Integration tests**: Test API client with mock backend
- **Telegram testing**: Deploy to VM and test with real bot

## Git Workflow

1. Create issue for each task
2. Create feature branch: `task-1-scaffold`
3. Commit changes with meaningful messages
4. Create PR with `Closes #issue-number`
5. Partner review
6. Merge to main

## Risks and Mitigations

- **API rate limiting**: Implement retry logic with exponential backoff
- **Token expiration**: Refresh tokens automatically
- **Network issues**: Handle timeouts and connection errors
- **LLM hallucination**: Validate tool calls before execution
