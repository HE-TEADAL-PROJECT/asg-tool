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

@app.get("/shipments")
async def getShipments():
    """
    Returns all the shipments that are present in the sFDP.

    """
    path_params = {
    }
    query_params = {
    }
    # Create Yaml and run executor
    con_spec = handle_transform.create_spec_section({'method': 'get', 'path': '/shipments', 'name': 'getShipments', 'parameters': [], 'description': 'Returns all the shipments that are present in the sFDP.\n', 'response_model': {'name': 'Shipments', 'properties': {'type': 'array', 'items': {'$ref': '#/components/schemas/Shipment'}}}}, 'http://industry.teadal.ubiwhere.com/fdp-czech-plant', "1234", "apiToken", path_params, query_params)
    full_spec = handle_transform.add_export_section('getShipments', con_spec, [{'endpoint': 'getShipments', 'context': [Document(metadata={'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.47788231183613417, 'relevance_score': 0.6990842223167419}, page_content='map fields or change names from source to target.'), Document(metadata={'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.47788231183613417, 'relevance_score': 0.6990842223167419}, page_content='map fields or change names from source to target.'), Document(metadata={'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.40529203600254815, 'relevance_score': 0.6452353000640869}, page_content='concatenate Two fields.'), Document(metadata={'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.40529203600254815, 'relevance_score': 0.6452353000640869}, page_content='concatenate Two fields.')], 'api_calls': [ApiCallInf(raw_str=' {"name": "tools.map_field", "arguments": {"df": "df", "source": "id", "target": "identifier"}}', valid=True, name='tools.map_field', parameters={'df': 'df', 'source': 'id', 'target': 'identifier'}, issues=ApiCallIssues(syntax_error=False, call_hallucinated=False, param_hallucinated=[], param_mistyped=[], param_missing=[], param_missing_info=[], param_outside_bounds=[], blank_substring=0, invalid_pair=[], repeated_arg=[], invalid_value=[]))]}])
    res = exec.run_from_spec_string(full_spec)
    return res

@app.get("/shipments/customer/{id}")
async def getShipmentsByCustomer(id: str):
    """
    Return shipment by customer id.
    """
    path_params = {
        "id": id
    }
    query_params = {
    }
    # Create Yaml and run executor
    con_spec = handle_transform.create_spec_section({'method': 'get', 'path': '/shipments/customer/{id}', 'name': 'getShipmentsByCustomer', 'parameters': [{'name': 'id', 'in': 'path', 'type': 'string', 'nullable': False}], 'description': 'Return shipment by customer id.', 'response_model': {'name': 'Shipments', 'properties': {'type': 'array', 'items': {'$ref': '#/components/schemas/Shipment'}}}}, 'http://industry.teadal.ubiwhere.com/fdp-czech-plant', "1234", "apiToken", path_params, query_params)
    full_spec = handle_transform.add_export_section('getShipmentsByCustomer', con_spec, [{'endpoint': 'getShipments', 'context': [Document(metadata={'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.47788231183613417, 'relevance_score': 0.6990842223167419}, page_content='map fields or change names from source to target.'), Document(metadata={'description': 'map fields or change names from source to target.', 'endpoint': 'map_field', 'method': 'GET', 'operation_id': 'map_field', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "source": {"type": "str", "description": "The first column name.", "required": true}, "target": {"type": "str", "description": "The second column name.", "required": true}}', 'summary': 'map_field', 'tag': 'tools', 'title': 'map_field', 'similarity_score': 0.47788231183613417, 'relevance_score': 0.6990842223167419}, page_content='map fields or change names from source to target.'), Document(metadata={'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.40529203600254815, 'relevance_score': 0.6452353000640869}, page_content='concatenate Two fields.'), Document(metadata={'description': 'concatenate Two fields.', 'endpoint': 'concatenate_fields', 'method': 'GET', 'operation_id': 'concatenate_fields', 'output_schema': '{}', 'parameters': '{"df": {"type": "any", "description": "input dataframe.", "required": true}, "col1": {"type": "str", "description": "The first column.", "required": true}, "col2": {"type": "str", "description": "The second column.", "required": true}, "output": {"type": "str", "description": "the new column name.", "required": true}}', 'summary': 'concatenate_fields', 'tag': 'tools', 'title': 'concatenate_fields', 'similarity_score': 0.40529203600254815, 'relevance_score': 0.6452353000640869}, page_content='concatenate Two fields.')], 'api_calls': [ApiCallInf(raw_str=' {"name": "tools.map_field", "arguments": {"df": "df", "source": "id", "target": "identifier"}}', valid=True, name='tools.map_field', parameters={'df': 'df', 'source': 'id', 'target': 'identifier'}, issues=ApiCallIssues(syntax_error=False, call_hallucinated=False, param_hallucinated=[], param_mistyped=[], param_missing=[], param_missing_info=[], param_outside_bounds=[], blank_substring=0, invalid_pair=[], repeated_arg=[], invalid_value=[]))]}])
    res = exec.run_from_spec_string(full_spec)
    return res
