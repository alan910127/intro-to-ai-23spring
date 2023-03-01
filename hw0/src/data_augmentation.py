import random
from pathlib import Path
from typing import Callable, Literal

import cv2
import numpy as np

Transformer = Callable[[cv2.Mat], cv2.Mat]


def translate(offset_x: int = 0, offset_y: int = 0) -> Transformer:
    """Create a transformer that translates the image by the given offset."""

    def transformer(image: cv2.Mat) -> cv2.Mat:
        width, height = image.shape[:2]
        matrix = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        return cv2.warpAffine(image, matrix, (height, width))

    return transformer


def rotate(degree: int = 0) -> Transformer:
    """Create a transformer that rotates the image by the given angle in degree."""

    def transformer(image: cv2.Mat) -> cv2.Mat:
        width, height = image.shape[:2]
        matrix = cv2.getRotationMatrix2D((width // 2, height // 2), degree, 1)
        return cv2.warpAffine(image, matrix, (height, width))

    return transformer


def flip(axis: Literal["vertical", "horizontal", "diagonal"]) -> Transformer:
    """Create a transformer that flips the image along the given axis."""

    def transformer(image: cv2.Mat) -> cv2.Mat:
        if axis == "vertical":
            return cv2.flip(image, 0)

        if axis == "horizontal":
            return cv2.flip(image, 1)

        return cv2.flip(image, -1)

    return transformer


def scale(
    scale_x: float = 1.0, scale_y: float = 1.0, interpolation: int = cv2.INTER_AREA
) -> Transformer:
    """Create a transformer that scales the image by the given scale factor."""

    def transformer(image: cv2.Mat) -> cv2.Mat:
        return cv2.resize(
            image,
            (0, 0),
            fx=scale_x,
            fy=scale_y,
            interpolation=interpolation,
        )

    return transformer


def crop(width: int, height: int, start_x: int = 0, start_y: int = 0) -> Transformer:
    """Create a transformer that crops the image."""

    def transformer(image: cv2.Mat) -> cv2.Mat:
        return image[start_x : start_x + width, start_y : start_y + height]

    return transformer


def main(
    image_path: Path = Path.cwd() / "data" / "image.png",
) -> None:
    """Entry point of the application."""

    image = cv2.imread(str(image_path))
    width, height = image.shape[:2]

    transformers = {
        "translate": translate(
            offset_x=random.randint(0, width // 2),
            offset_y=random.randint(0, height // 2),
        ),
        "rotate": rotate(degree=random.randint(0, 360)),
        "flip": flip(axis=random.choice(["vertical", "horizontal", "diagonal"])),
        "scale": scale(scale_x=random.random() * 2, scale_y=random.random() * 2),
        "crop": crop(
            start_x=random.randint(0, width // 2),
            width=random.randint(0, width // 2),
            start_y=random.randint(0, height // 2),
            height=random.randint(0, height // 2),
        ),
    }

    for name, transformer in transformers.items():
        transformed = transformer(image)
        cv2.imwrite(str(image_path.with_stem(name)), transformed)


if __name__ == "__main__":
    main()
