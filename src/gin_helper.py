import json
from pprint import pformat
from typing import cast, Any

from gin.common.types import ToolDetails
from gin.common.con_spec import (
    ArgLocationEnum,
    ArgSourceEnum,
    CallTypeEnum,
)
from gin.gen.agents.tool_calling import simple_tool_calling as gin_tool_calling
from gin.common.tool_decorator import tool_metadata_list as gin_tool_metadata

import files_helper
import openapi_helper

from utils import logger


def _get_transforms(transform_folder_path: str) -> list:
    """
    Loads functions from python modules found in the provided folder
    Loading affects GIN's gin_tool_metadata object

    Returns all functions in gin_tool_metadata after the load
    """
    loaded_functions = files_helper.load_user_functions(
        folder_path=transform_folder_path
    )
    logger.debug(f"loaded {len(loaded_functions)} transform functions")
    result = [transform.model_dump() for transform in gin_tool_metadata]
    return result


def _get_tool_for_call(call_name: str, context: list) -> ToolDetails | None:
    logger.debug(f"enter for {call_name} with {len(context)} context elements")
    result = None

    for context_element in context:
        tool_details_str = context_element.get("tool_details_str")
        tool_details_dict = json.loads(tool_details_str)
        tool_details = ToolDetails(**tool_details_dict)
        logger.debug(f"tool_details={pformat(tool_details, sort_dicts=False)}")
        if call_name == tool_details.name:
            logger.debug(f"found tool for {call_name}")
            result = tool_details
            break

    return result


def _add_ep_exports(ep_name: str, ep_con_spec: dict, tr_instructs: list[dict]):
    """Adds the export section for the specified endpoint to to the provided conectors spec. Export section is obtained from the provided transfrom instructions."""
    logger.debug(f"enter for {ep_name}")
    ep_tr_instructs = [
        tr_instruct
        for tr_instruct in tr_instructs
        if tr_instruct["endpoint"] == ep_name
    ]
    if ep_tr_instructs == []:
        logger.warning(f"there are no exports for {ep_name}")
        return json.dumps(ep_con_spec, indent=3)

    logger.debug(f"there are {len(ep_tr_instructs)} exports for {ep_name}")
    dataframe = "."
    # TODO why this is taked only from the first element?
    output_df = ep_tr_instructs[0]["output_df_name"]
    exports = {"exports": {output_df: {"dataframe": dataframe, "fields": {}}}}
    for ep_tr_instructions in ep_tr_instructs:
        output_df_name = ep_tr_instructions.get("output_df_name")
        target_name = ep_tr_instructions.get("target_name", "")
        api_calls = ep_tr_instructions.get("api_calls", [])
        logger.debug(
            f"processing {len(api_calls)} api calls for {ep_name}.{output_df_name}.{target_name}"
        )

        functions_param_section = []
        for api_call in api_calls:
            api_call_name = api_call.name
            api_call_params = api_call.parameters
            logger.debug(
                f"api_call_name={api_call_name}, api_call_params={api_call_params}"
            )
            tool_details = _get_tool_for_call(
                api_call_name, ep_tr_instructions["context_metadata"]
            )
            if not tool_details:
                logger.warning(f"there are no tools for {api_call_name}")
                break

            logger.debug(f"doc={tool_details}({type(tool_details)})")

            list_args = []
            ref_params = tool_details.parameters
            for param, param_detail in ref_params.items():
                if param == "df":
                    continue
                if param == "required":
                    continue
                if param in api_call.parameters or ("required" in param_detail):
                    args = {}
                    args["name"] = param
                    if param in api_call.parameters:
                        args["value"] = api_call.parameters[param]
                    args["type"] = param_detail["type"]
                    list_args.append(args)

            func_section = {
                "function": tool_details.name,
                "description": tool_details.description,
                "params": {},
            }
            for param in list_args:
                func_section["params"][param["name"]] = param["value"]
                # functions_param_section.append(func_section)
            functions_param_section.append(func_section)

        fields = cast(dict[str, Any], exports["exports"][output_df]["fields"])
        fields[target_name] = functions_param_section
    ep_con_spec["spec"]["output"]["exports"] = exports["exports"]
    return json.dumps(ep_con_spec, indent=3)


def _get_prop_tr_instructs(
    ep_name,
    el_name,
    prop_name,
    prop_data,
    gin_config_path: str,
    transform_functions: list,
) -> dict:
    logger.debug(f"enter for {ep_name}.{el_name}.{prop_name}")
    result: dict = {}

    # TODO - figure why we are not sending examples and return type
    gin_input = f"{prop_data.get('description')} to target: {prop_name}"
    logger.debug(f"calling gin with query={gin_input}")
    gin_result = gin_tool_calling(
        functions=transform_functions, query=gin_input, config_file=gin_config_path
    )
    if not gin_result:
        logger.warning("failed to generate tool call for property")
        return result

    gin_iter_count = gin_result.get("iter_count")
    logger.debug(f"gin has performed {gin_iter_count} iterations")

    gin_api_calls = gin_result.get("api_calls")
    logger.debug(f"gin_api_calls={gin_api_calls}")

    gin_static_api_calls = gin_result.get("static_api_calls")
    logger.debug(f"gin_static_api_calls={gin_static_api_calls}")
    gin_llm_api_calls = gin_result.get("LLM_api_calls")
    logger.debug(f"gin_llm_api_calls={gin_llm_api_calls}")

    gin_context = gin_result.get("context")
    if not gin_context or not len(gin_context):
        logger.warning(
            f"no tools context for property {prop_name} of element {el_name}"
        )
        return result

    logger.debug(f"gin has returned with {len(gin_context)} tools context elements")
    # retrieve needed data from custom gin objects
    prop_context = [cntx_el.metadata for cntx_el in gin_context]

    # TODO why we take this one and not the static_ or llm_
    prop_api_calls = list(gin_api_calls)
    result = {
        "endpoint": ep_name,
        "output_df_name": el_name,
        "target_name": prop_name,
        "context_metadata": prop_context,
        "api_calls": prop_api_calls,
    }
    return result


