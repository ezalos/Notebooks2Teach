# ABOUTME: Downloads the three Only Wood customer exports used by the My M and A project into data/.
# ABOUTME: Rate-capped and sequential; the files are gitignored and must never be committed.
"""Usage: uv run get_data.py          (~4 MB, four files)

The M and A workshops do not need their files: they build six-row surrogates with the same
pathologies, so a session works offline. The MobApp Studio workshops use the real Play Store
export when it is present and generate a stand-in when it is not.
"""
import subprocess
from pathlib import Path

DATA = Path(__file__).parent / "data"
URL = "https://storage.googleapis.com/qwasar-public/only_wood_customer_us_{n}.csv"
# The My MobApp Studio dataset is published on Kaggle, which needs an account; this is the same
# 10,841-row file mirrored on GitHub, so the workshops work without one.
PLAYSTORE = ("googleplaystore.csv",
             "https://raw.githubusercontent.com/elaysason/Google-Play-Apps/main/googleplaystore.csv")


def fetch(name: str, url: str) -> None:
    out = DATA / name
    if out.exists():
        print(f"  have {out.name}")
        return
    print(f"  fetching {out.name}", flush=True)
    subprocess.run(["curl", "-sSL", "--limit-rate", "25M", "-o", str(out), url], check=True)


def main() -> None:
    DATA.mkdir(exist_ok=True)
    for n in (1, 2, 3):
        fetch(f"only_wood_customer_us_{n}.csv", URL.format(n=n))
    fetch(*PLAYSTORE)
    print(f"done: {sum(f.stat().st_size for f in DATA.glob('*.csv')) / 1e6:.1f} MB in {DATA}")


if __name__ == "__main__":
    main()
