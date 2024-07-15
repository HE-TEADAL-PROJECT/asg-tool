from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse

app = FastAPI()

# Define FastAPI endpoints

@app.get("/shipments")
async def getShipments():
    """
    Returns all the shipments that are present in the sFDP.

    """
    path_params = {
    }
    query_params = {
    }
    response = requests.get("http://industry.teadal.ubiwhere.com/fdp-czech-plant/shipments".format(**path_params), params=query_params)
    response_data = response.json()
    return JSONResponse(response_data)

@app.get("/shipments/customer/{id}")
async def getShipmentsByCustomer(id: str):
    """
    Returns the data of a patient given its unique identifier.
    """
    path_params = {
        "id": id
    }
    query_params = {
    }
    response = requests.get("http://industry.teadal.ubiwhere.com/fdp-czech-plant/shipments/customer/{id}".format(**path_params), params=query_params)
    response_data = response.json()
    return JSONResponse(response_data)
