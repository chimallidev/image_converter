from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image
import pillow_avif

from config.settings import (
    AppConfig,
    QUALITY_PRESETS,
)
from services.image_loader import ImageLoader
from services.image_resizer import ImageResizer
from services.progress_logger import ProgressLogger
from utils.file_utils import FileUtils


class ImageConverter:
    def __init__(self, config: AppConfig):
        self.config = config

        self.preset = QUALITY_PRESETS[
            config.quality_preset
        ]

    def process_images(self):
        FileUtils.ensure_directory_exists(
            self.config.output_dir
        )

        image_files = ImageLoader.load_images(
            self.config.input_dir
        )

        total_files = len(image_files)

        if total_files == 0:
            print("No se encontraron imágenes.")
            return

        progress_bar = ProgressLogger.create_progress_bar(
            total_files
        )

        with ThreadPoolExecutor(
            max_workers=self.config.max_workers
        ) as executor:

            futures = []

            for image_path in image_files:
                future = executor.submit(
                    self._process_single_image,
                    image_path,
                )

                futures.append(future)

            for future in futures:
                future.result()
                progress_bar.update(1)

        progress_bar.close()

        print("\nProceso finalizado.")

    def _process_single_image(
        self,
        image_path: Path,
    ):
        with Image.open(image_path) as image:

            has_alpha = (
                image.mode in ("RGBA", "LA")
                or "transparency" in image.info
            )

            if has_alpha:
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")

            original_size = image.size

            if self.config.resize_enabled:
                image = ImageResizer.resize_image(
                    image=image,
                    resize_mode=self.config.resize_mode,
                    max_size=self.config.max_size,
                )

            relative_path = image_path.relative_to(
                self.config.input_dir
            )

            output_relative = relative_path.with_suffix(
                f".{self.config.output_format}"
            )

            output_path = (
                self.config.output_dir
                / output_relative
            )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._save_image(
                image=image,
                output_path=output_path,
            )

            print(
                f"\nConvertida: {image_path.name} | "
                f"{original_size} -> {image.size}"
            )

    def _save_image(
        self,
        image,
        output_path: Path,
    ):
        output_format = self.config.output_format.upper()

        if output_format == "AVIF":

            image.save(
                output_path,
                format="AVIF",
                quality=self.preset["quality"],
                speed=self.preset["speed"],
            )

        else:

            image.save(
                output_path,
                format="WEBP",
                quality=self.preset["quality"],
                method=self.preset["method"],
            )