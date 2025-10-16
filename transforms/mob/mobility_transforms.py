from geopy.distance import geodesic
import pandas as pd

from gin.common.tool_decorator import make_tool
# from asg_runtime import make_tool

import logging
logger = logging.getLogger(__name__)

@make_tool
def filter_stations_within_distance(
    df: pd.DataFrame,
    latitude: float,
    longitude: float,
    distance: int = 0,
    distance_column: str = 'distance') -> pd.DataFrame:
    """
    For each stop in the Stops DataFrame, computes the distance (in meters) between the stop and a given geographic point (latitude and longitude). Returns a DataFrame with an additional column containing the computed distances, filtered for distances lesser than a given distance, and sorted by distance.

    Args:
        df (pd.DataFrame): DataFrame containing station records with 'stop_lat' and 'stop_lon' as strings.
        latitude (float): Latitude of the reference point.
        longitude (float): Longitude of the reference point.
        distance (int): Maximum distance in meters to filter stations; if zero, no filtering is performed.
        distance_column (str): The name of the new column with distance from the specified point.

    Returns:
        pd.DataFrame: Filtered and sorted DataFrame with stations within the specified distance and an additional column named 'distance_column' with distances from the specified point.
    """

    logger.debug(f"stops closer than {distance} meters to {latitude}:{longitude}")
    logger.debug(f"input dataframe shape: {df.shape}")

    # Convert latitude and longitude columns to float
    df['stop_lat'] = pd.to_numeric(df['stop_lat'], errors='coerce')
    df['stop_lon'] = pd.to_numeric(df['stop_lon'], errors='coerce')
    # Drop rows with invalid coordinates
    df = df.dropna(subset=['stop_lat', 'stop_lon'])
    logger.debug(f"cleaned dataframe shape: {df.shape}")

    # Compute distance for each row and store in 'distance_column' as integer
    center_coords = (latitude, longitude)
    df[distance_column] = df.apply(
        lambda row: int(round(geodesic((row['stop_lat'], row['stop_lon']), center_coords).meters)),
        axis=1
    )
    logger.debug(f"appended dataframe shape: {df.shape}")

    # Filter rows based on distance if specified
    if distance:
        df = df[df[distance_column] <= distance]
        logger.debug(f"filtered dataframe shape: {df.shape}")

    # Sort by distance
    return df.sort_values(by=distance_column)
