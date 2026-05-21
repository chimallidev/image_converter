from tqdm import tqdm


class ProgressLogger:
    @staticmethod
    def create_progress_bar(total: int):
        return tqdm(
            total=total,
            desc="Convirtiendo imágenes",
            unit="img",
        )