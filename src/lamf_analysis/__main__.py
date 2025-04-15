import logging
from typing import Iterable
from pathlib import Path
import tifffile
from dask.distributed import Client
from dask import delayed, compute

from lamf_analysis.ophys import zstack


logger = logging.getLogger(__name__)


def sort_zstack_path(
    zstack_path: Path,
    output_dir: Path
):
    logger.debug(f"Registering zstacks: {zstack_path=}")
    zstack_reg, channels_saved = zstack.register_local_zstack_from_raw_tif(
        zstack_path)
    for ch_ind, channel in enumerate(channels_saved):
        logger.debug(f"Saving channel: {ch_ind=}")
        tifffile.imsave(
            output_dir / f"{zstack_path.stem}_reg_ch_{channel}.tif",
            zstack_reg[ch_ind]
        )


def sort_zstacks(
    zstack_paths: Iterable[Path],
    output_dir: Path,
    use_dask: bool = False,
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
    if not use_dask:
        return [
            sort_zstack_path(zstack_path, output_dir)
            for zstack_path in zstack_paths
        ]

    client = Client(processes=False)
    tasks = [
        delayed(sort_zstack_path)(zstack_path, output_dir)
        for zstack_path in zstack_paths
    ]
    results = compute(*tasks)
    client.close()
    return results


if __name__ == "__main__":
    import time
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
        "--use_dask",
        action="store_true",
        help="Run in dry run mode",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig()
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    sort_start = time.time()
    sort_zstacks(
        zstack_paths=args.zstack_paths,
        output_dir=args.output_dir,
        use_dask=args.use_dask,
    )
    sort_time = time.time() - sort_start
    logger.debug(f"{sort_time=}")
