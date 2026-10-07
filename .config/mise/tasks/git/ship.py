#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///
#MISE alias="ship"
#MISE description="Stage, commit, and push everything"
#USAGE arg "<message>" help="Commit message"

import os
import subprocess
import sys

try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", os.environ["usage_message"]], check=True)
    subprocess.run(["git", "push"], check=True)
except subprocess.CalledProcessError as error:
    sys.exit(error.returncode)
