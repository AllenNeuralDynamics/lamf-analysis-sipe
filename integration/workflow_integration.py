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
    import os
    import time
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use_dask",
        action="store_true",
        help="Use dask parallel processing.",
    )

    args = parser.parse_args()

    local_zstacks = [
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
    ]
    # mesoscope_workflow-friendly way of creating tinestamped folders
    output_dir_parts = ["C:/local-zstack-test/", ]

    if args.use_dask:
        output_dir_parts.append("dask")
    else:
        output_dir_parts.append("no-dask")

    output_dir_parts.append(str(int(time.time())))
    output_dir = os.path.join(*output_dir_parts)
    os.makedirs(output_dir, exist_ok=True)

    sort_local_zstacks(
        "dist/lamf_analysis.exe",
        local_zstacks,
        output_dir,
        args.use_dask,
    )