import subprocess
import logging
from typing import Iterable
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed


logger = logging.getLogger(__name__)


def sort_local_zstacks(
    local_zstack_sorter: str,
    local_zstack_paths: Iterable[str],
    local_zstack_output_dir: Path,
    use_dask: bool = False,
):
    args = [
        local_zstack_sorter,
        "sort_zstacks",
        "--zstack_paths",
        *local_zstack_paths,
        "--output_dir",
        local_zstack_output_dir.as_posix(),
    ]

    if use_dask:
        args.append("--use_dask")

    return subprocess.run(args, check=True)


def chunk_list(input_list: list, chunk_size: int) -> list:
    """Splits a list into chunks of a specified size.
    """
    # Using list comprehension to chunk the input_list
    return [
        input_list[i:i + chunk_size]
        for i in range(0, len(input_list), chunk_size)
    ]


def sort_local_zstacks_parallel(
    local_zstack_sorter: str,
    local_zstack_paths: Iterable[str],
    local_zstack_output_dir: Path,
    use_dask: bool = False,
    n_processes: int = 2,
):
    """Uses concurrent.futures to run multiple lamf_analysis.exe sorting
     processes in parallel.
    """
    _path_list = list(local_zstack_paths)
    sort_tasks = [
        _path_list[i:i + n_processes]
        for i in range(0, len(_path_list), n_processes)
    ]
    # Use ProcessPoolExecutor to run subprocesses concurrently
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                sort_local_zstacks,
                local_zstack_sorter,
                task,
                local_zstack_output_dir,
                use_dask,
            )
            for task in sort_tasks
        ]

        # Handle results as they complete
        for future in as_completed(futures):
            try:
                result = future.result()  # Will raise if subprocess.run failed
                logger.debug(f"Subprocess completed successfully: {result}")
            except subprocess.CalledProcessError as e:
                logger.debug(f"Subprocess failed: {e}")


if __name__ == "__main__":
    import time
    import argparse

    logging.basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use_dask",
        action="store_true",
        help="Use dask parallel processing.",
    )
    parser.add_argument(
        "--use_multiprocess_pool",
        action="store_true",
        help="Use concurrent.futures to run multiple processes.",
    )
    parser.add_argument(
        "--number_of_processes",
        type=int,
        default=2,
    )

    args = parser.parse_args()

    if (use_dask := args.use_dask):
        logger.info(f"Using dask: {use_dask=}")
    output_dir = (
        Path("C:/local-zstack-test/")
        / ("dask" if use_dask else "no-dask")
        / str(int(time.time()))
    )
    logger.info(f"Output directory: {output_dir=}")

    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    sort_args = (
        "dist/lamf_analysis.exe",
        [
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack2.tiff",
            "C:/local-zstack-test/unsorted/1427719737_local_z_stack3.tiff",
        ],
        output_dir,
        args.use_dask,
    )
    if args.use_multiprocess_pool:
        logger.info(f"Using multiprocess pool: {args.use_multiprocess_pool=}")
        logger.setLevel(logging.DEBUG)
        sort_local_zstacks_parallel(
            *sort_args, n_processes=args.number_of_processes)
    else:
        sort_local_zstacks(*sort_args)
    end_time = time.time()
    logger.info(f"Sorting took {end_time - start_time:.2f} seconds")
