from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response
from starlette.status import HTTP_200_OK

from asg_runtime import Executor


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        executor = await Executor.async_create()
        app.state.executor = executor
        app.state.settings = executor.get_settings()

        yield  # reached if no errors
    except Exception:
        # log and exit on startup error
        import traceback
        print(traceback.format_exc())
        raise

    # clean things up if needed
    await executor.shutdown()


app = FastAPI(lifespan=lifespan)

# --- Service Endpoints ---

@app.get("/service/settings", tags=["service"])
def get_settings(request: Request) -> dict:
    return request.app.state.settings


@app.get("/service/stats", tags=["service"])
async def get_stats(request: Request) -> dict:
    executor: Executor = request.app.state.executor
    return executor.get_stats()


@app.post("/service/origin_cache/clean", tags=["service"])
async def clear_origin_cache(request: Request) -> str:
    executor: Executor = request.app.state.executor
    result = await executor.async_clear_origin_cache()
    return result


@app.post("/service/response_cache/clean", tags=["service"])
async def clear_response_cache(request: Request) -> str:
    executor: Executor = request.app.state.executor
    result = await executor.async_clear_response_cache()
    return result


# --- Data Endpoints ---
# helper called by all data endpoints
async def get_endpoint_data(request: Request, endpoint_spec: str) -> Response:
    executor: Executor = request.app.state.executor
    try:
        result = await executor.async_get_endpoint_data(endpoint_spec)

        if result.get("status") == "ok":
            return Response(
                content=result["data"], 
                media_type="application/json",
                status_code=HTTP_200_OK)
        
        # "status" is is not "ok" - return error
        raise HTTPException(status_code=500, detail=result.get("message", "Unknown error"))

    except HTTPException:
        raise
    except Exception as e:  
        # unhandled exception - log and return error
        import traceback
        print(traceback.format_exc())
        message = f"Unhandled exception of type {type(e)} in get_endpoint_data: {e}."
        raise HTTPException(status_code=500, detail=message)
 
# --- Generated Data Endpoints ---

@app.get("/sales", tags=["data"])
async def sales_endpoint(request: Request, ):
    """
    No description
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
      "timeout": 3333,
      "apiCalls": {
         "GetSalesAll": {
            "type": "url",
            "endpoint": "/sales",
            "method": "get",
            "arguments": []
         }
      },
      "output": {
         "execution": "",
         "runtimeType": "python",
         "data": {
            "Sales": {
               "api": "GetSalesAll",
               "metadata": [],
               "path": "."
            }
         },
         "exports": {
            "Sales": {
               "dataframe": ".",
               "fields": {
                  "client_name": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "NomeCliente",
                           "target": "client_name"
                        }
                     }
                  ],
                  "category": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "Categoria",
                           "target": "category"
                        }
                     }
                  ],
                  "total_value": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "ValorTOT",
                           "target": "total_value"
                        }
                     }
                  ],
                  "currency": [
                     {
                        "function": "map_field",
                        "description": "map fields or change names from source to target.",
                        "params": {
                           "source": "Moeda",
                           "target": "currency"
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
         "url": "http://88.157.206.142/fdp-industry-czech/"
      }
   ],
   "apiKey": "DUMMY_KEY",
   "auth": "apiToken"
}
    for i, param in enumerate(path_params):
        if full_spec["spec"]["apiCalls"]["GetSalesAll"]["arguments"][i]["argLocation"] == 'parameter':
            full_spec["spec"]["apiCalls"]["GetSalesAll"]["arguments"][i]["value"] = path_params[param]

    for i, param in enumerate(query_params):
        if full_spec["spec"]["apiCalls"]["GetSalesAll"]["arguments"][i]["argLocation"] == 'header':
            full_spec["spec"]["apiCalls"]["GetSalesAll"]["arguments"][i]["value"] = query_params[param] 

    spec_string = f"""{full_spec}"""

    return await get_endpoint_data(request, spec_string)
