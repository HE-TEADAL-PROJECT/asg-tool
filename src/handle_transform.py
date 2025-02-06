import json
import os
from gin.common.types import ToolDetails
from gin.gen.agents.tool_calling import apply_tool_calling
import gin.gen.config
import gin.gen.config


from gin.common.con_spec import (
    ArgLocationEnum,
    ArgSourceEnum,
    CallTypeEnum,
)
from gin.gen.agents.tool_calling import simple_tool_calling
from gin.common.tool_decorator import tool_metadata_list
from gin.executor.transform.load_functions import load_user_functions
import sys

sys.path.append("./transform")


def _tool_call(
    config_file: str,
    query: str,
    transform_folder_path: str,
) -> dict:
    """
    Make a call for GIN tool calling with the tools
    """
    load_user_functions(transform_folder_path)
    functions = [transform.model_dump() for transform in tool_metadata_list]
    return simple_tool_calling(
    config_file=config_file,
    functions=functions,
    query=query,
    ) 


def _get_doc_for_call(call_name: str, context_metadata: dict):
    for doc in context_metadata:
        tool_details_dict = json.loads(doc["tool_details_str"])
        tool_details = ToolDetails(**tool_details_dict)
        if call_name == tool_details.name:
            print(f"Context doc for call {call_name}: {doc}")
            return tool_details


def add_export_section(endpoint_name, con_spec, results):
    """Adds the export section to con_spec from the results calculated from the instuctions"""
    endpoint_transforms = [res for res in results if res["endpoint"] == endpoint_name]
    if endpoint_transforms == []:
        return json.dumps(con_spec, indent=3)
    dataframe = "."
    output_df = endpoint_transforms[0]["output_df_name"]
    exports = {"exports": {output_df: {"dataframe": dataframe, "fields": {}}}}
    for endpoint_transform in endpoint_transforms:
        target_field = endpoint_transform["target_name"]
        for call in endpoint_transform["api_calls"]:
            context_doc = _get_doc_for_call(
                call.name, endpoint_transform["context_metadata"]
            )
            doc = context_doc
            args = {}
            list_args = []
            ref_params = doc.parameters
            for param, param_detail in ref_params.items():
                if param == "df":
                    continue
                if param == 'required':
                    continue
                if param in call.parameters or (
                     param_detail.required
                ):
                    args = {}
                    args["name"] = param
                    if param in call.parameters:
                        args["value"] = call.parameters[param]
                    args["type"] = param_detail["type"]
                    list_args.append(args)

            functions_param_section = []
            func_section = {
                "function": doc.name,
                "description": doc.description,
                "params": {},
            }
            for param in list_args:
                func_section["params"][param["name"]] = param["value"]
                # functions_param_section.append(func_section)
            functions_param_section.append(func_section)

        exports["exports"][output_df]["fields"][target_field] = functions_param_section
    con_spec["spec"]["output"]["exports"] = exports["exports"]
    return json.dumps(con_spec, indent=3)


def create_spec_section(endpoint, base_url, apiKey, auth, path_params, query_params):
    """Creates the connector spec for calling the fdp API"""
    apicall = {
        "type": CallTypeEnum.URL,
    }
    list_args = []
    apicalls_dict = {}

    args = {}
    apicall["endpoint"] = endpoint["path"]
    apicall["method"] = endpoint["method"]
    # Find the matching tool by name
    for param in endpoint["parameters"]:
        if param["name"] in path_params.keys():
            args["name"] = param["name"]
            args["source"] = ArgSourceEnum.CONSTANT
            args["value"] = f'path_params[{param["name"]}]'
            args["type"] = param["type"]
            args["argLocation"] = ArgLocationEnum.PARAMETER
        # query params
        list_args.append(args)
    apicall["arguments"] = list_args

    apicalls_dict[endpoint["name"]] = apicall

    con_spec = {
        "apiVersion": "connector/v1",
        "kind": "connector/v1",
        "metadata": {
            "name": "TBD",
            "description": "TBD",
            "inputPrompt": "DUMMY PROMPT - SPEC IS CREATED STATICALLY",
        },
        "spec": {
            "apiCalls": apicalls_dict,
            "output": {
                "execution": "",
                "runtimeType": "python",
                "data": {
                    endpoint["response_model"]["name"]: {
                        "api": endpoint["name"],
                        "metadata": [],
                        "path": ".",
                    }
                },  # should be for all
                "exports": None,
            },
        },
        "servers": [{"url": base_url}],
        "apiKey": apiKey,
        "auth": auth,
    }

    return con_spec


def handle_transform_instructions(list_of_instructions, conf, transform_folder_path):
    results = []
    for endpoint_instructs in list_of_instructions["sfdp_endpoints"]:
        for endpoint, instructs in endpoint_instructs.items():
            for field_name, field_data in instructs["schema"].items():
                for param_name, param_data in field_data["properties"].items():
                    res = {}
                    result = _tool_call(
                        conf, param_data["description"] + f" to target: {param_name}" , transform_folder_path
                    )
                    res["endpoint"] = endpoint
                    res["context_metadata"] = [
                        context.metadata for context in result["context"]
                    ]
                    res["api_calls"] = result["api_calls"]
                    res["target_name"] = param_name
                    res["output_df_name"] = field_name
                    results.append(res)
    return results
