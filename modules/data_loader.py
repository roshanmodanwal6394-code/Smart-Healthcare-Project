import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = [
    "PatientID",
    "Age",
    "Gender",
    "Department",
    "Condition",
    "AdmissionDate",
    "LengthOfStay",
    "Admissions",
    "BloodGroup"
]


def load_data(file_path=None):
    if file_path is None:
        file_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "patient_records.csv"
        )

    df = pd.read_csv(file_path)

    return validate_data(df)


def validate_data(df):
    df = df.copy()

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
        )

    df = df[REQUIRED_COLUMNS]

    df["PatientID"] = df["PatientID"].astype(str)

    for column in [
        "Age",
        "LengthOfStay",
        "Admissions"
    ]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df["AdmissionDate"] = pd.to_datetime(
        df["AdmissionDate"],
        errors="coerce"
    )

    for column in [
        "Gender",
        "Department",
        "Condition",
        "BloodGroup"
    ]:
        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    original_count = len(df)

    df = df.dropna(
        subset=[
            "Age",
            "LengthOfStay",
            "Admissions",
            "AdmissionDate"
        ]
    )

    removed_rows = original_count - len(df)

    df = df.drop_duplicates(
        subset=["PatientID"]
    )

    df = df[
        (df["Age"] >= 0)
        & (df["Age"] <= 120)
        & (df["LengthOfStay"] >= 0)
        & (df["Admissions"] >= 0)
    ].copy()

    df["Age"] = df["Age"].astype(int)
    df["LengthOfStay"] = df["LengthOfStay"].astype(int)
    df["Admissions"] = df["Admissions"].astype(int)

    return df.reset_index(drop=True), {
        "removed_rows": removed_rows,
        "total_rows": len(df)
    }