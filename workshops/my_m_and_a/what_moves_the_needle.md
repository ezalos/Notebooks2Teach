# My M and A — what moves the needle

Merging three customer exports from an acquired company into one warehouse schema.
Every number below was measured by running `my_m_and_a.py` on the three real Only Wood files.

## The 60-second version

This project has no modelling in it at all — it is **a chain of decisions, each of which changes
the answer to "how many customers did we buy?"**. The same three files legitimately produce
30 000, 28 499, 28 487 or 28 486 customers depending on how carefully you clean, and only the last
number is defensible.

The work that moves the needle is **normalising before comparing**. Duplicates that differ by
capitalisation, stray quotes or a type prefix are invisible until you remove capitalisation, stray
quotes and type prefixes.

## What actually moved the needle

| step | effect |
|---|---|
| **Parsing each file in its own dialect** | table 2 loaded naively returns **9 999 rows, not 10 000** — the first customer becomes the header |
| **Stripping table 3's type prefixes** | `string_Male`, `"integer_26"`, `boolean_1`, `character_M` → usable values |
| **Validating the email key** | `forgottoask@woodinc` appears **499 times**; dedup on it merges 499 strangers into one person |
| **Normalising gender** | six encodings (`Male/M/0/Female/F/1`) → two |
| **Normalising country** | ten spellings → one, and `12` / `1` → missing (not invented) |
| **De-duplicating on a validated key** | 30 000 rows → **28 486 customers**, 0 duplicate emails |

Final: **28 486 customers**, gender {Male 14 697, Female 13 789}, country resolved for 14 290 and
missing for 14 196, ages 18–99.

## The decoding problem, and how to answer it with evidence

Three of the files use `0` and `1` for gender. Does `1` mean male or female? The data answers it:

- 30 000 rows contain **19 email addresses that appear in more than one file**.
- Exactly **3** of those pair a coded value with a written one.
- All three say the same thing: **`0` is Male** (`fadel.roberto@`, `gerhold_keenan@`, `howell_arron@`).

Three customers is thin, and the migration notes should say so — but *"0 = Male, based on three
customers present in two systems"* is a sentence a reviewer can check. "0 = Male" with no
justification is not.

**The transferable habit:** when a column's meaning is undocumented, look for records that appear
twice. Overlap is free documentation.

## Main pitfalls

| pitfall | what it looks like | cost |
|---|---|---|
| **A load that does not raise** | `pd.read_csv` returns a DataFrame for all three files | two of them are wrong, and one silently deletes a customer |
| **Deduplicating on an unvalidated key** | `drop_duplicates("email")` | 499 unrelated customers collapse into one |
| **Inventing a country** | table 2 has no country column; every other row says USA | filling it is a fabrication about 10 000 people |
| **Treating `12` as data** | a country recorded as `12`, 1 682 times | junk mapped to missing is honest; junk mapped to "USA" is not |
| **Guessing the 0/1 encoding** | a coin flip dressed as a decision | the data contains the answer |
| **Parsing and cleaning in one function** | one unreadable loader | separate them: parse first, clean second |
| **Committing the CSVs** | the brief fails the project on sight | `data/`, `*.db`, `*.csv` in `.gitignore` — which is why the function takes CSV *contents*, not filenames |

**Also real, and easy to miss:** 489 rows in table 2 have **no email at all** (996 across the
three), so those customers have no key. And `age` in table 2 contains values like `"50years"` —
the column is text, and not uniformly so.

## Reconciliation: the step nobody teaches

A load that reports no error is not a verified load. Four checks, and the pair that matters:

- **row count** and **distinct emails** together. Rows doubling while distinct emails stay flat is
  the signature of a **duplicate load** — running the migration script twice. Either check alone
  misses it.
- **null rate per column**, to catch a column that arrived empty from a name mismatch.
- **round trip**: read it back out, compare as text, expect zero differing rows.

## Where to demo it

| point | open |
|---|---|
| the finished merge | `my_m_and_a.py` |
| dialects, the naive-load data loss, the target schema | `01_schemas_and_formats.ipynb` |
| normalisation, the 0/1 evidence, the placeholder key | `02_merge_keys_duplicates.ipynb` |
| explicit SQL schema, reconciliation, the duplicate-load signature | `03_sql_loading_checks.ipynb` |
