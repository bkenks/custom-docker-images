#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///
#MISE description="Build an image locally for the host platform and load it as <image>:dev"
#USAGE arg "<image>" help="Image folder name under images/"

import os
import subprocess
import sys
from pathlib import Path

image = os.environ["usage_image"]
context = Path("images") / image
if not (context / "Dockerfile").is_file():
    sys.exit(f"image:build: no Dockerfile at {context}/Dockerfile")
build_command = ["docker", "buildx", "build", "--load", "--tag", f"{image}:dev", context]
try:
    subprocess.run(build_command, check=True)
except subprocess.CalledProcessError as error:
    sys.exit(error.returncode)
