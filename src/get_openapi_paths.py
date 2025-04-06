import yaml
from gin.gen.util import ref_resolver
import logging
from gin.common.logging import Logging
logger = logging.getLogger(Logging.BASE)

"""
Helper functions
"""


def load_openapi_spec(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


"""
Get needed endpoints data from spec to create an operational fast api application
"""


def parse_endpoints(
        openapi_spec: str, 
        instructions: str) -> list[dict]:
    
    logger.debug(f"parse_endpoints enter")
    paths = openapi_spec.get("paths", {})
    endpoints = []
    for path, methods in paths.items():
        sfdp_endpoint_name = ""
        for instruction in instructions["sfdp_endpoints"]:
            # Get the key and the content (dictionary)
            for key, content in instruction.items():
                # Check if the 'fdp_path' matches the desired value
                if "fdp_path" in content and content["fdp_path"] == path:
                    sfdp_endpoint_name = key
                if "sfdp_path" in content and content["fdp_path"] == path:
                    sfdp_endpoint_path = content["sfdp_path"]
            sfdp_endpoint_description = content.get("sfdp_endpoint_description", "No description") 
            if path == content["fdp_path"]:
                for method, details in methods.items():
                    parameters = [
                        {
                            "name": param["name"],
                            "in": param["in"],
                            "type": param["schema"]["type"],
                            "nullable": param["schema"].get("nullable", False),
                        }
                        for param in details.get("parameters", [])
                    ]
                    response_model_spec = {}
                    response_model_name = ""
                    schema = details["responses"]["200"]["content"]["application/json"][
                        "schema"
                    ]

                    if "$ref" in schema:
                        response_ref = schema["$ref"]
                    elif "items" in schema and "$ref" in schema["items"]:
                        response_ref = schema["items"]["$ref"]
                    else:
                        response_ref = None

                    if response_ref:
                        response_model_name = response_ref.split("/")[-1]
                        response_model_spec = ref_resolver.resolve_ref_for_object(
                            openapi_spec,
                            openapi_spec["components"]["schemas"][response_model_name],
                        )

                    if "properties" in response_model_spec:
                        if sfdp_endpoint_name != "":
                            endpoints.append(
                                {
                                    "method": method,
                                    "path": path,
                                    "sfdp_endpoint_name": sfdp_endpoint_name,
                                    "sfdp_endpoint_path": sfdp_endpoint_path,
                                    "name": details["operationId"],
                                    "parameters": parameters,
                                    "description": sfdp_endpoint_description,
                                    "response_model": {
                                        "name": response_model_name,
                                        "properties": response_model_spec["properties"],
                                    },
                                }
                            )
                    else:
                        if sfdp_endpoint_name != "":
                            endpoints.append(
                                {
                                    "method": method,
                                    "path": path,
                                    "sfdp_endpoint_name": sfdp_endpoint_name,
                                    "sfdp_endpoint_path": sfdp_endpoint_path,
                                    "name": details["operationId"],
                                    "parameters": parameters,
                                    "description": sfdp_endpoint_description,
                                    "response_model": {
                                        "name": response_model_name,
                                        "properties": response_model_spec,
                                    },
                                }
                            )
    return endpoints
