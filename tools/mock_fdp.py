from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Define FastAPI endpoints

@app.get("/fdp-amts-gtfs-static/stops")
async def getStops():
    """
    Returns all the stops that are present in the FDP.

    """
    res = [
        {
            "stop_id": 101,
            "stop_name": "Martiri LibertĂ  SaittaMarshall B",
            "stop_lat": 37.50755595,
            "stop_lon": 15.09658165,
            "location_type": 0,
            "parent_station": "Martiri LibertĂ  SaittaMarshall A",
            "wheelchair_boarding": "",
        },
        {
            "stop_id": 102,
            "stop_name": "Martiri LibertĂ  SaittaMarshall A",
            "stop_lat": 37.50755595,
            "stop_lon": 15.09658165,
            "location_type": 0,
            "parent_station": "",
            "wheelchair_boarding": "",
        },
    ]
    return JSONResponse(res)


@app.get("/fdp-amts-gtfs-static/stops/stop_id/{stop_id}")
async def getStopById(stop_id: str):
    """
    Returns the data of a stop given its unique identifier.
    """
    if stop_id == "101":
        res = {
            "stop_id": 101,
            "stop_name": "Martiri LibertĂ  SaittaMarshall B",
            "stop_lat": 37.50755595,
            "stop_lon": 15.09658165,
            "location_type": 0,
            "parent_station": "Martiri LibertĂ  SaittaMarshall A",
            "wheelchair_boarding": "",
        }
    else:
        raise HTTPException(status_code=404, detail="Item not found")

    return JSONResponse(res)


@app.get("/fdp-czech-plant/shipments")
async def getShipments():
    res = [
        {
            "year": 2024,
            "month": 1,
            "week": 3,
            "customer_id": 1111,
            "customer_name": "Bob",
            "item_id": "30331568937",
            "item_desc": "piece of pieces",
        },
        {
            "year": 2024,
            "month": 12,
            "week": 3,
            "customer_id": 1112,
            "customer_name": "Alice",
            "item_id": "30331568938",
            "item_desc": "piece of pieces",
        },
         {
            "year": 2023,
            "month": 12,
            "week": 3,
            "customer_id": 1113,
            "customer_name": "Alice3",
            "item_id": "30331568938",
            "item_desc": "piece of pieces",
        },
         {
            "year": 2024,
            "month": 11,
            "week": 3,
            "customer_id": 1114,
            "customer_name": "Alice4",
            "item_id": "30331568938",
            "item_desc": "piece of pieces",
        },
         {
            "year": 2024,
            "month": 10,
            "week": 3,
            "customer_id": 1115,
            "customer_name": "Alice5",
            "item_id": "30331568938",
            "item_desc": "piece of pieces",
        },
    ]
    return res
