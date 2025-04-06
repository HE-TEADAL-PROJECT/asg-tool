from fastapi import FastAPI
from fastapi.responses import JSONResponse


from gin.executor import exec

app = FastAPI()

# Define FastAPI endpoints

@app.get("/stop_id/{stop_id}")
async def stops_endpoint(stop_id: str):
    """
    Returns the data of a stop given its unique identifier.
    """
    path_params = {
        "stop_id": stop_id
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
         "getStopById": {
            "type": "url",
            "endpoint": "/stops/stop_id/{stop_id}",
            "method": "get",
            "arguments": [
               {
                  "name": "stop_id",
                  "source": "constant",
                  "value": "path_params[stop_id]",
                  "type": "string",
                  "argLocation": "parameter"
               }
            ]
         }
      },
      "output": {
         "execution": "",
         "runtimeType": "python",
         "data": {
            "Stop": {
               "api": "getStopById",
               "metadata": [],
               "path": "."
            }
         },
         "exports": {
            "Stop": {
               "dataframe": ".",
               "fields": {
                  "stop_ID": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "stop_id",
                           "target": "stop_ID"
                        }
                     }
                  ],
                  "stop_full_name": [
                     {
                        "function": "concatenate_fields",
                        "description": "concatenate Two fields.",
                        "params": {
                           "col1": "stop_name",
                           "col2": "parent_station",
                           "output": "stop_full_name"
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
         "url": "http://medicine01.teadal.ubiwhere.com/fdp-medicine-node01"
      }
   ],
   "apiKey": "DUMMY_KEY",
   "auth": "apiToken"
}
    for i, param in enumerate(path_params):
        if full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["argLocation"] == 'parameter':
            full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["value"] = path_params[param]

    for i, param in enumerate(query_params):
        if full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["argLocation"] == 'header':
            full_spec["spec"]["apiCalls"]["getStopById"]["arguments"][i]["value"] = query_params[param] 

    spec_string = f"""{full_spec}"""

    
    res = exec.run_from_spec_string(spec_string)
    try:
        response_data = {key: (df.dropna()).to_dict(orient='records') for key, df in res.items()}
    except:
        # In case no transformations, return json.
        return JSONResponse(res['.'])
    return JSONResponse(response_data)
