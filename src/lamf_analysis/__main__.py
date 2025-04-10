from lamf_analysis.ophys import zstack



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LAMF analysis entry point",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to the config file.",
    )