# Drive Me Crazy — traffic flow forecasting (Qwasar, Season 03 Data Science)

Traditional baselines and a compact PDFormer (Propagation Delay-aware Dynamic Long-range
Transformer, AAAI 2023) on PeMS04 / PeMS07 / PeMS08 / NYCTaxi.

| deliverable | file |
|---|---|
| dataset analysis | `dataset_analysis.ipynb` |
| traditional models (Persistence, Historical Average, Ridge) | `drive_me_crazy_tradi.ipynb` |
| PDFormer + delay ablation | `drive_me_crazy_pdformer.ipynb` |
| findings on propagation delay | `propagation_delay_findings.md` |
| presentation | `presentation.txt` |
| dashboard (Looker Studio equivalent) | `dashboard.ipynb`, pointed to by `lookerstudio_url.txt` |

Notebooks are self-contained (the same ~100-line loader / metrics block is repeated at the top of
each) because the platform accepts only the notebooks. They write small CSVs to `results/`, which the
dashboard reads. Datasets (~160 MB) and checkpoints live in `data/` and are never committed.

## Run locally

```
uv sync
uv run get_data.py                     # PeMS from a HuggingFace mirror, NYCTaxi from the PDFormer authors' Drive
uv run jupyter lab                     # then run the notebooks in the order of the table above
```

Headless, in order: `uv run jupyter nbconvert --to notebook --execute --inplace <notebook>.ipynb`.

Environment knobs (read by every notebook): `DMC_DATASETS=PEMS08,NYCTaxi` restricts the datasets,
`DMC_EPOCHS=1` turns the PDFormer notebook into a smoke test (one epoch on a 2 000-window slice).
The full PDFormer sweep (30 epochs PeMS04/08/NYCTaxi, 15 PeMS07, plus the no-delay ablation on
PeMS04/08/NYCTaxi) takes about two hours on an RTX 4090.

## Run in Docker (GPU)

```
docker build -t drive-me-crazy .
docker run --rm --gpus all -v "$PWD:/app" drive-me-crazy                                   # smoke (~1 min + data download)
docker run --rm --gpus all -v "$PWD:/app" -e DMC_EPOCHS=0 -e DMC_DATASETS= drive-me-crazy   # full run
```

The image (python 3.13 + uv, ~12 GB because torch bundles CUDA) runs `get_data.py` then the four
notebooks in place; with the bind mount the executed notebooks and `results/` land on the host. Add
`--user "$(id -u):$(id -g)" -e HOME=/tmp` to keep those files owned by you. On a rate-capped
connection, pre-fetch the wheels with `uv run --with packaging ../wheelhouse.py` and build with
`--build-arg UV_ARGS="--no-index --find-links /wheelhouse"`.
