# ABOUTME: Reference solution for the Qwasar "My M and A" project: merge 3 messy customer CSVs into one schema.
# ABOUTME: Scratch exploration to size the workshop; the teaching version lives in the workshop notebooks.
import csv
import io
from pathlib import Path
import re

import pandas as pd

SCHEMA = ["gender", "firstname", "lastname", "email", "age", "city", "country", "created_at", "referral"]


def _strip_types(s: pd.Series) -> pd.Series:
    """Table 3 prefixes every value with its type: string_Male, "integer_26", character_M, boolean_1."""
    return (s.astype(str)
            .str.replace(r'^"|"$', "", regex=True)
            .str.replace(r"^(string|integer|character|boolean|float)_", "", regex=True))


def _clean_text(s: pd.Series) -> pd.Series:
    """Names and cities carry stray quotes and backslashes from three generations of bad exports."""
    return (s.astype(str)
            .str.replace(r'[\\"]', "", regex=True)
            .str.strip()
            .replace({"": None, "nan": None, "None": None}))


def normalise_city(s: pd.Series) -> pd.Series:
    """NEW YORK / new_york / New-York all name one city: separators to spaces, then title case."""
    v = _clean_text(s).str.replace(r"[_\-]+", " ", regex=True).str.replace(r"\s+", " ", regex=True)
    return v.str.title()


def normalise_gender(s: pd.Series) -> pd.Series:
    """Male/Female/M/F/1/0 -> Male/Female.

    0 = Male, 1 = Female. Evidence, not a guess: three customers appear in two exports at once,
    explicit in one and coded in the other (fadel.roberto@, gerhold_keenan@, howell_arron@) and all
    three pair "Male" with 0. Weak (n=3) but it is the only direct evidence the data offers, and it
    agrees with the most reliable slice of the first-name check.
    """
    v = _clean_text(s).str.lower()
    return v.map({"male": "Male", "m": "Male", "0": "Male",
                  "female": "Female", "f": "Female", "1": "Female"})


def normalise_country(s: pd.Series) -> pd.Series:
    """US / USA / U.S.A. / United-State-Of-America / 12 -> United States of America; junk -> None."""
    v = _clean_text(s)
    key = v.str.lower().str.replace(r"[^a-z]", "", regex=True)
    known = {"us", "usa", "unitedstateofamerica", "unitedstatesofamerica", "unitedstates", "america"}
    return key.map(lambda k: "United States of America" if k in known else None)


def normalise_name(full: pd.Series) -> pd.DataFrame:
    """One name field -> first / last. Capitalisation is all over the place, so title-case everything."""
    v = _clean_text(full).fillna("")
    parts = v.str.split(r"\s+", n=1, expand=True)
    if parts.shape[1] == 1:
        parts[1] = None
    return pd.DataFrame({"firstname": parts[0].str.title().replace({"": None}),
                         "lastname": parts[1].str.title().replace({"": None})})


def normalise_email(s: pd.Series) -> pd.Series:
    """Lowercase, and drop anything that is not a real address (forgottoask@woodinc has no TLD)."""
    v = _clean_text(s).str.lower()
    return v.where(v.str.match(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", na=False))


def normalise_age(s: pd.Series) -> pd.Series:
    v = pd.to_numeric(_strip_types(_clean_text(s)), errors="coerce")
    return v.where(v.between(0, 120)).astype("Int64")


def _read(content, **kw) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(content) if isinstance(content, str) else content, **kw)


def my_m_and_a(content_1, content_2, content_3) -> str:
    # Table 1: a normal CSV, but with a UserName column we drop and separate first/last names.
    t1 = _read(content_1)
    df1 = pd.DataFrame({
        "gender": normalise_gender(t1.Gender),
        "firstname": _clean_text(t1.FirstName).str.title(),
        "lastname": _clean_text(t1.LastName).str.title(),
        "email": normalise_email(t1.Email),
        "age": normalise_age(t1.Age),
        "city": normalise_city(t1.City),
        "country": normalise_country(t1.Country),
    })

    # Table 2: no header, ';' separated, columns in a different order, no country at all.
    t2 = _read(content_2, sep=";", header=None, names=["age", "city", "gender", "name", "email"])
    df2 = pd.DataFrame({
        "gender": normalise_gender(t2.gender),
        **normalise_name(t2.name),
        "email": normalise_email(t2.email),
        "age": normalise_age(t2.age),
        "city": normalise_city(t2.city),
        "country": None,
    })

    # Table 3: header is comma separated but the rows are tab separated, and every value carries a type prefix.
    raw = content_3 if isinstance(content_3, str) else content_3.read()
    header, _, body = raw.partition("\n")
    t3 = _read(body, sep="\t", header=None, names=header.strip().split(","), quoting=csv.QUOTE_NONE)
    df3 = pd.DataFrame({
        "gender": normalise_gender(_strip_types(t3.Gender)),
        **normalise_name(_strip_types(t3.Name)),
        "email": normalise_email(_strip_types(t3.Email)),
        "age": normalise_age(t3.Age),
        "city": normalise_city(_strip_types(t3.City)),
        "country": normalise_country(_strip_types(t3.Country)),
    })

    merged = pd.concat([df1, df2, df3], ignore_index=True)
    merged["created_at"] = None          # neither source tracked it; the target schema expects the column
    merged["referral"] = None
    # One row per customer: email is the only identifier shared by the three systems.
    merged = (merged.dropna(subset=["email"])
              .sort_values(["email", "country"], na_position="last")
              .drop_duplicates(subset="email", keep="first")
              .reset_index(drop=True))
    return merged[SCHEMA].to_csv(index=False)


def _data_path(name):
    for up in range(4):
        candidate = Path(*([".."] * up), "data", name)
        if candidate.exists():
            return candidate
    raise FileNotFoundError("run `uv run get_data.py` in workshops/ first")


if __name__ == "__main__":
    contents = [_data_path(f"only_wood_customer_us_{i}.csv").read_text() for i in (1, 2, 3)]
    out = my_m_and_a(*contents)
    df = pd.read_csv(io.StringIO(out))
    print("merged shape:", df.shape)
    print(df.head(5).to_string())
    print("\nnulls:\n", df.isna().sum().to_string())
    print("\ngender:", df.gender.value_counts(dropna=False).to_dict())
    print("country:", df.country.value_counts(dropna=False).to_dict())
    print("age:", df.age.min(), "-", df.age.max(), "| dupe emails:", df.email.duplicated().sum())
