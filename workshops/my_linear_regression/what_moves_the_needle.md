# My Linear Regression — what moves the needle

Least squares and gradient descent built from scratch, on the data the subject itself generates
(`X = 4*rand(100,1)`, `y = 10 + 2X + noise`) and the function it defines
(`f(x) = 3 + (x−[2,6])ᵀ(x−[2,6])`). Every number below was measured by running
`my_linear_regression.ipynb`.

## The 60-second version

This project has **no data cleaning and no modelling judgement** — the data is generated from a
known rule. What decides whether it takes an evening or a week is almost entirely **numpy
mechanics**, and one bug in particular costs more than everything else combined.

The intellectual content is in the written questions, not the code: *why* the closed form stops
being usable, *what* the learning rate actually does, and *what* "it converges" promises.

## What actually moved the needle

| | result |
|---|---|
| **θ from the normal equation** | **[10.215, 1.885]** against the generating 10 and 2 |
| MSE at that θ | 0.807 |
| residual std | 0.898 against the noise std of 1.0 — the fit absorbs a sliver of the noise |
| **gradient descent on the same problem** | **[10.215, 1.885]** — identical, after 1 000 iterations instead of one inversion |
| training complexity | $O(nd^2 + d^3)$: **0.28 ms at 10 features → 67 ms at 400** (240× for 40× the features) |
| prediction complexity | $O(nd)$: **0.03 ms → 0.27 ms** over the same range (9×) |

**The asymmetry is the lesson.** Training is the expensive half and it explodes with the number of
*features*, not rows. That is why the normal equation becomes unusable long before prediction does,
and why gradient descent exists at all.

## The learning rate, measured

| learning rate | after 50 steps | f |
|---|---|---|
| 0.01 | `[1.272, 3.815]` | 8.31 — right direction, far too slow |
| 0.1 – 0.9 | `[2, 6]` | **3** — converged |
| **1.0** | `[0, 0]` | **43** — oscillates for ever, exactly back at the start |
| 1.1 | `[-18199, -54597]` | 3.3e9 — diverged |

The tipping point is **not folklore**: this bowl has second derivative 2, so one step multiplies
the distance to the minimum by $(1-2\alpha)$. Below 1 it shrinks; at exactly 1 the factor is $-1$
(same distance, other side, for ever); above 1 it grows.

Largest rate that converges **within 200 iterations: 0.98**, not 1.0 — and that gap is the answer
to the subject's question about iterations. **Convergence is a promise about the limit; your
patience is a budget.**

Convergence rate: **geometric**, a constant factor per step, so a straight line on a log plot. At
α = 0.1 the factor is 0.8 — about ten steps per decimal digit.

## Main pitfalls — ranked by time lost

**1. The silent shape broadcast. This is the whole project.**
`y` is `(100, 1)`. The moment one side of a subtraction becomes `(100,)` — a `ravel()`, a `.values`,
an index — numpy broadcasts into a **(100, 100)** matrix and the MSE returns **10.77 instead of
0.807**. Thirteen times wrong, no error, no warning. Every other bug announces itself; this one does
not.

```python
def mean_squared_error(y_predicted, y_label):
    assert y_predicted.shape == y_label.shape, (y_predicted.shape, y_label.shape)
    ...
```

One line. Keep it in the submission.

**2. The history that is one point repeated.**
`self.current_ -= learning_rate * gradient` mutates in place, so appending `self.current_` appends
the *same object* every time. The history ends up holding **1 distinct point instead of 51**, and
the path plot the subject explicitly asks for is a single dot. Either rebind
(`self.current_ = self.current_ - ...`) or append `.copy()`.

**3. Panicking at 10 iterations.**
The subject's own example is `grad.optimize(10)` at lr 0.1. From a random start that lands around
**f = 3.3**, not 3. Nothing is broken — ~25 steps gives three decimals, ~50 gives eight. People
spend an evening debugging correct code.

**4. `inv` instead of `pinv`.**
Call `bias_column` twice (easy — `X_new` looks like a sensible thing to pass) and you get two
identical columns, `XᵀX` is singular, and `np.linalg.inv` raises `LinAlgError: Singular matrix`.
`pinv` returns the same answer and carries on.

**5. Expecting the two halves to meet.**
`LeastSquaresRegression` and `GradientDescentOptimizer` are independent in the subject, and the
optimizer is generic — it takes any `f` and `fprime` and knows nothing about regression. Students
try to weld the regression into the optimizer and tangle both. Keep them apart; *then* bridge them
voluntarily (feed it the MSE and its gradient) and confirm you land on the same θ. That is the
moment the project clicks.

**6. Expecting the regression to behave like `f`.**
`f` is a perfectly round bowl (curvature 2 in both directions), so descent walks **straight** to the
minimum. The regression's MSE is a stretched valley, so its path plunges then crawls. Same
algorithm, different geometry — and the reason feature scaling exists: the same regression with the
feature ×1000, same learning rate, **overflows to `nan`**.

## Where to demo it

| point | open |
|---|---|
| the finished answer and every written question | `my_linear_regression.ipynb` |
| the shape assert, bias column, residuals | `01_least_squares.ipynb` |
| the `.copy()` trap, the 3D plot, the history path | `02_gradient_descent.ipynb` |
| the four regimes, the 0.98 edge, scaling, loss curves | `03_learning_rate_and_diagnostics.ipynb` |
