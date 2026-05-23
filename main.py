from config.settings import AppConfig
from services.converter import ImageConverter


def main():
    config = AppConfig.from_user_input()

    converter = ImageConverter(config)
    converter.process_images()


main()