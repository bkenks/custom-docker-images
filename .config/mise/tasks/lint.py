#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///
#MISE description="Lint workflows, Dockerfiles, and formatting"

import subprocess
import sys
from glob import glob

try:
    subprocess.run(["actionlint"], check=True)
    for dockerfile in sorted(glob("images/*/Dockerfile")):
        subprocess.run(["hadolint", dockerfile], check=True)
    subprocess.run(["treefmt", "--fail-on-change"], check=True)
except subprocess.CalledProcessError as error:
    sys.exit(error.returncode)
