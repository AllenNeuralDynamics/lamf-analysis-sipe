import pathlib
from pydantic_settings import BaseSettings
from integration.local_zstack_sort import sort_local_zstacks


class Settings(BaseSettings):

    local_zstack_sorter: str = "dist/lamf_analysis.exe"
    local_zstack_paths: list[str] = [
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack0.tiff",
        "C:/local-zstack-test/unsorted/1427719737_local_z_stack1.tiff",
    ]
    local_zstack_output_dir: pathlib.Path = pathlib.Path(
        "C:/local-zstack-test/sorted/no-dask"
    )
    use_dask: bool = False
    n_processes: int = 2
    verbose: bool = False


if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    settings = Settings().model_dump()
    logger.info(f"Settings: {settings}")
    completed_process = sort_local_zstacks(**settings)

    assert completed_process.returncode == 0, (
        "Non-dask local zstack sorter failed with return code:"
        f" {completed_process.returncode}"
    )
