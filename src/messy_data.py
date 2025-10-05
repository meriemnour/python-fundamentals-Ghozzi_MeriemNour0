import pandas as pd


def main() -> None:  # Added return type annotation
    print("=== Pandas Data Display ===\n")  # Task 7: Data cleaning - duplicates
    print("7. Data Cleaning - Duplicates:")
    print("from the slides")

    # What your CSV actually looks like
    messy_data = pd.DataFrame(
        {
            "user_id": [1, 2, 2, 3, None, 4, 5],
            "age": [25, None, 30, -5, 150, "unknown", 41],
            "salary": [50000, 75000, 75000, None, 999999, "60,000", 85000],
            "email": [
                "alice@test.com",
                "",
                "bob@test",
                "charlie@test.com",
                None,
                "dave@test.com",
                "meriem@gmail.com",
            ],
            "signup_date": [
                "2024-01-15",
                "2024-02-30",
                "2024-03-15",
                None,
                "invalid",
                "2024-04-01",
                "2022-04-01",
            ],
        }
    )
    print(messy_data)

    # Check for duplicates
    print(f"Total rows: {len(messy_data)}")
    print(f"Unique user_ids: {messy_data['user_id'].nunique()}")
    print(f"Unique email: {messy_data['email'].nunique()}")
    print(f"Duplicate user_ids: {messy_data['user_id'].duplicated().sum()}")

    # Find duplicate rows
    duplicates = messy_data[messy_data["user_id"].duplicated(keep=False)]
    print("\nDuplicate records:")
    print(duplicates)

    # Remove duplicates (keep first occurrence)
    df_clean = messy_data.drop_duplicates(subset=["user_id"], keep="first")
    print(f"After deduplication: {len(df_clean)} rows")
    print(df_clean)

    # Comprehensive null analysis
    print("Missing Value Analysis:")
    print(messy_data.isnull().sum())
    print("\nMissing Value Percentages:")
    print((messy_data.isnull().sum() / len(messy_data) * 100).round(2))

    # Visualize missing patterns
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Missing value heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(messy_data.isnull(), cbar=True, yticklabels=False)
    plt.title("Missing Value Pattern")
    plt.show()

    # Missing value combinations
    print("\nMissing value combinations:")
    print(messy_data.isnull().value_counts())

    # Task 8: Type conversion
    print("8. Type Conversion:")

    def safe_type_conversion(df: pd.DataFrame) -> pd.DataFrame:  # Added type annotation
        """Safely convert data types with error handling"""
        # Convert numeric columns
        numeric_cols = ["age", "salary"]
        for col in numeric_cols:
            # Convert to numeric, errors become NaN
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # Report conversion issues
            invalid_count = df[col].isnull().sum()
            print(f"{col}: {invalid_count} invalid values converted to NaN")

        # Convert date columns
        df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
        print(df)

        return df

    # Apply the conversion
    df_typed = safe_type_conversion(messy_data.copy())
    print(df_typed.dtypes)

    def validate_ranges(df: pd.DataFrame) -> list[str]:  # Added type annotation
        """Validate data ranges and business rules"""

        issues = []

        # Age validation
        invalid_ages = df[(df["age"] < 0) | (df["age"] > 120)]
        if not invalid_ages.empty:
            issues.append(f"Invalid ages: {len(invalid_ages)} records")
            print("Invalid age records:")
            print(invalid_ages[["user_id", "age"]])

        # Salary validation
        invalid_salaries = df[(df["salary"] < 0) | (df["salary"] > 1000000)]
        if not invalid_salaries.empty:
            issues.append(f"Suspicious salaries: {len(invalid_salaries)} records")

        # Date validation (future dates)
        future_dates = df[df["signup_date"] > pd.Timestamp.now()]
        if not future_dates.empty:
            issues.append(f"Future signup dates: {len(future_dates)} records")

        return issues

    validation_issues = validate_ranges(df_typed)
    for issue in validation_issues:
        print(f"  {issue}")

    def validate_emails(df: pd.DataFrame) -> pd.DataFrame:  # Added type annotation
        """Validate email format using regex"""

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # Check email format
        valid_emails = df["email"].str.match(email_pattern, na=False)
        invalid_emails = df[~valid_emails & df["email"].notna()]

        print(f"Valid emails: {valid_emails.sum()}")
        print(f"Invalid emails: {len(invalid_emails)}")

        if not invalid_emails.empty:
            print("\nInvalid email examples:")
            print(invalid_emails[["user_id", "email"]].head())

        # Create validation flag
        df["email_valid"] = valid_emails

        return df

    df_validated = validate_emails(df_typed.copy())
    print(df_validated)


if __name__ == "__main__":
    main()
