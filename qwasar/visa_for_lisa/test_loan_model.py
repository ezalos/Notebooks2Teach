# ABOUTME: Smoke tests for loan_model.py: the pipeline fits on a small synthetic frame
# ABOUTME: and predict returns one probability in [0, 1] per input row.
import numpy as np
import pandas as pd

import loan_model

COLUMNS = ["ID", "Age", "Experience", "Income", "ZIP Code", "Family", "CCAvg", "Education",
           "Mortgage", "Personal Loan", "Securities Account", "CD Account", "Online", "CreditCard"]


def synthetic(n: int = 60, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "ID": np.arange(n), "Age": rng.integers(23, 67, n), "Experience": rng.integers(-3, 43, n),
        "Income": rng.integers(8, 224, n), "ZIP Code": rng.integers(90000, 96000, n),
        "Family": rng.integers(1, 5, n), "CCAvg": rng.uniform(0, 10, n), "Education": rng.integers(1, 4, n),
        "Mortgage": rng.integers(0, 600, n), "Securities Account": rng.integers(0, 2, n),
        "CD Account": rng.integers(0, 2, n), "Online": rng.integers(0, 2, n), "CreditCard": rng.integers(0, 2, n),
    })
    df["Personal Loan"] = (df["Income"] > 120).astype(int)
    return df[COLUMNS]


def test_train_writes_model_and_learns_income_rule(tmp_path):
    csv = tmp_path / "loans.csv"
    synthetic().to_csv(csv, index=False)
    model = loan_model.train(csv, model_path=tmp_path / "m.joblib")
    assert (tmp_path / "m.joblib").exists()
    rich = synthetic(seed=1).query("Income > 180")
    assert loan_model.predict(model, rich).mean() > 0.5


def test_predict_returns_one_probability_per_row():
    df = synthetic()
    model = loan_model.build_pipeline().fit(df, df["Personal Loan"])
    proba = loan_model.predict(model, df.drop(columns=["Personal Loan"]))
    assert proba.shape == (len(df),)
    assert ((proba >= 0) & (proba <= 1)).all()