def _get_tr_instructs(
    asg_spec: dict, gin_config_path: str, transform_functions: list
) -> list[dict]:
    sfdp_endpoints = asg_spec["sfdp_endpoints"]
    logger.debug(f"enter for {len(sfdp_endpoints)} endpoints")
    results = []
    for sfdp_endpoint in sfdp_endpoints:
        for ep_name, ep_contents in sfdp_endpoint.items():
            logger.debug(f"endpoint name: {ep_name}")
            # logger.debug(f"endpoint contents:{pformat(ep_contents, sort_dicts=False)})")
            ep_schema = ep_contents.get("schema")
            if not ep_schema:
                logger.warning(f"endpoint {ep_name} has no schema, skipping")
                continue

            # logger.debug(f"endpoint schema" {pformat(ep_schema, sort_dicts=False)})")
            for el_name, el_data in ep_schema.items():
                logger.debug(f"element name: {el_name}")
                # logger.debug(f"element data: {pformat(el_data, sort_dicts=False)})")
                el_props = el_data.get("properties")
                if not el_props:
                    logger.warning(
                        f"element {el_name} in endpoint {ep_name} has no properties, skipping"
                    )
                    continue

                for prop_name, prop_data in el_props.items():
                    logger.debug(f"property name: {prop_name}")
                    prop_instructions = _get_prop_tr_instructs(
                        ep_name,
                        el_name,
                        prop_name,
                        prop_data,
                        gin_config_path,
                        transform_functions,
                    )
                    # logger.debug(f"prop_instructions={pformat(prop_instructions, sort_dicts=False)})")
                    results.append(prop_instructions)

    logger.debug(f"returning {len(results)} elements")
    return results


def _create_spec_section(
    endpoint, base_url, apiKey, auth, path_params, query_params, timeout
):
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
            "timeout": timeout,
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


def _get_ep_specs(
    fdp_url: str,
    fdp_key: str,
    fdp_timeout: int,
    endpoints: list[dict],
    tr_instructs: list[dict],
) -> dict:
    result = {}
    logger.debug(
        f"enter for {len(endpoints)} endpoints and {len(tr_instructs)} transforms"
    )

    for endpoint in endpoints:
        ep_name = endpoint["sfdp_endpoint_name"]
        ep_params = endpoint["parameters"]
        logger.debug(f"ep_name={ep_name}, ep_params={ep_params}")

        ep_path_params = {}
        ep_query_params = {}
        for ep_param in ep_params:
            # can have 'in', 'name', 'required', 'schema' fields
            # but usually is just empty
            param_name = ep_param["name"]
            param_in = ep_param["in"]
            logger.debug(f"param={ep_param}")
            if param_in == "path":
                ep_path_params[param_name] = ep_param
            if param_in == "query":
                ep_query_params[param_name] = ep_param

        # this does not handle exports and could be done before calling gin
        ep_spec = _create_spec_section(
            endpoint,
            fdp_url,
            fdp_key,
            "apiToken",
            ep_path_params,
            ep_query_params,
            fdp_timeout,
        )

        full_ep_spec = _add_ep_exports(ep_name, ep_spec, tr_instructs)

        result[ep_name] = full_ep_spec
    logger.debug(f"returning {len(result)} specs")

    return result


def generate_sfdp(
    fdp_spec_path: str,
    fdp_url: str,
    fdp_timeout: int,
    fdp_key: str,
    instructions_path: str,
    gin_config_path: str,
    transforms_path: str,
) -> tuple[list[dict], dict]:
    logger.debug("enter")

    fdp_spec = openapi_helper.load_openapi_spec(fdp_spec_path)
    logger.debug("loaded fdp_spec")
    asg_spec = openapi_helper.load_openapi_spec(instructions_path)
    logger.debug("loaded asg_spec")
    old_endpoints = openapi_helper.parse_endpoints(fdp_spec, asg_spec)
    endpoints = openapi_helper.get_sfdp_endpoints(fdp_spec, asg_spec)
    assert old_endpoints == endpoints, "mismatch between old and new parser versions"
    logger.debug(
        f"will generate {len(endpoints)} endpoints:\n{pformat(endpoints, sort_dicts=False)}"
    )

    transform_functions = _get_transforms(transforms_path)
    transform_instructions = _get_tr_instructs(
        asg_spec, gin_config_path, transform_functions
    )
    # logger.debug(f"transform_instructions:\n{pformat(transform_instructions, sort_dicts=False)}")

    endpoint_specs = _get_ep_specs(
        fdp_url, fdp_key, fdp_timeout, endpoints, transform_instructions
    )

    logger.debug("returning {len(endpoints)} endpoints and {len(endpoint_specs)} specs")
    return endpoints, endpoint_specs


if __name__ == "__main__":
    import utils

    utils.setup_logging()

    logger.debug(f"gin_tool_metadata={gin_tool_metadata}")
    loaded_functions = files_helper.load_user_functions(folder_path="./transforms")
    logger.debug(f"loaded_functions={loaded_functions}")
    logger.debug(f"after gin_load_functions gin_tool_metadata={gin_tool_metadata}")
    functions = [transform.model_dump() for transform in gin_tool_metadata]
    logger.debug(f"functions={functions}")
