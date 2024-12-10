from fastapi import FastAPI
from fastapi.responses import JSONResponse


from gin.gen.executor import exec

app = FastAPI()

# Define FastAPI endpoints

@app.get("/year-quarter")
async def shipments_endpoint():
    """
    Returns all the shipments that are present in the sFDP.

    """
    path_params = {
    }
    query_params = {
    }
    # Create Yaml and run executor
    full_spec = {
   "apiVersion": "connector/v1",
   "kind": "connector/v1",
   "metadata": {
      "name": "TBD",
      "description": "TBD",
      "inputPrompt": "DUMMY PROMPT - SPEC IS CREATED STATICALLY"
   },
   "spec": {
      "apiCalls": {
         "getShipments": {
            "type": "url",
            "endpoint": "/shipments",
            "method": "get",
            "arguments": []
         }
      },
      "output": {
         "execution": "",
         "runtimeType": "python",
         "data": {
            "Shipments": {
               "api": "getShipments",
               "metadata": [],
               "path": "."
            }
         },
         "exports": {
            "Shipment": {
               "dataframe": ".",
               "fields": {
                  "year": [
                     {
                        "function": "filter_by_year",
                        "description": "Filters a DataFrame to return rows where the year matches the given input_year.",
                        "params": {
                           "year_col": "year",
                           "input_year": 2024
                        }
                     }
                  ],
                  "month": [
                     {
                        "function": "filter_by_quarter",
                        "description": "Filters a DataFrame to return rows where the month falls within the specified quarter.",
                        "params": {
                           "month_col": "month",
                           "quarter": 4
                        }
                     }
                  ]
               }
            }
         }
      }
   },
   "servers": [
      {
         "url": "http://localhost:8003/"
      }
   ],
   "apiKey": "DUMMY_KEY",
   "auth": "apiToken"
}
    for i, param in enumerate(path_params):
        if full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["argLocation"] == 'parameter':
            full_spec["spec"]["apiCalls"]["getShipments"]["arguments"][i]["value"] = path_params[param]

    for i, param in enumerate(query_params):
        if full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["argLocation"] == 'header':
            full_spec["spec"]["apiCalls"]["getShipments"]["arguments"][i]["value"] = query_params[param] 

    spec_string = f"""{full_spec}"""

    
    res = exec.run_from_spec_string(spec_string)
    try:
        response_data = {key: (df.dropna()).to_dict(orient='records') for key, df in res.items()}
    except:
        # In case no transformations, return json.
        return JSONResponse(res['.'])
    return JSONResponse(response_data)

@app.get("/name-id")
async def another_shipments_endpoint():
    """
    Returns all the shipments that are present in the sFDP.

    """
    path_params = {
    }
    query_params = {
    }
    # Create Yaml and run executor
    full_spec = {
   "apiVersion": "connector/v1",
   "kind": "connector/v1",
   "metadata": {
      "name": "TBD",
      "description": "TBD",
      "inputPrompt": "DUMMY PROMPT - SPEC IS CREATED STATICALLY"
   },
   "spec": {
      "apiCalls": {
         "getShipments": {
            "type": "url",
            "endpoint": "/shipments",
            "method": "get",
            "arguments": []
         }
      },
      "output": {
         "execution": "",
         "runtimeType": "python",
         "data": {
            "Shipments": {
               "api": "getShipments",
               "metadata": [],
               "path": "."
            }
         },
         "exports": {
            "Customer": {
               "dataframe": ".",
               "fields": {
                  "customer_name_id": [
                     {
                        "function": "concatenate_fields",
                        "description": "concatenate Two fields.",
                        "params": {
                           "col1": "customer_name",
                           "col2": "customer_id",
                           "output": "customer_name_id"
                        }
                     }
                  ],
                  "client_name": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "customer_name",
                           "target": "client_name"
                        }
                     }
                  ]
               }
            }
         }
      }
   },
   "servers": [
      {
         "url": "http://localhost:8003/"
      }
   ],
   "apiKey": "DUMMY_KEY",
   "auth": "apiToken"
}
    for i, param in enumerate(path_params):
        if full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["argLocation"] == 'parameter':
            full_spec["spec"]["apiCalls"]["getShipments"]["arguments"][i]["value"] = path_params[param]

    for i, param in enumerate(query_params):
        if full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["argLocation"] == 'header':
            full_spec["spec"]["apiCalls"]["getShipments"]["arguments"][i]["value"] = query_params[param] 

    spec_string = f"""{full_spec}"""

    
    res = exec.run_from_spec_string(spec_string)
    try:
        response_data = {key: (df.dropna()).to_dict(orient='records') for key, df in res.items()}
    except:
        # In case no transformations, return json.
        return JSONResponse(res['.'])
    return JSONResponse(response_data)
