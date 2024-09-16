from unittest import result
from acg.agents.tool_calling import apply_tool_calling 
from acg import config
from acg.agents.build_connector import (
    _get_inference_model,
    _get_missing_value_int,
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

def parse_transform_result(result):
    return result['api_calls']
    #print(result[''])

def handle_transform_instructions(list_of_instructions):
    conf = './examples/ephemeral_vectorstore_config.yaml'
    results = [] 
    for instruction in list_of_instructions:
        endpoint, instruct = instruction.split(':')
        result =_tool_call(conf, instruct)
        func_call ={}
        for call in result['api_calls']:
            func_call['endpoint'] = endpoint
            func_call['parameters'] = call.parameters
            func_call['name'] = (call.name).split('.')[1]
            results.append(func_call)
        # Add quotation marks for str typed params.
        for call in results:
        # Find the matching tool by name
            matching_tool = next((tool for tool in tool_metadata_list if tool.name == call['name']), None)
            if matching_tool:
                for param_name, param_value in call['parameters'].items():
                    matching_param = next((_param for _param in matching_tool.params if _param['name'] == param_name), None)
                    # Check if the parameter type is 'str' and update the call's parameter
                    if matching_param and matching_param['type'] == 'str':
                        call['parameters'][param_name] = f"'{param_value}'"

    return results

if __name__ == "__main__":
    list_of_instructions = ['Rename column id to identifier']
    handle_transform_instructions(list_of_instructions)
    