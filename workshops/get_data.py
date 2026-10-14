# ABOUTME: Downloads the three Only Wood customer exports used by the My M and A project into data/.
# ABOUTME: Rate-capped and sequential; the files are gitignored and must never be committed.
"""Usage: uv run get_data.py          (~2.5 MB, three files)

The workshop notebooks do not need these: they build six-row surrogates with the same
pathologies, so a session works offline. Fetch the real exports when you move on to the
project itself.
"""
import subprocess
from pathlib import Path

DATA = Path(__file__).parent / "data"
URL = "https://storage.googleapis.com/qwasar-public/only_wood_customer_us_{n}.csv"


def main() -> None:
    DATA.mkdir(exist_ok=True)
    for n in (1, 2, 3):
        out = DATA / f"only_wood_customer_us_{n}.csv"
        if out.exists():
            print(f"  have {out.name}")
            continue
        print(f"  fetching {out.name}", flush=True)
        subprocess.run(["curl", "-sSL", "--limit-rate", "25M", "-o", str(out), URL.format(n=n)], check=True)
    print(f"done: {sum(f.stat().st_size for f in DATA.glob('*.csv')) / 1e6:.1f} MB in {DATA}")


if __name__ == "__main__":
    main()
