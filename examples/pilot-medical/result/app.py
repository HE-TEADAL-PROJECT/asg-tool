from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import traceback
from pydantic_settings import BaseSettings

from gin.executor import exec

class Settings(BaseSettings):
    debug: bool = False

settings = Settings()

app = FastAPI()

def log_level_string():
    if settings.debug:
        return "DEBUG"
    else:
        return None

@app.get("/info")
async def info():
    return {
        "debug": settings.debug,
    }

# Define FastAPI endpoints

@app.get("/persons_above_30")
async def persons_above_30():
    """
    This endpoint returns all the people of age > 30
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
      "timeout": 333,
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
            "Person": {
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
                  ],
                  "care_site_id": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "care_site_id",
                           "target": "care_site_id"
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
         "url": "http://medicine01.teadal.ubiwhere.com/fdp-medicine-node01/"
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

    try:
        res = exec.run_from_spec_string(
            spec_string, 
            log_level=log_level_string(),
            user_functions_path="./transform")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="The specified file or directory was not found.")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail="Permission denied. Ensure you have the necessary access rights.")
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Syntax error in the provided spec file: {str(e)}")
    except Exception as e:
        error_message = f"Executor failed to run the spec file: {str(e)}"
        traceback.print_exc()  # Logs the full traceback for debugging
        raise HTTPException(status_code=500, detail=error_message)
    
    try:
        response_data = {key: (df.dropna()).to_dict(orient='records') for key, df in res.items()}
    except:
        # In case no transformations, return json.
        return JSONResponse(res['.'])
    return JSONResponse(response_data)

@app.get("/persons_above_60")
async def persons_above_60():
    """
    This endpoint returns all the people of age > 60
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
      "timeout": 333,
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
            "Person": {
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
                           "age": 60,
                           "target": "person_age"
                        }
                     }
                  ],
                  "care_site_id": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "care_site_id",
                           "target": "care_site_id"
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
         "url": "http://medicine01.teadal.ubiwhere.com/fdp-medicine-node01/"
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

    try:
        res = exec.run_from_spec_string(
            spec_string, 
            log_level=log_level_string(),
            user_functions_path="./transform")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="The specified file or directory was not found.")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail="Permission denied. Ensure you have the necessary access rights.")
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Syntax error in the provided spec file: {str(e)}")
    except Exception as e:
        error_message = f"Executor failed to run the spec file: {str(e)}"
        traceback.print_exc()  # Logs the full traceback for debugging
        raise HTTPException(status_code=500, detail=error_message)
    
    try:
        response_data = {key: (df.dropna()).to_dict(orient='records') for key, df in res.items()}
    except:
        # In case no transformations, return json.
        return JSONResponse(res['.'])
    return JSONResponse(response_data)
