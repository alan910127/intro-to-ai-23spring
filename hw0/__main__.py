#!/usr/bin/env python3

from pathlib import Path

import click


@click.group()
def cli():
    """Run commands."""


@cli.command()
@click.option("--input", "-i", type=click.Path(exists=True), default=None)
@click.option("--output", "-o", type=click.Path(), default=None)
@click.option("--box", "-b", type=click.Path(exists=True), default=None)
def box(input: str, output: str, box: str):
    """Draw the bounding boxes on the image."""

    import src.draw_bounding_box

    kwargs = {}

    if box is not None:
        kwargs["bounding_box_path"] = Path(box)

    if input is not None:
        kwargs["image_path"] = Path(input)

    if output is not None:
        kwargs["output_path"] = Path(output)

    src.draw_bounding_box.main(**kwargs)


@cli.command()
@click.option("--input", "-i", type=click.Path(exists=True), default=None)
@click.option("--output", "-o", type=click.Path(), default=None)
def bg(input: str, output: str):
    """Detect the motion of the video and extract it to a video."""

    import src.remove_background

    kwargs = {}

    if input is not None:
        kwargs["video_path"] = Path(input)

    if output is not None:
        kwargs["output_path"] = Path(output)

    src.remove_background.main(**kwargs)


if __name__ == "__main__":
    cli()
