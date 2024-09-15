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
    df = pd.DataFrame(response_data)
    
    # Apply transformation functions
    
    df = transform_functions.map_field(df=df, 
        source='id', 
        
        target='identifier'
        )
    
    
    # Return the transformed result
    return JSONResponse(df.to_dict(orient="records"))

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
    df = pd.DataFrame(response_data)
    
    # Apply transformation functions
    
    df = transform_functions.map_field(df=df, 
        source='id', 
        
        target='identifier'
        )
    
    
    # Return the transformed result
    return JSONResponse(df.to_dict(orient="records"))
