import pygame
from typing import Union


class ImageLoader:
    @staticmethod
    def load_png(image_path, width: Union[int, float] = -1, height: Union[int, float] = -1):
        return ImageLoader.scale_image(pygame.image.load(image_path).convert_alpha(), width, height)

    @staticmethod
    def scale_image(image, width: Union[int, float] = -1, height: Union[int, float] = -1):
        if width == -1 and height == -1:
            return image

        image_width, image_height = image.get_size()
        # If width is -1, calculate width automatically preserving the image aspect ratio
        if width == -1:
            width = height / image_height * image_width
        if height == -1:
            height = width / image_width * image_height

        return pygame.transform.scale(image, (width, height))
