# teadal-connectors

# Creation of FastAPI server automatically.
 - From root dir Run generate_app_from_spec.py - this will generate a FastAPI
   application automatically named generated_fastapi_app.py.
 - run the server using the command - uvicorn fast_api_from_spec.generated_fa
stapi_app:app --reload
 - The server will run on localhost port 8000.
 - From the browser run http://localhost:8000/stops/stop_id/1031 
   or http://localhost:8000/stops/, the response will be returned as json.