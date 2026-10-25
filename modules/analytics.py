import pandas as pd


def calculate_kpis(df):
    total_patients = df["PatientID"].nunique()

    total_admissions = int(
        df["Admissions"].sum()
    )

    avg_age = (
        round(df["Age"].mean(), 1)
        if not df.empty else 0
    )

    avg_stay = (
        round(df["LengthOfStay"].mean(), 1)
        if not df.empty else 0
    )

    departments = df["Department"].nunique()

    conditions = df["Condition"].nunique()

    return {
        "total_patients": total_patients,
        "total_admissions": total_admissions,
        "avg_age": avg_age,
        "avg_stay": avg_stay,
        "departments": departments,
        "conditions": conditions
    }


def department_summary(df):
    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby("Department")
        .agg(
            Patients=("PatientID", "nunique"),
            Admissions=("Admissions", "sum"),
            Average_Stay=("LengthOfStay", "mean"),
            Average_Age=("Age", "mean")
        )
        .reset_index()
    )

    result["Average_Stay"] = (
        result["Average_Stay"].round(1)
    )

    result["Average_Age"] = (
        result["Average_Age"].round(1)
    )

    return result.sort_values(
        "Patients",
        ascending=False
    )


def condition_summary(df):
    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby("Condition")
        .agg(
            Patients=("PatientID", "nunique"),
            Admissions=("Admissions", "sum"),
            Average_Stay=("LengthOfStay", "mean")
        )
        .reset_index()
    )

    result["Average_Stay"] = (
        result["Average_Stay"].round(1)
    )

    return result.sort_values(
        "Patients",
        ascending=False
    )


def monthly_admissions(df):
    if df.empty:
        return pd.DataFrame(
            columns=["Month", "Admissions"]
        )

    result = df.copy()

    result["Month"] = (
        result["AdmissionDate"]
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        result.groupby("Month")["Admissions"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    return result


def age_group_summary(df):
    if df.empty:
        return pd.DataFrame(
            columns=["Age Group", "Patients"]
        )

    result = df.copy()

    result["Age Group"] = pd.cut(
        result["Age"],
        bins=[-1, 17, 35, 50, 65, 120],
        labels=[
            "0–17",
            "18–35",
            "36–50",
            "51–65",
            "66+"
        ]
    )

    summary = (
        result.groupby(
            "Age Group",
            observed=False
        )["PatientID"]
        .nunique()
        .reset_index()
    )

    summary.columns = [
        "Age Group",
        "Patients"
    ]

    return summary


def generate_insights(df):
    if df.empty:
        return [
            "No records available for analysis."
        ]

    insights = []

    top_department = (
        df["Department"].value_counts()
    )

    if not top_department.empty:
        insights.append(
            f"**Largest department:** "
            f"{top_department.index[0]} "
            f"has {top_department.iloc[0]} patient records."
        )

    top_condition = (
        df["Condition"].value_counts()
    )

    if not top_condition.empty:
        insights.append(
            f"**Most frequent condition:** "
            f"{top_condition.index[0]}."
        )

    average_stay = df["LengthOfStay"].mean()

    insights.append(
        f"**Average length of stay:** "
        f"{average_stay:.1f} days."
    )

    older_patients = df[df["Age"] >= 65]

    insights.append(
        f"**Patients aged 65+:** "
        f"{older_patients['PatientID'].nunique()}."
    )

    return insights