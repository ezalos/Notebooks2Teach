# ABOUTME: Pre-fetches every wheel a Linux x86_64 `uv sync --frozen` would download, rate-capped,
# ABOUTME: so `docker build` can install with --no-index --find-links instead of hitting PyPI at line rate.
"""Usage (from a project dir holding uv.lock):  uv run --with packaging ../wheelhouse.py [--python 3.13]

Downloads go to ./wheelhouse/ one at a time via `curl --limit-rate 25M` (the household line
rule: bulk transfers capped at 25 MB/s, never in parallel). Existing files are skipped, so the
script is safe to re-run. Then:

    docker build --build-arg UV_ARGS="--no-index --find-links /wheelhouse" -t <image> .
"""
import argparse
import subprocess
import sys
import tomllib
from pathlib import Path

from packaging.tags import compatible_tags, cpython_tags
from packaging.utils import parse_wheel_filename

LIMIT = "25M"
PLATFORMS = [f"manylinux_2_{minor}_x86_64" for minor in range(36, 4, -1)] + [
    "manylinux2014_x86_64", "manylinux2010_x86_64", "manylinux1_x86_64", "linux_x86_64"]


def supported_tags(python: str) -> dict:
    major, minor = (int(x) for x in python.split("."))
    tags = list(cpython_tags((major, minor), platforms=PLATFORMS)) + list(
        compatible_tags((major, minor), platforms=PLATFORMS))
    return {t: i for i, t in enumerate(tags)}  # lower index = better match


def pick_wheel(wheels: list[dict], ranking: dict) -> dict | None:
    best, best_rank = None, len(ranking)
    for w in wheels:
        name = w["url"].rsplit("/", 1)[-1]
        try:
            _, _, _, tags = parse_wheel_filename(name)
        except Exception:
            continue
        rank = min((ranking.get(t, len(ranking)) for t in tags), default=len(ranking))
        if rank < best_rank:
            best, best_rank = w, rank
    return best


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--python", default="3.13")
    ap.add_argument("--lock", type=Path, default=Path("uv.lock"))
    ap.add_argument("--dest", type=Path, default=Path("wheelhouse"))
    args = ap.parse_args()

    ranking = supported_tags(args.python)
    lock = tomllib.load(args.lock.open("rb"))
    args.dest.mkdir(exist_ok=True)
    todo, skipped, total = [], [], 0
    for pkg in lock["package"]:
        if "registry" not in pkg.get("source", {}):
            continue
        wheel = pick_wheel(pkg.get("wheels", []), ranking)
        if wheel is None:
            skipped.append(pkg["name"])  # no Linux wheel: platform-specific package or sdist-only
            continue
        todo.append(wheel)
        total += wheel.get("size", 0)
    print(f"{len(todo)} wheels, {total / 1e6:.0f} MB at {LIMIT}/s; no Linux wheel for: {skipped or 'none'}")

    for i, w in enumerate(todo, 1):
        name = w["url"].rsplit("/", 1)[-1]
        out = args.dest / name
        if out.exists() and out.stat().st_size == w.get("size", out.stat().st_size):
            continue
        print(f"[{i}/{len(todo)}] {name} ({w.get('size', 0) / 1e6:.1f} MB)", flush=True)
        subprocess.run(["curl", "-sSL", "--limit-rate", LIMIT, "-o", str(out), w["url"]], check=True)
    print("done:", sum(f.stat().st_size for f in args.dest.iterdir()) / 1e6, "MB in", args.dest)


if __name__ == "__main__":
    main()
