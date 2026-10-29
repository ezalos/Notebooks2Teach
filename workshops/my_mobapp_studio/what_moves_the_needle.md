# My MobApp Studio — what moves the needle

A Google Play market report for a studio deciding which category to enter.
Every number below was measured by running `my_mobapp_studio.ipynb` on the real 10 841-row export.

## The 60-second version

**One cleaning step decides the entire report.** De-duplicating 1 181 repeated app entries takes
the market from **168 billion installs to 75 billion** — skip it and you overstate by **123 %**,
with a chart to prove it and nothing in the data complaining.

**Then the recommendation flips the chart the brief asked for.** `GAME` wins the pie at 17.9 % of
installs, but it holds 945 apps, so the average game gets 14 M. `COMMUNICATION` has 315 apps and
averages **35 M** — 2.5× better odds for one new entrant. Totals describe the market; ratios
describe your chances in it, and that is what the client actually asked.

## What actually moved the needle

| step | effect | why it matters |
|---|---|---|
| **De-duplication** | 168 bn → **75 bn installs (+123 % if skipped)** | the headline number of the whole project |
| **Installs-per-app instead of totals** | GAME 14 M vs COMMUNICATION **35 M** | changes the recommendation |
| **Dropping the corrupt row** | one row explains **five** impossible values | rating 19.0, installs "Free", price "Everyone", reviews "3.0M" |
| **Excluding novelty apps from price stats** | FINANCE mean **$8.41** → median **$0.00** | the brief's own chart is misleading without it |
| **Log axes for counts** | installs span 6 orders of magnitude | a linear axis is a blank chart |

Headline answers: **~75 billion installs**, **$291 M** paid-app gross sales, 9 659 apps after
cleaning (754 paid).

## Two findings worth 30 seconds each

**Rating does not predict installs (+0.04). Neither does price (−0.01).**
Only Reviews↔Installs correlate (+0.63), and reviews are a by-product of installs. So "build a
highly-rated app and the downloads follow" is not supported by this data.

**99.9 % of installs are free apps.** Their revenue is ads and in-app purchases, neither of which
is in the dataset. $291 M is a floor for a narrow slice, not the size of the market.

## Main pitfalls

| pitfall | what it looks like | cost |
|---|---|---|
| **Skipping de-duplication** | a plausible, confident, doubled market size | the report's headline is wrong by 123 % |
| **Writing five fixes for one bug** | separate patches for rating 19.0, "Free" installs, "Everyone" price… | all five come from row 10472, shifted one column left |
| **`mean()` on a skewed column** | FINANCE "averages $8.41" | 20 novelty apps at $300–400 (`I am rich`, `I'm Rich - Trump Edition`) |
| **Trusting the pie chart** | "enter GAME, it's the biggest" | biggest *and* most crowded — the ratio says Communication |
| **False precision** | "75,322,526,427 installs" | installs are **20 buckets**; eleven digits claim accuracy the data never had. Say "roughly 75 billion" |
| **`dropna()` on ratings** | 13.6 % of apps dropped quietly | those apps have a **median of 1 review** vs 3 017 for rated apps — you delete the unpopular half of the store |
| **Reporting MSE to a client** | "Mean Squared Error: 22.2" | the units are dollars *squared*; meaningless to a VP |

## The blog post is half the submission

`link_to_blog_post.txt` is graded as a scientific experiment: assumptions, method, results,
limitations, next experiment. The most common failure is not the analysis — it is a link that
needs a login. **Open it in a private window before submitting.**

Limitations that should appear in it, each with its number:
1. 1 181 duplicates removed; skipping that step changes the headline by 123 %.
2. Installs are buckets, so every total is a lower bound.
3. Paid downloads only — ads and IAP fund 99.9 % of installs and are invisible here.
4. 13.6 % of apps have no rating, and they are the unreviewed ones.
5. A 2018 snapshot: nothing here says what is *growing*.

## Where to demo it

| point | open |
|---|---|
| the finished report and the recommendation | `my_mobapp_studio.ipynb` |
| the corrupt row, de-duplication, MNAR ratings | `01_cleaning_as_decisions.ipynb` |
| the novelty-app price trap, log axes, totals vs ratios | `02_charts_that_dont_lie.ipynb` |
| assumptions, claims-to-evidence, limitations | `03_report_as_experiment.ipynb` |
