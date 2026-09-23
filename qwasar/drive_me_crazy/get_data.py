# ABOUTME: Downloads the four traffic datasets (PeMS04/07/08, NYCTaxi) into data/, skipping existing files.
# ABOUTME: PeMS from a HuggingFace mirror via rate-capped curl; NYCTaxi from the PDFormer authors' Google Drive.
"""Usage: uv run get_data.py            (≈ 160 MB total; nothing is ever committed)

PeMS0x.npz      — (T, N, 3) float array: traffic flow, occupancy, speed per 5-min step per sensor
adj_PEMS0x.npy  — (N, N) binary symmetric sensor adjacency (road-network neighbours)
NYCTaxi/    — LibCity atomic files: NYCTaxi.geo (15×5 grid cells), NYCTaxi.grid (30-min inflow/outflow)
"""
import pickle
import subprocess
from pathlib import Path

import gdown
import numpy as np

DATA = Path(__file__).parent / "data"
HF = "https://huggingface.co/datasets/jimmygao3218/{ds}/resolve/main/{name}"
PDFORMER_DRIVE_FOLDER = "176Uogr_kty02NQcM9gB2ZT_ngulEhb0H"  # github.com/BUAABIGSCity/PDFormer README


def curl(url: str, out: Path) -> None:
    if out.exists():
        print(f"  have {out.name}")
        return
    print(f"  fetching {out.name}", flush=True)
    subprocess.run(["curl", "-sSL", "--limit-rate", "25M", "-o", str(out), url], check=True)


def main() -> None:
    DATA.mkdir(exist_ok=True)
    for ds in ["PEMS04", "PEMS07", "PEMS08"]:
        print(ds)
        curl(HF.format(ds=ds, name=f"{ds}.npz"), DATA / f"{ds}.npz")
        npy = DATA / f"adj_{ds}.npy"
        if not npy.exists():
            pkl = DATA / f"adj_{ds}.pkl"
            curl(HF.format(ds=ds, name=pkl.name), pkl)
            # The mirror ships the adjacency as a pickled ndarray. Unpickling third-party data can run
            # code, so it happens here once, is checked to be a plain square 0/1 matrix, and is re-saved
            # as .npy; the notebooks only ever np.load the .npy.
            adj = np.asarray(pickle.load(pkl.open("rb")))
            assert adj.ndim == 2 and adj.shape[0] == adj.shape[1] and set(np.unique(adj)) <= {0, 1}, adj.shape
            np.save(npy, adj.astype(np.float32))
            pkl.unlink()

    print("NYCTaxi")
    nyc = DATA / "NYCTaxi"
    nyc.mkdir(exist_ok=True)
    wanted = {"NYCTaxi.geo", "NYCTaxi.grid", "config.json"}
    if all((nyc / f).exists() for f in wanted):
        print("  have all files")
        return
    files = gdown.download_folder(id=PDFORMER_DRIVE_FOLDER, skip_download=True, quiet=True)
    for f in files:
        name = Path(f.path).name
        if f.path.startswith("NYCTaxi/") and name in wanted and not (nyc / name).exists():
            print(f"  fetching {name}", flush=True)
            gdown.download(id=f.id, output=str(nyc / name), quiet=True)


if __name__ == "__main__":
    main()
