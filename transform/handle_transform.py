import json
from acg.agents.tool_calling import apply_tool_calling 
from acg import config
from acg.retrieval import get_doc_for_call

from acg.agents.build_connector import (
    _get_inference_model,
    _get_missing_value_int,
)

from acg.con_spec import (
    ArgLocationEnum,
    ArgSourceEnum,
    CallTypeEnum,
    make_out_dataframes,
)
from acg.agents.context_retrievers import retrieve_tools_from_list
from acg.executor.transform.decorator import tool_metadata_list
import sys
sys.path.append("./transform")

import transform_functions

def _tool_call(
    config_file: str,
    query: str,
) -> dict:
    conf = config.import_config(config_file)
    inference_model = _get_inference_model("gen", conf)
    context = retrieve_tools_from_list(query, config_file, tool_metadata_list)
    state = {
        "conf": conf,
        "inference_model": inference_model,
        "user_input": query,
        "issues": "",
        "missing_value_int": _get_missing_value_int(query),
        "context": context,
        "api_calls": [],
        "feedback": "",
        "iter_count": 0,
    }
    final_state = apply_tool_calling(state)
    return final_state

def add_export_section(endpoint_name, con_spec, results):
    # assuming only one
    endpoint_transform = next((res for res in results if res['endpoint'] == endpoint_name), None)
    if endpoint_transform is None:
        return json.dumps(con_spec)
    for call in endpoint_transform['api_calls']:
        context_doc = get_doc_for_call(call.name, endpoint_transform['context'])
        doc = context_doc.metadata
        args = {}
        list_args = []
        ref_params = json.loads(doc["parameters"])
        for param, props in ref_params.items():
            if param == 'df':
                continue
            if param in call.parameters or (
                "required" in props and props["required"]
            ):
                args = {}
                args["name"] = param
                if param in call.parameters:
                    args["value"] = call.parameters[param]
                args["type"] = ref_params[param]["type"]
                list_args.append(args)
    dataframe = list(con_spec['spec']['output']['data'].keys())[0]
    #dataframe = make_out_dataframes(endpoint_transform_inf['api_calls'][-1],endpoint_transform_inf["context"])
    exports = {
    'exports': {
        'MyoutputDF': {
            'dataframe': dataframe,
            'fields': {
                'target': [
                    {
                        'function': doc['operation_id'],
                        'description': doc['description'],
                        'params': {}
                    }
                    ]
                    }
                }
            }
        }
    for param in list_args:
        exports['exports']['MyoutputDF']['fields']['target'][0]['params'][param['name']] = param['value']
    con_spec['spec']['output']['exports'] = exports['exports']
    return json.dumps(con_spec)


def create_spec_section(endpoint, base_url, apiKey, auth, path_params, query_params ):
    apicall = {
        "type": CallTypeEnum.URL,
    }
    list_args = []
    apicalls_dict = {}

    args = {}
    apicall["endpoint"] = endpoint["path"]
    apicall["method"] = endpoint["method"]
    # Find the matching tool by name
    for param in endpoint['parameters']:
        if param["name"] in path_params.keys():
            args["name"] = param["name"]
            args["source"] = ArgSourceEnum.CONSTANT
            args["value"] = path_params[param["name"]]
            args["type"] = param["type"]
            args["argLocation"] = ArgLocationEnum.PARAMETER
        #query params
        list_args.append(args)
    apicall["arguments"] = list_args

    apicalls_dict[endpoint["name"]] = apicall

    con_spec = {
        "apiVersion": "connector/v1",
        "kind": "connector/v1",
        "metadata": {
            "name": "TBD",
            "description": "TBD",
            "inputPrompt": "BLABLABALBA",
        },
        "spec": {
            "apiCalls": apicalls_dict,
            "output": {
                "execution": "",
                "runtimeType": "python",
                "data": {endpoint["response_model"]["name"] : {"api":endpoint["name"], "metadata":None, "path":"."}},#should be for all
                "exports": None,
            },
        },
        "servers": [{"url": base_url}],
        "apiKey": apiKey,
        "auth": auth,
    }
    #print(con_spec)
    #return json.dumps(con_spec)
    return con_spec


def handle_transform_instructions(list_of_instructions):
    conf = './examples/ephemeral_vectorstore_config.yaml'
    results = [] 
    for instruction in list_of_instructions:
        res = {}
        endpoint, instruct = instruction.split(':')
        result =_tool_call(conf, instruct)
        res['endpoint'] = endpoint
        res['context'] = result['context']
        res['api_calls'] = result['api_calls']
        results.append(res)        
    return results

if __name__ == "__main__":
    list_of_instructions = ['Rename column id to identifier']
    handle_transform_instructions(list_of_instructions)
    