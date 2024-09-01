# teadal-connectors

# Creation of FastAPI servers automatically.
 - From root dir Run generate_app_from_spec.py - this will generate a FastAPI
   application automatically for each spec file in openapi-specs directory.
 - Run the server using the command - uvicorn fast_api_from_spec.{{generated_fastapi_app}}:app --reload
   .where {{generated_fastapi_app}} is one of the generated FastAPI generated apps.
 - The server will run on localhost port 8000.
 - From the browser run those examples:
     for stops: http://localhost:8000/stops/, http://localhost:8000/stops/stop_id/1031
     for shipments: http://localhost:8000/shipments, http://localhost:8000/shipments/customer/501220267
     the response will be returned as json.