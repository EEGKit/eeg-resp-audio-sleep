import click
import numpy as np

from .. import set_log_level
from ..tasks import asynchronous as asynchronous_task
from ..tasks import baseline as baseline_task
from ..tasks import isochronous as isochronous_task
from ..tasks import synchronous_cardiac as synchronous_cardiac_task
from ..tasks import synchronous_respiration as synchronous_respiration_task
from ..tasks._config import N_DEVIANT, N_TARGET
from ._utils import fq_deviant, fq_target, stream, verbose


@click.command()
@click.option(
    "--duration",
    prompt="Duration of the baseline (seconds)",
    help="Duration of the baseline in seconds.",
    type=float,
)
@verbose
def baseline(duration: float, verbose: str) -> None:
    """Run a baseline task."""
    set_log_level(verbose)
    baseline_task(duration)


@click.command()
@click.option(
    "--delay",
    prompt="Delay between 2 stimulus (seconds)",
    help="Delay between 2 stimulus in seconds.",
    type=float,
)
@fq_target
@fq_deviant
@verbose
def isochronous(delay: float, target: float, deviant: float, verbose: str) -> None:
    """Run an isochronous task."""
    set_log_level(verbose)
    isochronous_task(delay, target=target, deviant=deviant)


@click.command()
@click.option(
    "--delays",
    help="Min and max delays between 2 stimuli in seconds.",
    type=(float, float),
    default=(0.5, 1.5),
    show_default=True,
)
@fq_target
@fq_deviant
@verbose
def asynchronous(
    delays: tuple[float, float], target: float, deviant: float, verbose: str
) -> None:
    """Run an asynchronous task."""
    set_log_level(verbose)
    # create random peak position based on the min/max delays requested
    if delays[0] <= 0:
        raise ValueError("The minimum delay must be strictly positive.")
    if delays[1] <= 0:
        raise ValueError("The maximum delay must be strictly positive.")
    rng = np.random.default_rng()
    delays = rng.uniform(low=delays[0], high=delays[1], size=N_TARGET + N_DEVIANT - 1)
    peaks = np.hstack(([0], np.cumsum(delays)))
    asynchronous_task(peaks, target=target, deviant=deviant)


@click.command()
@stream
@click.option(
    "--ch-name",
    prompt="Respiration channel name",
    help="Name of the respiration channel in the stream.",
    type=str,
)
@fq_target
@fq_deviant
@verbose
def synchronous_respiration(
    stream: str, ch_name: str, target: float, deviant: float, verbose: str
) -> None:
    """Run a synchronous respiration task."""
    set_log_level(verbose)
    synchronous_respiration_task(stream, ch_name, target=target, deviant=deviant)


@click.command()
@stream
@click.option(
    "--ch-name",
    prompt="ECG channel name",
    help="Name of the ECG channel in the stream.",
    type=str,
)
@click.option(
    "--delay",
    prompt="Target delay between 2 stimulus (seconds)",
    help="Target delay between 2 stimulus in seconds.",
    type=float,
)
@fq_target
@fq_deviant
@verbose
def synchronous_cardiac(
    stream: str, ch_name: str, delay: float, target: float, deviant: float, verbose: str
) -> None:
    """Run a synchronous cardiac task."""
    set_log_level(verbose)
    synchronous_cardiac_task(stream, ch_name, delay, target=target, deviant=deviant)
