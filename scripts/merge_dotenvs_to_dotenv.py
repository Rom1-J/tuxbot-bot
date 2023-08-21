from pathlib import Path


ROOT_DIR_PATH = Path(__file__).parent.parent.resolve()
ENVS_NAME = (".local", ".production")
ENVS_FILES = (".bot", ".cogs", ".postgres")


def merge(input_file_path: Path, merged_file_paths: Path) -> None:
    with open(merged_file_paths, "w") as output_file:
        for file_name in ENVS_FILES:
            with open(str(input_file_path / file_name)) as merged_file:
                for line in merged_file.readlines():
                    if line.startswith("#") or not line.strip():
                        continue

                    output_file.write(line)


def main() -> None:
    for environment in ENVS_NAME:
        merge(
            ROOT_DIR_PATH / ".envs" / environment,
            ROOT_DIR_PATH / f".env{environment}",
        )


if __name__ == "__main__":
    main()
