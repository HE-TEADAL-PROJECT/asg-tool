from gin.common.tool_decorator import make_tool
# from asg_runtime import make_tool

from typing import Any
import pandas as pd

@make_tool
def map_field(df: pd.DataFrame, source: str, target: str) -> pd.DataFrame:
    """
    Creates or updates a column in the DataFrame by copying values from another column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        source (str): Name of the source column whose values will be copied.
        target (str): Name of the target column to create or overwrite.

    Returns:
        pd.DataFrame: DataFrame with the target column set to the values of the source column.

    Raises:
        KeyError: If the source column does not exist in df.
    """
    if source not in df.columns:
        raise KeyError(f"Column '{source}' not found in DataFrame.")

    df[target] = df[source]
    return df

def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """
    Renames a column in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        old_name (str): Current name of the column to rename.
        new_name (str): New name for the column.

    Returns:
        pd.DataFrame: DataFrame with the column renamed.

    Raises:
        KeyError: If old_name does not exist in df.
    """
    if old_name not in df.columns:
        raise KeyError(f"Column '{old_name}' not found in DataFrame.")

    return df.rename(columns={old_name: new_name})

@make_tool
def concatenate_fields(df: pd.DataFrame, col1: str, col2: str, output: str, sep: str = "") -> pd.DataFrame:
    """
    Concatenates the string representations of two columns into a new column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        col1 (str): The first column name.
        col2 (str): The second column name.
        output (str): The name of the new column to create or overwrite.
        sep (str, optional): Separator to insert between values. Defaults to "".

    Returns:
        pd.DataFrame: DataFrame with the new output column containing concatenated values.

    Raises:
        KeyError: If either col1 or col2 does not exist in df.
    """
    if col1 not in df.columns:
        raise KeyError(f"Column '{col1}' not found in DataFrame.")
    if col2 not in df.columns:
        raise KeyError(f"Column '{col2}' not found in DataFrame.")

    df[output] = df[col1].astype(str) + sep + df[col2].astype(str)
    return df

@make_tool
def filter_by_column_value(df: pd.DataFrame, filter_column: str, filter_value: Any) -> pd.DataFrame:
    """
    Filters the input DataFrame to return only rows with values equal to the input filter_value in the column named filter_column.

    Args:
        df (pd.DataFrame)   : Input DataFrame.
        filter_column (str) : The name of the column to filter on.
        filter_value (Any)  : The filter value to match.
    
    Returns:
        pd.DataFrame: A filtered DataFrame containing only rows where the given column equals filter_value.
    
    Raises:
        KeyError: If filter_column does not exist in df.
    """
    if filter_column not in df.columns:
        raise KeyError(f"Column '{filter_column}' not found in DataFrame.")

    return df[df[filter_column] == filter_value]

# older transforms stay here for just in case

@make_tool
def filter_by_year(df, year_col, input_year):
    """
    Filters a DataFrame to return rows where the year matches the given input_year.

    Args:
        df (any): The input pandas DataFrame.
        year_col (str): The name of the column containing the year values.
        input_year (integer): The year to filter the DataFrame by.

    Returns:
        DataFrame: A filtered DataFrame with rows where the year matches input_year.
    """
    return df[df[year_col] == input_year]


@make_tool
def filter_by_quarter(df, month_col, quarter):
    """
    Filters a DataFrame to return rows where the month falls within the specified quarter.

    Args:
        df (any): The input pandas DataFrame.
        month_col (str): The name of the column containing the month values.
        quarter (integer): The quarter to filter by (1 for Q1, 2 for Q2, 3 for Q3, 4 for Q4).

    Returns:
        DataFrame: A filtered DataFrame with rows where the month falls within the given quarter.

    Raises:
        ValueError: If the quarter is not between 1 and 4.
    """
    quarters = {
        1: [1, 2, 3],  # Q1: January, February, March
        2: [4, 5, 6],  # Q2: April, May, June
        3: [7, 8, 9],  # Q3: July, August, September
        4: [10, 11, 12],  # Q4: October, November, December
    }

    if quarter not in quarters:
        raise ValueError("Quarter must be between 1 and 4.")

    return df[df[month_col].isin(quarters[quarter])]
