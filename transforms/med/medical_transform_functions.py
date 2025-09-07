from datetime import date
import pandas as pd

from gin.common.tool_decorator import make_tool
# from asg_runtime import make_tool

import logging
logger = logging.getLogger(__name__)

@make_tool
def persons_age(df: pd.DataFrame, target: str):
    """
    Computes persons age  

    Args:
        df (any): The input pandas DataFrame.

    Returns:
        data series with persons ages the calculated from birth_datetime property
    """
    df = df.copy()
    logger.debug(f"original df shape: {df.shape}")
    # Convert string column to datetime
    birth_dt_series = pd.to_datetime(df["birth_datetime"], errors="coerce")
    today = pd.to_datetime(date.today())

    # Calculate precise age
    age_series = today.year - birth_dt_series.dt.year
    not_had_birthday = (
        (today.month < birth_dt_series.dt.month) |
        ((today.month == birth_dt_series.dt.month) & (today.day < birth_dt_series.dt.day))
    )

    df[target] = age_series - not_had_birthday.astype(int)
    logger.debug(f"result df shape={df.shape}")
    return df

@make_tool
def persons_above_age(df: pd.DataFrame, age: int, target: str):
    """
    Filters a DataFrame to return rows where the age
    (calculated from birth_datetime) is bigger than the given input_age.

    Args:
        df (any): The input pandas DataFrame.
        age (integer): The age to filter the DataFrame by.
        target (str): the new column name, the target.

    Returns:
        DataFrame: A filtered DataFrame with rows where the age is bigger than input_age.
    """
    logger.debug(f"original df shape: {df.shape}")

    df = persons_age(df, target)
    result = df[df[target] >= age]
    
    logger.debug(f"result df shape={df.shape}")
    return result

@make_tool
def persons_below_age(df: pd.DataFrame, age: int, target: str):
    """
    Filters a DataFrame to return rows where the age
    (calculated from birth_datetime) is smaller than the given input_age.

    Args:
        df (any): The input pandas DataFrame.
        age (integer): The age to filter the DataFrame by.
        target (str): the new column name, the target.

    Returns:
        DataFrame: A filtered DataFrame with rows where the age is smaller than input_age.
    """
    logger.debug(f"original df shape: {df.shape}")

    df = persons_age(df, target)
    result = df[df[target] <= age]
    
    logger.debug(f"result df shape={df.shape}")
    return result

@make_tool
def persons_between_ages(
    df: pd.DataFrame, 
    min_age: int, 
    max_age: int, 
    target: str):
    """
    Filters a DataFrame to return rows where the age
    (calculated from birth_datetime) is bigger than the given input_min_age and smaller that the given input_max_age

    Args:
        df (any): The input pandas DataFrame.
        age (integer): The age to filter the DataFrame by.
        target (str): the new column name, the target.

    Returns:
        DataFrame: A filtered DataFrame with rows where the age is between input_min_age and input_max_age.
    """
    logger.debug(f"original df shape: {df.shape}")

    df = persons_age(df, target)
    result = df[(df[target] >= min_age) & (df[target] <= max_age)]
    
    logger.debug(f"result df shape={df.shape}")
    return result