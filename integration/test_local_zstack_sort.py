import time
import pathlib
from pydantic_settings import BaseSettings
from .local_zstack_sort import sort_local_zstacks  # TODO: fix by making package uv


class Settings(BaseSettings):

    local_zstack_sorter: str = "dist/lamf_analysis.exe"
    local_zstack_paths: list[str] = [
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack2.tiff",
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack3.tiff",
    ]
    local_zstack_output_dir: pathlib.Path = pathlib.Path(
        "C:/local-zstack-test/dask"
    )
    n_threads: int = 2
    verbose: bool = False


if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    settings = Settings().model_dump()
    logger.info(f"Settings: {settings}")
    start_time = time.time()
    completed_process = sort_local_zstacks(**settings)
    logger.info(f"Sorting time: {time.time() - start_time}s")
    assert completed_process.returncode == 0, (
        "Non-dask local zstack sorter failed with return code:"
        f" {completed_process.returncode}"
    )
