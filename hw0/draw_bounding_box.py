from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2


@dataclass
class BoundingBox:
    left: int
    right: int
    top: int
    bottom: int


PROJECT_ROOT = Path.cwd()
RED = (0, 0, 255)
THICKNESS = 3


def get_bounding_boxes(bounding_box_path: Path):
    """Read the bounding boxes from the plain text file at ``bounding_box_path``.

    Args:
        bounding_box_path (Path): Path to the bounding box description file

    Returns:
        List[BoundingBox]: A list of bounding boxes read from the file
    """

    def parse_line(line: str) -> BoundingBox:
        left, bottom, right, top, *_ = map(int, line.split())
        return BoundingBox(left, right, top, bottom)

    with bounding_box_path.open("r") as f:
        return [parse_line(line) for line in f]


def draw_bounding_boxes(
    image_path: Path, bounding_boxes: Iterable[BoundingBox], output_path: Path
):
    """Draw bounding boxes to the image.

    Args:
        image_path (Path): Path to the image to be drawn
        bounding_boxes (Iterable[BoundingBox]): Bounding box of each object.
        output_path (Path): Place to store the result, save to \
              ``{output_path}/output.png`` if ``output_path`` is a directory
    """

    image = cv2.imread(str(image_path))

    for bounding_box in bounding_boxes:
        image = cv2.rectangle(
            image,
            (bounding_box.left, bounding_box.bottom),
            (bounding_box.right, bounding_box.top),
            color=RED,
            thickness=THICKNESS,
        )

    if output_path.is_dir():
        output_path = output_path / "output.png"

    cv2.imwrite(str(output_path), image)


def main():
    """Entry point of the application."""

    bounding_boxes = get_bounding_boxes(PROJECT_ROOT / "data" / "bounding_box.txt")

    draw_bounding_boxes(
        image_path=PROJECT_ROOT / "data" / "image.png",
        bounding_boxes=bounding_boxes,
        output_path=PROJECT_ROOT / "data" / "output.png",
    )


if __name__ == "__main__":
    main()
