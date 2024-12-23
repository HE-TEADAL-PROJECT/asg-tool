from fastapi import FastAPI
from fastapi.responses import JSONResponse


from gin.executor import exec

app = FastAPI()

# Define FastAPI endpoints

@app.get("/persons_above_30")
async def persons_endpoint():
    """
    The whole 'Person' dataset will be returned. No parameters are needed.
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
         "GetPersonsAll": {
            "type": "url",
            "endpoint": "/persons",
            "method": "get",
            "arguments": []
         }
      },
      "output": {
         "execution": "",
         "runtimeType": "python",
         "data": {
            "Observation": {
               "api": "GetPersonsAll",
               "metadata": [],
               "path": "."
            }
         },
         "exports": {
            "Person": {
               "dataframe": ".",
               "fields": {
                  "person_ID": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "person_id",
                           "target": "person_ID"
                        }
                     }
                  ],
                  "person_age": [
                     {
                        "function": "persons_above_age",
                        "description": "Filters a DataFrame to return rows where the age\n      (calculated from year_of_birth, month_of_birth,day_of_birth) is bigger than the given input_age.",
                        "params": {
                           "age": 30,
                           "target": "person_age"
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
        if full_spec["spec"]["apiCalls"]["GetPersonsAll"]["arguments"][i]["argLocation"] == 'parameter':
            full_spec["spec"]["apiCalls"]["GetPersonsAll"]["arguments"][i]["value"] = path_params[param]

    for i, param in enumerate(query_params):
        if full_spec["spec"]["apiCalls"]["GetPersonsAll"]["arguments"][i]["argLocation"] == 'header':
            full_spec["spec"]["apiCalls"]["GetPersonsAll"]["arguments"][i]["value"] = query_params[param] 

    spec_string = f"""{full_spec}"""

    
    res = exec.run_from_spec_string(spec_string)
    try:
        response_data = {key: (df.dropna()).to_dict(orient='records') for key, df in res.items()}
    except:
        # In case no transformations, return json.
        return JSONResponse(res['.'])
    return JSONResponse(response_data)
