from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Any
import requests

app = FastAPI()

# Define Pydantic models for the components


class Stop(BaseModel):
        stop_id: int
        stop_name: str
        stop_lat: float
        stop_lon: float
        location_type: int
        parent_station: str
        wheelchair_boarding: str

class Stops(BaseModel):
        items: List[Stop]


# Define FastAPI endpoints

@app.get("/stops", response_model=Stops)
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
    return Stops(
        type=response_data["type"],
        items=response_data["items"])
    


@app.get("/stops/stop_id/{stop_id}", response_model=Stop)
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
    return Stop(
        stop_id=response_data["stop_id"],
        stop_name=response_data["stop_name"],
        stop_lat=response_data["stop_lat"],
        stop_lon=response_data["stop_lon"],
        location_type=response_data["location_type"],
        parent_station=response_data["parent_station"],
        wheelchair_boarding=response_data["wheelchair_boarding"])
    

