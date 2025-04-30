import subprocess
import logging
from typing import Iterable, Optional
from pathlib import Path


logger = logging.getLogger(__name__)


def sort_local_zstacks(
    local_zstack_sorter: str,
    local_zstack_paths: Iterable[str],
    local_zstack_output_dir: Path,
    n_threads: Optional[int] = None,
    verbose: bool = False,
):
    """
    Notes
    -----
    - Intended to be directly embedded as a file in the mesoscope_workflow
    - mesoscope_workflow is a 3.9.5 python environment running on windows 10 (as of 043025)
    """
    args = [
        local_zstack_sorter,
    ]

    if verbose:
        args.append("--verbose")

    args.extend([
        "sort_zstacks",
        "--zstack_paths",
        *local_zstack_paths,
        "--output_dir",
        local_zstack_output_dir.as_posix(),
    ])

    if n_threads is not None:
        args.extend([
            "--n_threads",
            str(n_threads)
        ])

    logger.debug(f"Starting sorting subprocess: {args=}")
    return subprocess.run(args, check=True)
