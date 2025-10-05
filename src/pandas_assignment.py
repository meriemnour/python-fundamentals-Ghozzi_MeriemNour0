import os
from functools import partial

import pandas as pd


def main() -> None:
    print("=== Pandas Data Display ===\n")

    users_csv = pd.read_csv(
        "C:/Users/merie/OneDrive - Constructor University/Desktop/pyhton/data/users.csv"
    )

    print("Users from CSV:")
    print(users_csv)

    # Create weather data (like in slides)
    dates = pd.date_range("2024-01-01", periods=6, freq="D")
    weather_data = {
        "date": dates,
        "temperature": [20.5, 22.1, 19.8, 21.3, 23.0, 18.5],
        "humidity": [65, 70, 68, 72, 69, 75],
        "city": ["Berlin"] * 6,
    }
    weather_df = pd.DataFrame(weather_data)

    # Create the data directory if it doesn't exist
    os.makedirs("../data", exist_ok=True)

    # Now save the CSV
    weather_df.to_csv("../data/weather_data.csv", index=False)

    print("Weather DataFrame:")
    print(weather_df)
    print()

    # Task 2: Define Pandas Series with custom index
    print("2. Creating Series with custom index...")
    sales_data = [15000, 18000, 22000, 19000]
    quarters = ["Q1_2024", "Q2_2024", "Q3_2024", "Q4_2024"]
    sales_series = pd.Series(sales_data, index=quarters, name="quarterly_sales")
    print(sales_series)
    print()

    print("3. Creating custom DataFrame...")
    product_data = {
        "product_id": ["P001", "P002", "P003", "P004"],
        "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor"],
        "category": ["Electronics", "Accessories", "Accessories", "Electronics"],
        "price": [1200.50, 25.99, 75.00, 350.00],
        "stock_quantity": [15, 100, 45, 25],
    }
    product_df = pd.DataFrame(product_data)
    print(product_df)
    print()

    # Task 4: Inspect DataFrames
    print("4. DataFrame Inspection:")
    print("Users CSV data types:")
    print(users_csv.dtypes)
    print("\nWeather data head:")
    print(weather_df.head(3))
    print("\nWeather data describe:")
    print(weather_df.describe())
    print()

    print("------------weather------------")
    print("examples from the slides ")
    # Task 5: Data slicing
    # Access column then slice rows
    temp_first_three = weather_df["temperature"][0:3]
    print(temp_first_three)
    # Or equivalently:
    # temp_first_three = weather_df[0:3]['temperature']

    # Multiple columns with row slicing
    subset = weather_df[["temperature", "humidity"]][1:4]
    print(subset)

    # Using .loc for label-based indexing
    # weather_subset = weather_df.loc["2024-01-02":"2024-01-04", "temperature"]
    # weather_df_indexed = weather_df.set_index("date")
    # weather_subset = weather_df_indexed.loc["2024-01-02":"2024-01-04", "temperature"]
    # print(weather_subset)

    # Using .iloc for position-based indexing
    position_subset = weather_df.iloc[1:4, [1, 2]]  # Rows 1-3, columns 1-2
    print(position_subset)

    # Boolean indexing with column access
    hot_days = weather_df[weather_df["temperature"] > 21]["city"]
    print(hot_days)

    print("------------user------------")
    # Task 5: Data slicing
    # Access column then slice rows
    user_first_five = users_csv["active"][0:5]
    print(user_first_five)
    # Or equivalently:
    # user_first_five = users_csv[0:3]['active']

    print("------------")
    # Multiple columns with row slicing
    subset = users_csv[["active", "age"]][1:5]
    print(subset)

    # Using .iloc for position-based indexing
    # position_subset = weather_df.iloc[1:4, [1, 2]]  # Rows 1-3, columns 1-2
    # print(position_subset)

    print("------------")
    # Boolean indexing with column access
    print("Users with age > 28:")
    age_filter = users_csv["age"] > 28
    print(users_csv[age_filter])

    # print("------------")
    # users_csv_indexed = users_csv.set_index("email")
    # user_subset = users_csv_indexed.loc["bob@example.com":"george@example.com", "age"]
    # print("Solution 1 - Using email as index:")
    # print(user_subset)

    print("Duplicate Analysis:")
    users_with_dupes = pd.concat([users_csv, users_csv.iloc[[0]]], ignore_index=True)
    print(users_with_dupes)

    # Task 7: Data cleaning - duplicates
    print("7. Data Cleaning - Duplicates:")

    # Create DataFrame with duplicates for demonstration
    users_with_dupes = pd.concat([users_csv, users_csv.iloc[[0]]], ignore_index=True)
    print("Data with duplicates:")
    print(users_with_dupes)

    print(f"\nDuplicate rows: {users_with_dupes.duplicated().sum()}")
    print(f"Unique names: {users_with_dupes['name'].nunique()}")

    users_deduplicated = users_with_dupes.drop_duplicates()
    print(f"After removing duplicates: {len(users_deduplicated)} rows")
    print()

    # Task 8: Type conversion
    print("8. Type Conversion:")

    # Create Series with mixed types for demonstration
    mixed_ages = pd.Series([25, 30, "thirty-five", 40, "unknown"])
    print("Mixed ages Series:")
    print(mixed_ages)
    print(f"Original dtype: {mixed_ages.dtype}")

    # Safe conversion
    cleaned_ages = pd.to_numeric(mixed_ages, errors="coerce")
    print("\nAfter conversion:")
    print(cleaned_ages)
    print(f"New dtype: {cleaned_ages.dtype}")
    print()

    # Task 9: Handle missing data with .apply()
    print("9. Handling Missing Data with .apply():")

    # Introduce missing values
    users_with_missing = users_csv.copy()
    users_with_missing.loc[3] = [4, "Diana Prince", None, None, True]

    def fill_missing_values(column: pd.Series) -> pd.Series:
        if column.name == "age":
            return column.fillna(column.median())
        elif column.name == "email":
            return column.fillna("unknown@example.com")
        else:
            return column

    users_filled = users_with_missing.apply(fill_missing_values)
    print("After filling missing values:")
    print(users_filled)
    print()

    # Task 10: Data cleaning pipeline with .pipe()
    print("10. Data Cleaning Pipeline with .pipe():")

    def clean_data_types(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and convert data types"""
        df_clean = df.copy()
        df_clean["age"] = pd.to_numeric(df_clean["age"], errors="coerce")
        return df_clean

    def add_validation_flags(df: pd.DataFrame) -> pd.DataFrame:
        """Add data validation flags"""
        df_valid = df.copy()
        df_valid["age_valid"] = (df_valid["age"] >= 18) & (df_valid["age"] <= 100)
        df_valid["email_valid"] = df_valid["email"].str.contains("@", na=False)
        return df_valid

        # Apply pipeline

    cleaned_users = users_csv.pipe(clean_data_types).pipe(add_validation_flags)

    print("After pipeline processing:")
    print(cleaned_users)
    print(f"Valid ages: {cleaned_users['age_valid'].sum()}/{len(cleaned_users)}")
    print(f"Valid emails: {cleaned_users['email_valid'].sum()}/{len(cleaned_users)}")
    print()

    # Task 11: Pipeline with partial arguments
    print("11. Pipeline with Partial Arguments:")

    def filter_by_age(
        df: pd.DataFrame, min_age: int, max_age: int
    ) -> pd.DataFrame:  # Added type annotation
        """Filter users by age range"""
        return df[(df["age"] >= min_age) & (df["age"] <= max_age)]

    # Create partial function for young adults
    filter_young_adults = partial(filter_by_age, min_age=18, max_age=30)

    # Apply with pipe
    young_users = users_csv.pipe(filter_young_adults)
    print("Young adults (18-30):")
    print(young_users)

    print("\n✅ All tasks completed successfully!")


if __name__ == "__main__":
    main()
