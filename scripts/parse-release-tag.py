#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///

import re
import sys
from pathlib import Path

RELEASE_TAG_PATTERN = re.compile(r"^(?P<image>[a-z0-9-]+)/(?P<upstream>.+)-r(?P<revision>[0-9]+)$")


def parse_release_tag(tag_name: str) -> None:
    match = RELEASE_TAG_PATTERN.match(tag_name)
    if not match:
        sys.exit(f"::error::Release tag '{tag_name}' must be '<image>/<upstream-version>-r<N>'")
    image_name = match["image"]
    upstream_version = match["upstream"]

    dockerfile = Path("images") / image_name / "Dockerfile"
    if not dockerfile.is_file():
        sys.exit(f"::error::No Dockerfile at {dockerfile}")

    from_pin_pattern = re.compile(
        rf"^FROM [^ ]+:{re.escape(upstream_version)}([-@ ]|$)", re.MULTILINE
    )
    if not from_pin_pattern.search(dockerfile.read_text()):
        sys.exit(f"::error::{dockerfile} FROM does not pin upstream version '{upstream_version}'")

    print(f"image={image_name}")
    print(f"upstream={upstream_version}")
    print(f"version={tag_name.partition('/')[2]}")


if len(sys.argv) != 2:
    sys.exit("usage: parse-release-tag.py <image>/<upstream-version>-r<N>")
parse_release_tag(sys.argv[1])
