import time

import psychtoolbox as ptb

from ..utils._checks import check_type
from ..utils._docs import fill_doc
from ..utils.logs import logger
from ._config import SOUND_DURATION, TARGET_DELAY, TRIGGERS
from ._utils import create_sounds, create_trigger, generate_sequence


@fill_doc
def isochronous(delay: float, *, target: float, deviant: float) -> None:  # noqa: D401
    """Isochronous auditory stimulus.

    Parameters
    ----------
    delay : float
        Delay between 2 stimuli in seconds.
    %(fq_target)s
    %(fq_deviant)s
    """
    check_type(delay, ("numeric",), "delay")
    if delay <= 0:
        raise ValueError("The delay must be strictly positive.")
    delay_post_trigger = delay - TARGET_DELAY
    logger.info("Starting isochronous block.")
    # create sound stimuli, trigger and sequence
    sounds = create_sounds()
    trigger = create_trigger()
    sequence = generate_sequence(target, deviant)
    # the sequence, sound and trigger generation validates the trigger dictionary, thus
    # we can safely map the target and deviant frequencies to their corresponding
    # trigger values and sounds.
    stimulus = {
        TRIGGERS[f"target/{target}"]: sounds[str(target)],
        TRIGGERS[f"deviant/{deviant}"]: sounds[str(deviant)],
    }
    # main loop
    counter = 0
    while counter <= sequence.size - 1:
        wait = ptb.GetSecs() + TARGET_DELAY
        stimulus.get(sequence[counter]).play(when=wait)
        logger.debug("Triggering %i in %.2f ms.", sequence[counter], TARGET_DELAY)
        time.sleep(TARGET_DELAY)
        trigger.signal(sequence[counter])
        time.sleep(delay_post_trigger)
        counter += 1
    # wait for the last sound to finish
    if delay_post_trigger < 1.1 * SOUND_DURATION:
        time.sleep(delay_post_trigger - 1.1 * SOUND_DURATION)
    logger.info("Isochronous block complete.")
