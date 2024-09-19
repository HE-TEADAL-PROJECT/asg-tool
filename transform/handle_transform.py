import json
from acg.agents.tool_calling import apply_tool_calling
from acg import config
from acg.retrieval import get_doc_for_call
from acg.util import to_snake_case

from acg.agents.build_connector import (
    _get_inference_model,
    _get_missing_value_int,
)

from acg.con_spec import (
    ArgLocationEnum,
    ArgSourceEnum,
    CallTypeEnum,
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


def _get_doc_for_call(call_name: str, context_metadata: dict):
    for doc in context_metadata:
        doc_call = f"{to_snake_case(doc['tag'])}.{doc['operation_id']}"
        if call_name == doc_call:
            return doc


def add_export_section(endpoint_name, con_spec, results):
    print(results)
    endpoint_transforms = [res for res in results if res["endpoint"] == endpoint_name]
    if endpoint_transforms == []:
        return json.dumps(con_spec)
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
            ref_params = json.loads(doc["parameters"])
            for param, props in ref_params.items():
                if param == "df":
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

            functions_param_section = []
            func_section = {
                "function": doc["operation_id"],
                "description": doc["description"],
                "params": {},
            }
            for param in list_args:
                func_section["params"][param["name"]] = param["value"]
                # functions_param_section.append(func_section)
            functions_param_section.append(func_section)

        exports["exports"][output_df]["fields"][target_field] = functions_param_section
    con_spec["spec"]["output"]["exports"] = exports["exports"]
    return json.dumps(con_spec)


def create_spec_section(endpoint, base_url, apiKey, auth, path_params, query_params):
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
            args["value"] = path_params[param["name"]]
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
            "inputPrompt": "BLABLABALBA",
        },
        "spec": {
            "apiCalls": apicalls_dict,
            "output": {
                "execution": "",
                "runtimeType": "python",
                "data": {
                    endpoint["response_model"]["name"]: {
                        "api": endpoint["name"],
                        "metadata": None,
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


def handle_transform_instructions(list_of_instructions):
    conf = "./examples/ephemeral_vectorstore_config.yaml"
    results = []
    for endpoint_instructs in list_of_instructions["sfdp_endpoints"]:
        for endpoint, instructs in endpoint_instructs.items():
            for field_name, field_data in instructs["schema"].items():
                for param_name, param_data in field_data["properties"].items():
                    res = {}
                    result = _tool_call(
                        conf, param_data["description"] + f" to target: {param_name}"
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


if __name__ == "__main__":
    list_of_instructions = ["Rename column id to identifier"]
    handle_transform_instructions(list_of_instructions)
