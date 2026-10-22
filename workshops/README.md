# Mentorship workshops

One directory per Qwasar project, three one-hour workshops each: a notebook mixing short
explanations with exercises the students fill in, plus a **solved twin** under `solutions/`,
executed with its outputs, to run live if the room gets stuck.

| project | workshops |
|---|---|
| [`my_tu_verras/`](my_tu_verras/) — house prices | [first look](my_tu_verras/01_first_look.ipynb) · [baseline and method](my_tu_verras/02_baseline_and_method.ipynb) · [errors and residuals](my_tu_verras/03_errors_and_residuals.ipynb) |
| [`my_m_and_a/`](my_m_and_a/) — merging three customer exports | [schemas and formats](my_m_and_a/01_schemas_and_formats.ipynb) · [keys and duplicates](my_m_and_a/02_merge_keys_duplicates.ipynb) · [SQL loading and reconciliation](my_m_and_a/03_sql_loading_checks.ipynb) |
| [`my_mobapp_studio/`](my_mobapp_studio/) — Play Store market report | [cleaning as decisions](my_mobapp_studio/01_cleaning_as_decisions.ipynb) · [charts that do not lie](my_mobapp_studio/02_charts_that_dont_lie.ipynb) · [the report as an experiment](my_mobapp_studio/03_report_as_experiment.ipynb) |
| [`my_linear_regression/`](my_linear_regression/) — least squares from scratch | [least squares](my_linear_regression/01_least_squares.ipynb) · [gradient descent](my_linear_regression/02_gradient_descent.ipynb) · [learning rate](my_linear_regression/03_learning_rate_and_diagnostics.ipynb) |

## Real data only

Every notebook runs on **the data its Qwasar project provides** — Qwasar's own `boston.csv`, the
three Only Wood exports, the Play Store export the brief links to, and for My Linear Regression the
`X`/`y` and `f(x)` the subject itself defines. Nothing is simulated: a lesson drawn from invented
data is a lesson about invented data, and the numbers in the prose would not match what a student
sees in their own notebook.

So the download is required:

```
uv sync                     # from the repository root
cd workshops && uv run get_data.py
uv run jupyter lab
```

A notebook whose dataset is missing says so and tells you to run `get_data.py`.

## How the notebooks are built

- Exercises are a function stub with `# TODO` comments, followed by a self-check cell that prints
  `PASS` / `not yet` instead of raising — a student can run the whole notebook top to bottom
  without meeting a traceback.
- Each section ends with a `**Rule of thumb:**` or `**The punchline:**` line, which is what
  students tend to write down.
- **Every number quoted in the prose was measured by running the solved notebook.** Where a claim
  and the output disagreed, the claim was changed — several times, including a leak demo that
  turned out to be exactly zero and a "cone" that turned out to be a U.

## A note on the graded projects

These teach the techniques and the method; they stop short of handing over a finished deliverable.
The exercises work one column, one decision or one function at a time, and the assembled pipeline,
the classes and the report stay the students' to write.
