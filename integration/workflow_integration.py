import subprocess
from typing import Iterable


def sort_local_zstacks(
    local_zstack_sorter: str,
    local_zstack_paths: Iterable[str],
    local_zstack_output_dir: str,
    use_dask: bool = False,
):
    args = [
        local_zstack_sorter,
        "sort_zstacks",
        "--zstack_paths",
        *local_zstack_paths,
        "--output_dir",
        str(local_zstack_output_dir),
    ]

    if use_dask:
        args.append("--use_dask")

    return subprocess.run(args, check=True)


if __name__ == "__main__":
    import time
    import argparse
    import pathlib
    import logging

    logging.basicConfig()

    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use_dask",
        action="store_true",
        help="Use dask parallel processing.",
    )

    args = parser.parse_args()

    if (use_dask := args.use_dask):
        logger.info(f"Using dask: {use_dask=}")
    output_dir = (
        pathlib.Path("C:/local-zstack-test/")
        / ("dask" if use_dask else "no-dask")
        / str(int(time.time()))
    )
    logger.info(f"Output directory: {output_dir=}")
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    sort_local_zstacks(
        "dist/lamf_analysis.exe",
        [
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack2.tiff",
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack3.tiff",
        ],
        output_dir.as_posix(),
        args.use_dask,
    )
    end_time = time.time()
    logger.info(f"Sorting took {end_time - start_time:.2f} seconds")
