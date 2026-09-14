# ABOUTME: Production pipeline for the Visa For Lisa loan-acceptance model (Galaxy Bank).
# ABOUTME: `train` fits + evaluates + saves model.joblib; `predict` scores a raw customer export.
import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

TARGET = "Personal Loan"
DROP = ["ID", "ZIP Code", TARGET]
MODEL_PATH = Path("model.joblib")


class Cleaner(BaseEstimator, TransformerMixin):
    """Same cleaning as the notebook: drop identifiers, fix the sign of Experience."""

    def fit(self, X, y=None):
        self.columns_ = [c for c in X.columns if c not in DROP]
        return self

    def transform(self, X):
        X = X[self.columns_].copy()
        X["Experience"] = X["Experience"].abs()
        return X


def build_pipeline(seed: int = 42) -> Pipeline:
    return Pipeline([
        ("clean", Cleaner()),
        ("rf", RandomForestClassifier(n_estimators=300, random_state=seed, n_jobs=-1)),
    ])


def train(csv: Path, seed: int = 42, model_path: Path | None = None) -> Pipeline:
    df = pd.read_csv(csv)
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, stratify=y, random_state=seed)
    model = build_pipeline(seed).fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, proba >= 0.5, target_names=["declined", "accepted"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, proba):.4f}")
    # Refit on everything before shipping: the hold-out was only there to report honest numbers.
    model.fit(df, y)
    if model_path is not None:
        joblib.dump(model, model_path)
        print(f"saved {model_path}")
    return model


def predict(model: Pipeline, customers: pd.DataFrame) -> np.ndarray:
    """Probability of accepting a loan offer, one per row of a raw customer export."""
    return model.predict_proba(customers)[:, 1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_train = sub.add_parser("train", help="fit on a labelled CSV and write model.joblib")
    p_train.add_argument("csv", type=Path)
    p_train.add_argument("--out", type=Path, default=MODEL_PATH)
    p_pred = sub.add_parser("predict", help="score a CSV of customers with model.joblib")
    p_pred.add_argument("csv", type=Path)
    p_pred.add_argument("--model", type=Path, default=MODEL_PATH)
    args = parser.parse_args()

    if args.cmd == "train":
        train(args.csv, model_path=args.out)
    else:
        model = joblib.load(args.model)
        for p in predict(model, pd.read_csv(args.csv)):
            print(f"{p:.4f}")


if __name__ == "__main__":
    main()
