import logging
from typing import Any, Iterable, Optional
from pathlib import Path
import tifffile
from copy import deepcopy
from dask.distributed import Client
from dask import delayed, compute

from lamf_analysis.ophys import zstack


logger = logging.getLogger(__name__)


def sort_zstack_path(
    zstack_path: Path,
    output_dir: Path,
    dry_run: bool = False,
):
    if dry_run:
        logger.debug(f"Dry run enabled. Skipping sort: {dry_run=}")
        return

    logger.debug(f"Registering zstacks: {zstack_path=}")
    zstack_reg, channels_saved = zstack.register_local_zstack_from_raw_tif(
        zstack_path)
    for ch_ind, channel in enumerate(channels_saved):
        logger.debug(f"Saving channel: {ch_ind=}")
        tifffile.imsave(
            output_dir / f"{zstack_path.stem}_reg_ch_{channel}.tif",
            zstack_reg[ch_ind]
        )


def split_list_into_chunks(
    input_list: list[Any],
    num_chunks: int,
) -> list[list[Any]]:
    """Splits a list into `num_chunks` approximately equal parts.
    """
    if num_chunks <= 0:
        raise ValueError("Number of chunks must be greater than 0.")

    avg = len(input_list) / float(num_chunks)
    chunks = []
    last = 0.0

    while last < len(input_list):
        chunks.append(input_list[int(last):int(last + avg)])
        last += avg

    return chunks


def sort_zstacks(
    zstack_paths: Iterable[Path],
    output_dir: Path,
    n_threads: Optional[int] = None,
    dry_run: bool = False,
):
    """
    >>> zstack_paths = [
    ...  Path(r"\\allen\programs\mindscope\workgroups\learning\pilots\online_motion_correction\mouse_746542\1406177928_local_z_stack0.tiff"),
    ...  Path(r"\\allen\programs\mindscope\workgroups\learning\pilots\online_motion_correction\mouse_746542\1406177928_local_z_stack1.tiff"),
    ...  Path(r"\\allen\programs\mindscope\workgroups\learning\pilots\online_motion_correction\mouse_746542\1406177928_local_z_stack2.tiff"),
    ...  Path(r"\\allen\programs\mindscope\workgroups\learning\pilots\online_motion_correction\mouse_746542\1406177928_local_z_stack3.tiff")
    ... ]
    >>> output_dir = Path(r"\\allen\aind\scratch\SIPE\mesoscope-test")
    >>> output_dir.mkdir(exist_ok=True, parents=True)
    >>> no_dask_dir = output_dir / "no-dask"
    >>> no_dask_dir.mkdir(exist_ok=True, parents=True)
    >>> sort_zstacks(
    ...  zstack_paths,
    ...  no_dask_dir,
    ...  use_dask=False)
    >>> dask_dir = output_dir / "dask"
    >>> dask_dir.mkdir(exist_ok=True, parents=True)
    >>> sort_zstacks(
    ...  zstack_paths,
    ...  dask_dir,
    ...  use_dask=True)
    """
    zstack_paths = list(zstack_paths)
    logger.debug(f"Sorting zstacks: {zstack_paths=}")
    if n_threads is None:
        logger.debug(f"Not using dask threading: {n_threads=}")
        return [
            sort_zstack_path(zstack_path, output_dir, dry_run)
            for zstack_path in zstack_paths
        ]

    logger.debug(f"Using dask threading: {n_threads=}")
    client = Client(processes=False)  # use threads
    results = compute(*(
        delayed(sort_zstacks)(zstack_paths_chunk, output_dir, dry_run)
        for zstack_paths_chunk in split_list_into_chunks(
            deepcopy(zstack_paths),
            n_threads,
        )
    ))
    client.close()
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LAMF analysis entry point",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Run in verbose mode",
    )
    # Create the subparser group
    subparsers = parser.add_subparsers(
        help="Available commands: sort_zstacks",
    )

    # Create the "add" subcommand parser
    sort_parser = subparsers.add_parser(
        "sort_zstacks",
        help="Sort zstacks.",
    )
    sort_parser.add_argument(
        "--zstack_paths",
        type=Path,
        nargs="+",
        help="Paths to zstack files",
    )
    sort_parser.add_argument(
        "--output_dir",
        type=Path,
        help="Output directory for sorted zstacks",
    )
    sort_parser.add_argument(
        "--n_threads",
        type=int,
        default=None,
        help="Number of dask threads to use for sorting.",
    )
    sort_parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Run in dry run mode (no sorting).",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig()
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    sort_zstacks(
        zstack_paths=args.zstack_paths,
        output_dir=args.output_dir,
        n_threads=args.n_threads,
        dry_run=args.dry_run,
    )
