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

@app.get("/stop_id/{stop_id}")
async def sfdp_endpoint(stop_id: str):
    """
    Returns the data of a stop given its unique identifier.
    """
    path_params = {
        "stop_id": stop_id
    }
    query_params = {
    }
    # Create Yaml and run executor
    endpoint_data = {'method': 'get', 'path': '/stops/stop_id/{stop_id}', 'sfdp_endpoint_name': 'sfdp_endpoint', 'sfdp_endpoint_path': '/stop_id/{stop_id}', 'name': 'getStopById', 'parameters': [{'name': 'stop_id', 'in': 'path', 'type': 'string', 'nullable': False}], 'description': 'Returns the data of a stop given its unique identifier.', 'response_model': {'name': 'Stop', 'properties': {'stop_id': {'type': 'integer', 'example': 101}, 'stop_name': {'type': 'string', 'example': 'Martiri LibertĂ  SaittaMarshall'}, 'stop_lat': {'type': 'number', 'example': 37.50755595}, 'stop_lon': {'type': 'number', 'example': 15.09658165}, 'location_type': {'type': 'integer', 'example': 0}, 'parent_station': {'type': 'string', 'example': ''}, 'wheelchair_boarding': {'type': 'string', 'example': ''}}}}
    con_spec = handle_transform.create_spec_section(endpoint_data, 'http://localhost:8003/fdp-amts-gtfs-static', "1234", "apiToken", path_params, query_params)

    transformations_instructions = [{'endpoint': 'sfdp_endpoint', 'context_metadata': [{'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.5280805992586097, 'relevance_score': 0.7011014819145203}, {'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name, the target.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.3201200829514901, 'relevance_score': 0.544719398021698}], 'api_calls': [ApiCallInf(raw_str=' {"name": "tools.map_field", "arguments": {"df": "df", "source": "stop_id", "target": "stop_ID"}}', valid=True, name='tools.map_field', parameters={'df': 'df', 'source': 'stop_id', 'target': 'stop_ID'}, issues=ApiCallIssues(syntax_error=False, call_hallucinated=False, param_hallucinated=[], param_mistyped=[], param_missing=[], param_missing_info=[], param_outside_bounds=[], blank_substring=0, invalid_pair=[], repeated_arg=[], invalid_value=[]))], 'target_name': 'stop_ID', 'output_df_name': 'Stop'}, {'endpoint': 'sfdp_endpoint', 'context_metadata': [{'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.459023325148298, 'relevance_score': 0.6386981010437012}, {'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.459023325148298, 'relevance_score': 0.6386981010437012}, {'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name, the target.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.42767470996013757, 'relevance_score': 0.595315158367157}, {'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name, the target.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.42767470996013757, 'relevance_score': 0.595315158367157}], 'api_calls': [ApiCallInf(raw_str=' {"name": "tools.concatenate_fields", "arguments": {"df": "input_dataframe", "col1": "stop_name", "col2": "parent_station", "output": "stop_full_name"}}', valid=True, name='tools.concatenate_fields', parameters={'df': 'input_dataframe', 'col1': 'stop_name', 'col2': 'parent_station', 'output': 'stop_full_name'}, issues=ApiCallIssues(syntax_error=False, call_hallucinated=False, param_hallucinated=[], param_mistyped=[], param_missing=[], param_missing_info=[], param_outside_bounds=[], blank_substring=0, invalid_pair=[], repeated_arg=[], invalid_value=[]))], 'target_name': 'stop_full_name', 'output_df_name': 'Stop'}]
    full_spec = handle_transform.add_export_section('sfdp_endpoint', con_spec, transformations_instructions)
    res = exec.run_from_spec_string(full_spec)
    try:
        response_data = {key: df.to_dict(orient='records') for key, df in res.items()}
    except:
        # In case no transformations, return json.
        return JSONResponse(res['.'])
    return JSONResponse(response_data)
