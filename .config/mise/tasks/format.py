#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///

import subprocess
import sys

try:
    subprocess.run(["treefmt"], check=True)
except subprocess.CalledProcessError as error:
    sys.exit(error.returncode)
