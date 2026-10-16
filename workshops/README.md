# Mentorship workshops

Seven one-hour workshops for the 42 AI-track students, each a notebook that mixes short
explanations with exercises they fill in. Every workshop has a **solved twin** under
`solutions/`, executed with its outputs, to run live if the room gets stuck.

| # | workshop | for |
|---|---|---|
| 00 | [How to know your model got better](00_methodology.ipynb) | the project they are finishing: train/validation/test, leakage, one change at a time, the logbook |
| 01 | [Three files, three dialects](my_m_and_a/01_schemas_and_formats.ipynb) | **My M and A** — reading a file before parsing it, CSV dialects, target schema |
| 02 | [Keys, duplicates and the values that lie](my_m_and_a/02_merge_keys_duplicates.ipynb) | **My M and A** — normalisation, decoding a coded column, the placeholder key |
| 03 | [Loading to SQL, and proving it worked](my_m_and_a/03_sql_loading_checks.ipynb) | **My M and A** — explicit schemas, reconciliation, round-trip |
| 01 | [The line, the cost, and the exact answer](my_linear_regression/01_least_squares.ipynb) | **My Linear Regression** — hypothesis, MSE, normal equation, residuals |
| 02 | [Walking downhill](my_linear_regression/02_gradient_descent.ipynb) | **My Linear Regression** — the gradient, the update rule, convexity |
| 03 | [The learning rate, and why scaling exists](my_linear_regression/03_learning_rate_and_diagnostics.ipynb) | **My Linear Regression** — four regimes, scaling, loss-curve diagnosis, extrapolation |
| 01 | [Cleaning is a chain of decisions](my_mobapp_studio/01_cleaning_as_decisions.ipynb) | **My MobApp Studio** — the corrupt row, duplicate scrapes (+123 % on the headline), missing-not-at-random |
| 02 | [Charts that do not lie](my_mobapp_studio/02_charts_that_dont_lie.ipynb) | **My MobApp Studio** — the mean-price trap, log scales, bucketed installs, totals vs ratios |
| 03 | [The report is the deliverable](my_mobapp_studio/03_report_as_experiment.ipynb) | **My MobApp Studio** — assumptions, claims-to-evidence, limitations, the next experiment |

## Running a session

```
uv sync          # from the repository root
uv run jupyter lab workshops/
```

Everything runs on the repository's existing environment (pandas, numpy, matplotlib,
ipywidgets, scikit-learn, sqlite3). **No dataset download is needed**: each notebook generates
the data it uses, and the M and A workshops build six-row surrogate files carrying the same
pathologies as the real exports (mixed dialects, type prefixes, six gender encodings, a
placeholder email). The MobApp Studio notebooks use the real Google Play export if
`uv run get_data.py` has fetched it, and generate an equivalent stand-in if not.

## How the notebooks are built

- Exercises are a function stub with `# TODO` comments, followed by a self-check cell that
  prints `PASS` / `not yet` instead of raising — a student can run the whole notebook top to
  bottom without ever meeting a traceback.
- Each section ends with a `**Rule of thumb:**` or `**The punchline:**` line, which is what
  students tend to write down.
- Every number quoted in the prose was measured by running the solved notebook; when a claim
  and the output disagreed, the claim was changed.

## A note on the graded projects

These workshops teach the techniques on **sub-problems and a different dataset**, never the
full deliverable. The M and A notebooks normalise one column at a time on surrogate files; the
linear-regression notebooks fit a bakery dataset rather than the subject's. The classes and
functions the students must submit stay theirs to write.
