from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
import pandas as pd
from transform import transform_functions

app = FastAPI()

# Define FastAPI endpoints

@app.get("/stops")
async def getStops():
    """
    Returns all the stops that are present in the FDP.

    """
    path_params = {
    }
    query_params = {
    }
    response = requests.get("http://mobility.teadal.ubiwhere.com/fdp-amts-gtfs-static/stops".format(**path_params), params=query_params)
    response_data = response.json()
    # Perform your transformation here
    # Transform to DF.
    # Create DataFrame from the response data
    # Convert the response to a DataFrame (df) if the function requires it
    df = pd.DataFrame(response_data)
    # Apply transformation function to the specific endpoint
    result = transform_functions.map_field(df=df,
        source='id', 
        target='identifier'
    )
    return JSONResponse(result)
    

@app.get("/stops/stop_id/{stop_id}")
async def getStopById(stop_id: str):
    """
    Returns the data of a stop given its unique identifier.
    """
    path_params = {
        "stop_id": stop_id
    }
    query_params = {
    }
    response = requests.get("http://mobility.teadal.ubiwhere.com/fdp-amts-gtfs-static/stops/stop_id/{stop_id}".format(**path_params), params=query_params)
    response_data = response.json()
    # Perform your transformation here
    # Transform to DF.
    # Create DataFrame from the response data
    return JSONResponse(response_data)
    
