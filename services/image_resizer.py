from PIL import Image


class ImageResizer:
    @staticmethod
    def resize_image(
        image: Image.Image,
        resize_mode: str,
        max_size: int,
    ):
        original_width, original_height = image.size

        if resize_mode == "ancho":
            if original_width <= max_size:
                return image

            ratio = max_size / original_width

            new_width = max_size
            new_height = int(original_height * ratio)

        else:
            if original_height <= max_size:
                return image

            ratio = max_size / original_height

            new_height = max_size
            new_width = int(original_width * ratio)

        return image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS,
        )