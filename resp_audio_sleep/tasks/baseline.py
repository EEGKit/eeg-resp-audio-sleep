from __future__ import annotations

from ..utils._checks import check_type
from ..utils.logs import logger
from ..utils.time import high_precision_sleep
from ._config import TRIGGER_TASKS
from ._utils import create_trigger


def baseline(duration: float) -> None:
    """Baseline block corresponding to a resting-state recording.

    Parameters
    ----------
    duration : float
        Duration of the baseline in seconds.
    """  # noqa: D401
    check_type(duration, ("numeric",), "duration")
    if duration <= 0:
        raise ValueError("The duration must be strictly positive.")
    trigger = create_trigger()
    logger.info("Starting baseline block of %.2f seconds.", duration)
    trigger.signal(TRIGGER_TASKS["baseline"][0])
    high_precision_sleep(duration)
    trigger.signal(TRIGGER_TASKS["baseline"][1])
    logger.info("Baseline block complete.")
