from pyspark.sql import SparkSession


def create_spark_session():
    return (
        SparkSession.builder
        .appName("SmartHealthcareAnalyzer")
        .master("local[*]")
        .config(
            "spark.sql.shuffle.partitions",
            "4"
        )
        .config(
            "spark.ui.enabled",
            "false"
        )
        .getOrCreate()
    )


def run_spark_sql(df, query):
    spark = None

    try:
        spark = create_spark_session()

        spark_df = spark.createDataFrame(
            df.copy()
        )

        spark_df.createOrReplaceTempView(
            "patients"
        )

        result = spark.sql(query)

        return result.toPandas()

    finally:
        if spark is not None:
            spark.stop()


def get_sample_queries():
    return {
        "Department Summary": """
            SELECT
                Department,
                COUNT(*) AS PatientRecords,
                SUM(Admissions) AS TotalAdmissions,
                ROUND(AVG(LengthOfStay), 2) AS AverageStay
            FROM patients
            GROUP BY Department
            ORDER BY PatientRecords DESC
        """,

        "Condition Analysis": """
            SELECT
                Condition,
                COUNT(*) AS PatientRecords,
                ROUND(AVG(Age), 1) AS AverageAge,
                ROUND(AVG(LengthOfStay), 1) AS AverageStay
            FROM patients
            GROUP BY Condition
            ORDER BY PatientRecords DESC
        """,

        "Age Group Analysis": """
            SELECT
                CASE
                    WHEN Age < 18 THEN '0-17'
                    WHEN Age < 36 THEN '18-35'
                    WHEN Age < 51 THEN '36-50'
                    WHEN Age < 66 THEN '51-65'
                    ELSE '66+'
                END AS AgeGroup,
                COUNT(*) AS PatientRecords
            FROM patients
            GROUP BY
                CASE
                    WHEN Age < 18 THEN '0-17'
                    WHEN Age < 36 THEN '18-35'
                    WHEN Age < 51 THEN '36-50'
                    WHEN Age < 66 THEN '51-65'
                    ELSE '66+'
                END
            ORDER BY AgeGroup
        """,

        "Longest Hospital Stays": """
            SELECT
                PatientID,
                Age,
                Department,
                Condition,
                LengthOfStay
            FROM patients
            ORDER BY LengthOfStay DESC
            LIMIT 10
        """
    }