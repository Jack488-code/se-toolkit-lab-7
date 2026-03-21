FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY bot/ ./bot/
COPY config.py ./
COPY handlers/ ./handlers/
COPY services/ ./services/

# Sync dependencies
RUN uv sync --frozen

# Run the bot
CMD ["uv", "run", "bot.py"]
