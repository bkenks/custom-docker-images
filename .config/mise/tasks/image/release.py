#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///
#MISE description="Validate a release tag and publish a GitHub release at the current pushed commit"
#MISE raw=true

import os
import subprocess
import sys
import json
from pathlib import Path

def get_image_tag_names() -> dict[str, str]:
    data = json.loads(Path(os.environ["PATHFILE_DATA"]).read_text())
    return data["images"]


def prompt_image_tag_name(image_tag_names: dict[str, str]) -> str:
    for image, tag_name in image_tag_names.items():
        print(f"  {image} -> {tag_name}")
    image = input("image alias: ").strip()
    if image not in image_tag_names:
        sys.exit(f"image:release: unknown image alias '{image}'; expected one of the above")
    return image_tag_names[image]


def prompt_revision() -> str:
    revision = input("revision: ").strip()
    if not revision.isdigit():
        sys.exit(f"image:release: revision '{revision}' must be a number")
    return revision


def compose_release_tag() -> str:
    tag_name = prompt_image_tag_name(get_image_tag_names())
    version = input("version: ").strip()
    revision = prompt_revision()
    return f"{tag_name}/{version}-r{revision}"


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
    publish_release(compose_release_tag())
except subprocess.CalledProcessError as error:
    sys.exit(error.returncode)
