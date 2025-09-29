import functools
import time
from dataclasses import dataclass
from typing import Any, Callable, NamedTuple, TypedDict, TypeVar

import numpy as np
import pandas as pd
from pydantic import BaseModel


class UserTypedDict(TypedDict):
    id: int
    name: str
    email: str
    age: int
    active: bool


class UserNamedTuple(NamedTuple):
    id: int
    name: str
    email: str
    age: int
    active: bool


@dataclass
class UserDataClass:
    id: int
    name: str
    email: str
    age: int
    active: bool


class UserPydantic(BaseModel):
    id: int
    name: str
    email: str
    age: int
    active: bool


def create_data_structures() -> tuple[list[float], np.ndarray]:
    """Create both Python list and NumPy array with numerical data."""
    python_list = [1.5, 2.8, 3.2, 4.7, 5.1, 6.9, 7.3, 8.6, 9.4, 10.0]
    numpy_array = np.array([1.5, 2.8, 3.2, 4.7, 5.1, 6.9, 7.3, 8.6, 9.4, 10.0])
    return python_list, numpy_array


F = TypeVar("F", bound=Callable[..., Any])


def timer_decorator(func: F) -> F:
    """Decorator to measure function execution time."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.6f} seconds")
        return result

    return wrapper  # type: ignore


@timer_decorator
def multiply_python_list(scalar: float, data: list[float]) -> list[float]:
    """Multiply scalar with Python list."""
    return [scalar * x for x in data]


@timer_decorator
def multiply_numpy_array(scalar: float, data: np.ndarray) -> np.ndarray:
    """Multiply scalar with NumPy array."""
    return scalar * data


def compare_multiplication() -> None:
    """Compare execution time of scalar-vector multiplication."""
    scalar = 2.5
    python_list, numpy_array = create_data_structures()

    print("Comparing scalar-vector multiplication:")
    print(f"Scalar: {scalar}")
    print(f"Data size: {len(python_list)} elements")

    result_python = multiply_python_list(scalar, python_list)

    result_numpy = multiply_numpy_array(scalar, numpy_array)

    print(f"Python list result (first 3): {result_python[:3]}")
    print(f"NumPy array result (first 3): {result_numpy[:3]}")


def load_csv_to_dataframe() -> pd.DataFrame:
    """Load CSV file into Pandas DataFrame and print contents."""
    try:
        df = pd.read_csv("data/users.csv")
        print("\nCSV loaded into Pandas DataFrame:")
        print("=" * 50)
        print(df)
        print(f"\nDataFrame shape: {df.shape}")
        print(f"DataFrame columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return pd.DataFrame()


def demonstrate_user_structures() -> None:
    """Demonstrate all user structure types."""
    user_data: UserTypedDict = {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "age": 25,
        "active": True,
    }

    print("User structure demonstrations:")
    print("=" * 40)

    typed_dict_user: UserTypedDict = user_data
    print(f"TypedDict: {typed_dict_user}")

    namedtuple_user = UserNamedTuple(
        id=user_data["id"],
        name=user_data["name"],
        email=user_data["email"],
        age=user_data["age"],
        active=user_data["active"],
    )
    print(f"NamedTuple: {namedtuple_user}")

    dataclass_user = UserDataClass(
        id=user_data["id"],
        name=user_data["name"],
        email=user_data["email"],
        age=user_data["age"],
        active=user_data["active"],
    )
    print(f"Dataclass: {dataclass_user}")

    pydantic_user = UserPydantic(
        id=user_data["id"],
        name=user_data["name"],
        email=user_data["email"],
        age=user_data["age"],
        active=user_data["active"],
    )
    print(f"Pydantic: {pydantic_user}")


def main() -> None:
    """Main function to run all demonstrations."""
    print("Data Structures and Formats Demonstration")
    print("=" * 50)

    demonstrate_user_structures()

    print("\n" + "=" * 50)

    compare_multiplication()

    print("\n" + "=" * 50)

    load_csv_to_dataframe()


if __name__ == "__main__":
    main()
