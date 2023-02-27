from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Tuple

import cv2
import numpy as np

GREEN = (0, 255, 0)


@contextmanager
def video_capture(video_path: Path):
    capture = cv2.VideoCapture(str(video_path))
    try:
        yield capture
    finally:
        capture.release()


@contextmanager
def video_writer(video_path: Path, fourcc: int, fps: int, resolution: Tuple[int, int]):
    writer = cv2.VideoWriter(str(video_path), fourcc, fps, resolution)
    try:
        yield writer
    finally:
        writer.release()


def frames(capture: cv2.VideoCapture) -> Iterator[cv2.Mat]:
    while capture.isOpened():
        is_success, frame = capture.read()

        if not is_success:
            break

        yield frame


def get_difference(
    previous_frame: Optional[cv2.Mat], current_frame: cv2.Mat
) -> Tuple[Optional[cv2.Mat], cv2.Mat]:
    """Get the difference from the previous frame to the current frame.

    Args:
        previous_frame (cv2.Mat): The previous frame in the video
        current_frame (cv2.Mat): The current frame in the video

    Returns:
        Tuple[Optional[cv2.Mat], cv2.Mat]: (difference, current_frame)
    """

    if previous_frame is None:
        return None, current_frame

    diff = cv2.absdiff(previous_frame, current_frame)
    return diff, current_frame


def transform_nonblack(
    frame: cv2.Mat, to_color: Tuple[int, int, int] = GREEN
) -> cv2.Mat:
    """Transform the non-black pixels in the frame to the given color.

    Args:
        frame (cv2.Mat): The original frame
        to_color (Tuple[int, int, int]): Color to transform to. Defaults to GREEN.

    Returns:
        cv2.Mat: The transformed frame
    """

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray_frame, 25, 255, cv2.THRESH_BINARY_INV)

    green = np.ones_like(frame) * to_color
    green = green.astype(np.uint8)

    green[thresh != 0] = frame[thresh != 0]

    return green


def main(
    video_path: Path = Path.cwd() / "data" / "video.mp4",
    output_path: Path = Path.cwd() / "data" / "output.mp4",
    resolution_ratio: float = 0.5,
) -> None:
    if output_path.is_dir():
        output_path = output_path / "output.mp4"

    with video_capture(video_path) as capture:
        fps = round(capture.get(cv2.CAP_PROP_FPS))
        width = round(capture.get(cv2.CAP_PROP_FRAME_WIDTH) * resolution_ratio)
        height = round(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) * resolution_ratio)

        with video_writer(
            output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width * 2, height)
        ) as writer:

            previous_frame: Optional[cv2.Mat] = None

            for frame in frames(capture):
                frame = cv2.resize(frame, (width, height))
                diff_frame, previous_frame = get_difference(previous_frame, frame)

                if diff_frame is None:
                    continue

                green_diff_frame = transform_nonblack(diff_frame)
                stacked_frame = cv2.hconcat([previous_frame, green_diff_frame])
                writer.write(stacked_frame)


if __name__ == "__main__":
    main(capture_resolution=(1920, 1080))
