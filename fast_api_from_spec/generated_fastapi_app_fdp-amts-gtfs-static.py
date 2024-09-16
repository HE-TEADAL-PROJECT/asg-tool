from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
import pandas as pd
from transform import handle_transform
from acg.executor import exec
from langchain_core.documents.base import Document
from acg.types import ApiCallInf,ApiCallIssues

app = FastAPI()

# Define FastAPI endpoints

@app.get("/stops")
async def getStops():
    """
    Returns all the stops that are present in the FDP.

    """
    path_params = {
    }
    query_params = {
    }
    # Create Yaml and run executor
    con_spec = handle_transform.create_spec_section({'method': 'get', 'path': '/stops', 'name': 'getStops', 'parameters': [], 'description': 'Returns all the stops that are present in the FDP.\n', 'response_model': {'name': 'Stops', 'properties': {'type': 'array', 'items': {'$ref': '#/components/schemas/Stop'}}}}, 'http://mobility.teadal.ubiwhere.com/fdp-amts-gtfs-static', "1234", "apiToken", path_params, query_params)
    full_spec = handle_transform.add_export_section('getStops', con_spec, [{'endpoint': 'getShipments', 'context': [Document(metadata={'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.47788231183613417, 'relevance_score': 0.6990842223167419}, page_content='map fields or change names from source to target.'), Document(metadata={'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.40529203600254815, 'relevance_score': 0.6452352404594421}, page_content='concatenate Two fields.')], 'api_calls': [ApiCallInf(raw_str=' {"name": "tools.map_field", "arguments": {"df": "df", "source": "id", "target": "identifier"}}', valid=True, name='tools.map_field', parameters={'df': 'df', 'source': 'id', 'target': 'identifier'}, issues=ApiCallIssues(syntax_error=False, call_hallucinated=False, param_hallucinated=[], param_mistyped=[], param_missing=[], param_missing_info=[], param_outside_bounds=[], blank_substring=0, invalid_pair=[], repeated_arg=[], invalid_value=[]))]}])
    res = exec.run_from_spec_string(full_spec)
    return res

@app.get("/stops/stop_id/{stop_id}")
async def getStopById(stop_id: str):
    """
    Returns the data of a stop given its unique identifier.
    """
    path_params = {
        "stop_id": stop_id
    }
    query_params = {
    }
    # Create Yaml and run executor
    con_spec = handle_transform.create_spec_section({'method': 'get', 'path': '/stops/stop_id/{stop_id}', 'name': 'getStopById', 'parameters': [{'name': 'stop_id', 'in': 'path', 'type': 'string', 'nullable': False}], 'description': 'Returns the data of a stop given its unique identifier.', 'response_model': {'name': 'Stop', 'properties': {'stop_id': {'type': 'integer', 'example': 101}, 'stop_name': {'type': 'string', 'example': 'Martiri LibertĂ  SaittaMarshall'}, 'stop_lat': {'type': 'number', 'example': 37.50755595}, 'stop_lon': {'type': 'number', 'example': 15.09658165}, 'location_type': {'type': 'integer', 'example': 0}, 'parent_station': {'type': 'string', 'example': ''}, 'wheelchair_boarding': {'type': 'string', 'example': ''}}}}, 'http://mobility.teadal.ubiwhere.com/fdp-amts-gtfs-static', "1234", "apiToken", path_params, query_params)
    full_spec = handle_transform.add_export_section('getStopById', con_spec, [{'endpoint': 'getShipments', 'context': [Document(metadata={'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.47788231183613417, 'relevance_score': 0.6990842223167419}, page_content='map fields or change names from source to target.'), Document(metadata={'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.40529203600254815, 'relevance_score': 0.6452352404594421}, page_content='concatenate Two fields.')], 'api_calls': [ApiCallInf(raw_str=' {"name": "tools.map_field", "arguments": {"df": "df", "source": "id", "target": "identifier"}}', valid=True, name='tools.map_field', parameters={'df': 'df', 'source': 'id', 'target': 'identifier'}, issues=ApiCallIssues(syntax_error=False, call_hallucinated=False, param_hallucinated=[], param_mistyped=[], param_missing=[], param_missing_info=[], param_outside_bounds=[], blank_substring=0, invalid_pair=[], repeated_arg=[], invalid_value=[]))]}])
    res = exec.run_from_spec_string(full_spec)
    return res
