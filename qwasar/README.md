# Qwasar Season 03 projects

Two portfolio projects from the Qwasar upskill tracks, each self-contained with its own
uv environment and a gitignored `data/` directory (datasets are fetched on first run).

| Project | Track | Deliverables |
|---|---|---|
| [`visa_for_lisa/`](visa_for_lisa/) | Machine Learning | `visa_for_lisa.ipynb` (+ `loan_model.py` production script) |
| [`drive_me_crazy/`](drive_me_crazy/) | Data Science | `dataset_analysis.ipynb`, `drive_me_crazy_tradi.ipynb`, `drive_me_crazy_pdformer.ipynb`, `presentation.txt`, `lookerstudio_url.txt` |

Run any project:

```
cd <project> && uv sync && uv run jupyter lab
```

Notebooks are self-contained (Qwasar accepts only the listed files), so small helpers are
repeated across notebooks on purpose.
