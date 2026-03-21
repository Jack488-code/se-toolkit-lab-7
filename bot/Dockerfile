FROM python:3.12-slim

WORKDIR /app

# Copy files
COPY bot.py config.py ./
COPY handlers/ ./handlers/
COPY services/ ./services/
COPY pyproject.toml ./

# Install dependencies directly
RUN pip install --no-cache-dir python-telegram-bot httpx pydantic pydantic-settings python-dotenv

# Run the bot
CMD ["python", "bot.py"]
