# ABOUTME: Downloads the datasets the Qwasar projects provide, into workshops/data/.
# ABOUTME: Rate-capped and sequential; the files are gitignored and must never be committed.
"""Usage: uv run get_data.py          (~4 MB, five files)

Every workshop notebook runs on the real data its project ships. Nothing is generated or
simulated, so this download is required before a session.

  boston.csv                     My Tu Verras      (Qwasar's own copy; note the target is MDEV)
  only_wood_customer_us_{1,2,3}  My M and A        (the three exports to merge)
  googleplaystore.csv            My MobApp Studio  (the Kaggle set the brief links to, mirrored
                                                   on GitHub because Kaggle requires an account)

My Linear Regression needs no download: its subject generates its own data.
"""
import subprocess
from pathlib import Path

DATA = Path(__file__).parent / "data"
FILES = [
    ("boston.csv", "https://storage.googleapis.com/qwasar-public/track-ds/boston.csv"),
    ("only_wood_customer_us_1.csv", "https://storage.googleapis.com/qwasar-public/only_wood_customer_us_1.csv"),
    ("only_wood_customer_us_2.csv", "https://storage.googleapis.com/qwasar-public/only_wood_customer_us_2.csv"),
    ("only_wood_customer_us_3.csv", "https://storage.googleapis.com/qwasar-public/only_wood_customer_us_3.csv"),
    ("googleplaystore.csv",
     "https://raw.githubusercontent.com/elaysason/Google-Play-Apps/main/googleplaystore.csv"),
]


def main() -> None:
    DATA.mkdir(exist_ok=True)
    for name, url in FILES:
        out = DATA / name
        if out.exists():
            print(f"  have {name}")
            continue
        print(f"  fetching {name}", flush=True)
        subprocess.run(["curl", "-sSL", "--limit-rate", "25M", "-o", str(out), url], check=True)
    total = sum(f.stat().st_size for f in DATA.glob("*.csv"))
    print(f"done: {total / 1e6:.1f} MB in {DATA}")


if __name__ == "__main__":
    main()
