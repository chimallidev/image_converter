from pathlib import Path


class FileUtils:
    @staticmethod
    def ensure_directory_exists(directory: Path):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )