# My Tu Verras — what moves the needle

House-price prediction on Qwasar's `boston.csv` (506 towns, 13 features).
Every number below was measured by running `my_tu_verras.ipynb`, not estimated.

## The 60-second version

The baseline linear model scores **RMSE 4.72** against **9.71** for predicting the average — it
removes about half the error. But the score moves by **±0.68 purely from which towns land in
validation**, which is larger than most of the changes worth testing. So the first thing that moves
the needle is not a transform, it is **comparing on many splits instead of one**.

After that: the wins come from **fixing shapes, not swapping models** — `LSTAT` bends and price is
skewed, so logging both buys more than any amount of tuning a linear model. A random forest finds
that curvature on its own and wins outright.

## What actually moved the needle

30 splits, paired against the baseline on the same splits.

| change | Δ RMSE | wins | read it as |
|---|---|---|---|
| **RandomForest** | **−1.47** | 30/30 | the biggest single gain; it captures the curvature without being told |
| log(price) + log(LSTAT) + RM² | −0.65 | 27/30 | the best *linear* model |
| log(price) + log(LSTAT) | −0.56 | 29/30 | two transforms, no new model |
| log(LSTAT) | −0.49 | 30/30 | fixes the bend visible in the scatter plot |
| log(price) | −0.37 | 30/30 | fixes the right-skewed target |
| drop `B` | +0.07 | 5/30 | **costs nothing** — inside the noise |
| drop censored from train | +0.17 | 8/30 | hurts |
| RobustScaler | **0.000** | — | exactly zero, by construction |

**Split-to-split noise on the baseline: ±0.68.** Anything smaller than that is unresolvable on a
single split.

Final: RandomForest, **test RMSE 2.82**, measured once.

## Three results worth more than the gains

**1. The scaler does exactly nothing — `0.000`, not "almost nothing".**
Ordinary least squares has a closed-form solution invariant to feature scaling: multiply a column
by 1000 and its coefficient divides by 1000, leaving every prediction identical. It is not a
useless technique; it is useless *here*. It starts mattering with gradient descent, a penalty
(Ridge/Lasso), or a distance (KNN/SVM).

**2. Dropping `B` is free.**
`B` is `1000(Bk − 0.63)²` where Bk is the proportion of Black residents; scikit-learn removed this
dataset in 1.2 over it. Dropping it costs **+0.07 RMSE — inside the ±0.68 noise band**. There is no
performance argument for keeping it, so the ethical call costs nothing. Decide deliberately and
write the decision down.

**3. Removing inconvenient rows from training can hurt.**
Dropping the 16 censored towns from training makes validation **worse** (+0.17): they are the
model's only examples of expensive places, and validation still contains them.

## Main pitfalls

| pitfall | what it looks like | cost |
|---|---|---|
| **`MDEV`, not `MEDV`** | `AttributeError: 'DataFrame' object has no attribute 'MEDV'`. The subject text says `MEDV`; the file header says `MDEV` | an hour, and it reads like a broken load |
| **Comparing on one split** | a change "wins" by 0.4 and gets kept forever — or loses and gets discarded | silently wrong conclusions, both directions |
| **"No missing values" read as "clean"** | `dropna()` removes nothing, so the data looks fine | the censoring and the dead columns go unnoticed |
| **The ceiling at 50** | 16 towns at exactly 50.0, the most frequent value *and* the maximum | the worst error in the notebook (13.73) is one of them |
| **Expecting a cone** | the residual spread is **U-shaped on 30/30 splits** (4.47, 3.35, 2.94, 5.35, 5.83) | prescribing a fix for the wrong shape |
| **"log fixed the heteroscedasticity"** | it improved RMSE on 30/30 splits, and Breusch-Pagan got *worse* (49.4 → 56.5, worse on 19/30) | conflating a better score with a satisfied assumption |

**The censoring, in one line:** 2.8 % of training towns are capped at 50, but **11.3 % of the
model's most expensive predictions** are — a four-fold concentration. No transform recovers a value
that was never written down. Measure it, state it, move on.

## Where to demo it

| point | open |
|---|---|
| the lever ranking with the noise band | `my_tu_verras.ipynb`, "What actually improves it" |
| `MDEV`, the ceiling, the dead columns | `01_first_look.ipynb` |
| the dumb baseline and paired comparison | `02_baseline_and_method.ipynb` |
| the U-shape, Breusch-Pagan, censoring | `03_errors_and_residuals.ipynb` |
