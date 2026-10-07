#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///
#MISE description="Validate a release tag and publish a GitHub release at the current pushed commit"
#USAGE arg "<tag>" help="Release tag, e.g. nginx/1.27.3-r1"

import os
import subprocess
import sys


def get_git_output(*args: str) -> str:
    completed = subprocess.run(["git", *args], check=True, stdout=subprocess.PIPE, text=True)
    return completed.stdout.strip()


def publish_release(tag: str) -> None:
    subprocess.run(["scripts/parse-release-tag.py", tag], check=True, stdout=subprocess.DEVNULL)

    if get_git_output("status", "--porcelain"):
        sys.exit("image:release: working tree is dirty; commit and push first")

    subprocess.run(["git", "fetch", "--quiet", "origin"], check=True)
    commit = get_git_output("rev-parse", "HEAD")
    if not get_git_output("branch", "--remotes", "--contains", commit):
        sys.exit(f"image:release: {commit} is not pushed to origin; push first")

    subprocess.run(
        ["gh", "release", "create", tag, "--target", commit, "--title", tag, "--generate-notes"],
        check=True,
    )


try:
    publish_release(os.environ["usage_tag"])
except subprocess.CalledProcessError as error:
    sys.exit(error.returncode)
