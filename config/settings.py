from dataclasses import dataclass
from pathlib import Path


QUALITY_PRESETS = {
    "maxima": {
        "quality": 95,
        "method": 6,
        "speed": 1,
    },
    "balanceada": {
        "quality": 80,
        "method": 5,
        "speed": 4,
    },
    "web": {
        "quality": 55,
        "method": 4,
        "speed": 6,
    },
    "ultra": {
        "quality": 45,
        "method": 3,
        "speed": 8,
    },
}


@dataclass
class AppConfig:
    input_dir: Path
    output_dir: Path
    output_format: str
    resize_enabled: bool
    resize_mode: str | None
    max_size: int | None
    quality_preset: str
    lossless_enabled: bool
    max_workers: int

    @staticmethod
    def from_user_input():
        print("=== CONFIGURACIÓN DEL CONVERSOR ===\n")

        input_dir = Path(
            input("Carpeta de entrada: ").strip()
        )

        output_dir = Path(
            input("Carpeta de salida: ").strip()
        )

        output_format = input(
            "Formato de salida (webp/avif): "
        ).strip().lower()

        while output_format not in ["webp", "avif"]:
            output_format = input(
                "Formato inválido. Elige webp o avif: "
            ).strip().lower()

        resize_answer = input(
            "¿Deseas ajustar dimensiones máximas? (s/n): "
        ).strip().lower()

        resize_enabled = resize_answer == "s"

        resize_mode = None
        max_size = None

        if resize_enabled:
            resize_mode = input(
                "Limitar ancho o altura? (ancho/altura): "
            ).strip().lower()

            while resize_mode not in ["ancho", "altura"]:
                resize_mode = input(
                    "Valor inválido. Escribe ancho o altura: "
                ).strip().lower()

            max_size = int(
                input("Valor máximo en píxeles: ").strip()
            )

        quality_preset = input(
            "Preset de calidad (maxima/balanceada/web/ultra): "
        ).strip().lower()

        while quality_preset not in QUALITY_PRESETS:
            quality_preset = input(
                "Preset inválido. "
                "Elige maxima/balanceada/web/ultra: "
            ).strip().lower()

        lossless_answer = input(
            "¿Modo lossless? (s/n): "
        ).strip().lower()

        lossless_enabled = lossless_answer == "s"

        max_workers = int(
            input("Número de hilos paralelos: ").strip()
        )

        return AppConfig(
            input_dir=input_dir,
            output_dir=output_dir,
            output_format=output_format,
            resize_enabled=resize_enabled,
            resize_mode=resize_mode,
            max_size=max_size,
            quality_preset=quality_preset,
            lossless_enabled = lossless_enabled,
            max_workers=max_workers,
        )