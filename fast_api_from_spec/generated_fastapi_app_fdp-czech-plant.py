from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
import pandas as pd
from transform import transform_functions

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
    # Perform your transformation here
    # Transform to DF.
    # Create DataFrame from the response data
    return JSONResponse(response_data)
    df = pd.DataFrame(response_data)
    
    # Apply transformation functions
    
    df = transform_functions.map_field(df=df, 
        source='id', 
        
        target='identifier'
        )
    
    
    # Return the transformed result
    return JSONResponse(df.to_dict(orient="records"))

@app.get("/shipments/customer/{id}")
async def getShipmentsByCustomer(id: str):
    """
    Return shipment by customer id.
    """
    path_params = {
        "id": id
    }
    query_params = {
    }
    response = requests.get("http://industry.teadal.ubiwhere.com/fdp-czech-plant/shipments/customer/{id}".format(**path_params), params=query_params)
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
