"""Command handlers for the Telegram bot."""

from .start import handle_start
from .help import handle_help
from .health import handle_health
from .labs import handle_labs
from .scores import handle_scores
from .enrollment import handle_enrollment_count
from .pass_rates import handle_pass_rates
from .lowest_pass_rate import handle_lowest_pass_rate
from .task_count import handle_task_count
from .interaction_stats import handle_interaction_stats

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
    "handle_enrollment_count",
    "handle_pass_rates",
    "handle_lowest_pass_rate",
    "handle_task_count",
    "handle_interaction_stats",
]
