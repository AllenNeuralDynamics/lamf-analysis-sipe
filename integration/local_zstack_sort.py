import subprocess
import logging
from typing import Iterable
from pathlib import Path


logger = logging.getLogger(__name__)


def sort_local_zstacks(
    local_zstack_sorter: str,
    local_zstack_paths: Iterable[str],
    local_zstack_output_dir: Path,
    use_dask: bool = False,
    n_processes: int = 2,
    verbose: bool = False,
):
    """
    >>> non_dask_completed_process = sort_local_zstacks((
    ...  "dist/lamf_analysis.exe",
    ...  [
    ...   "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
    ...   "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
    ...  ],
    ...  Path("C:/local-zstack-test/sorted/no-dask"),
    ...  False,
    ... )
    >>> dask_completed_process = sort_local_zstacks((
    ...  "dist/lamf_analysis.exe",
    ...  [
    ...   "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
    ...   "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
    ...   "C:/local-zstack-test/unsorted/1427719737_local_z_stack2.tiff",
    ...   "C:/local-zstack-test/unsorted/1427719737_local_z_stack3.tiff",
    ...  ],
    ...  Path("C:/local-zstack-test/sorted/dask"),
    ...  True,
    ...  2,
    ... )
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

    if use_dask:
        args.extend([
            "--use_dask",
            "--n_processes",
            str(n_processes)
        ])

    logger.debug(f"Starting sorting subprocess: {args=}")
    return subprocess.run(args, check=True)


# if __name__ == "__main__":
#     import os
#     import time
#     import argparse

#     logging.basicConfig()

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--use_dask",
#         action="store_true",
#         help="Use dask parallel processing.",
#     )
#     parser.add_argument(
#         "--use_multiprocess_pool",
#         action="store_true",
#         help="Use concurrent.futures to run multiple processes.",
#     )
#     parser.add_argument(
#         "--number_of_processes",
#         type=int,
#         default=2,
#     )

#     args = parser.parse_args()

#     if (use_dask := args.use_dask):
#         logger.info(f"Using dask: {use_dask=}")
#     output_dir_root = os.environ.get(
#         "ZSTACK_OUTPUT_DIR_ROOT",
#         "C:/local-zstack-test/",
#     )
#     output_dir = (
#         Path(output_dir_root)
#         / ("dask" if use_dask else "no-dask")
#         / str(int(time.time()))
#     )
#     logger.info(f"Output directory: {output_dir=}")

#     output_dir.mkdir(parents=True, exist_ok=True)

#     start_time = time.time()
#     sort_args = (
#         "dist/lamf_analysis.exe",
#         [
#             "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
#             "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
#             "C:/local-zstack-test/unsorted/1427719737_local_z_stack2.tiff",
#             "C:/local-zstack-test/unsorted/1427719737_local_z_stack3.tiff",
#         ],
#         output_dir,
#         args.use_dask,
#     )
#     if args.use_multiprocess_pool:
#         logger.info(f"Using multiprocess pool: {args.use_multiprocess_pool=}")
#         logger.setLevel(logging.DEBUG)
#         sort_local_zstacks_parallel(
#             *sort_args, n_processes=args.number_of_processes)
#     else:
#         sort_local_zstacks(*sort_args)
#     end_time = time.time()
#     logger.info(f"Sorting took {end_time - start_time:.2f} seconds")
