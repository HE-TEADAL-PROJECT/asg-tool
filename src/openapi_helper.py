from gin.gen.util import ref_resolver
import yaml
from utils import logger


def load_openapi_spec(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return dict(yaml.safe_load(file))

def get_sfdp_endpoints(fdp_spec: dict, asg_spec: dict) -> list[dict]:
    """
    Cross-reference ASG spec with FDP spec and extract endpoint definitions.
    """
    logger.debug("enter")
    endpoints = []

    fdp_paths = fdp_spec.get("paths", {})
    schemas = fdp_spec.get("components", {}).get("schemas", {})

    for sfdp_endpoint in asg_spec["sfdp_endpoints"]:
        for sfdp_ep_name, sfdp_ep_content in sfdp_endpoint.items():
            fdp_path = sfdp_ep_content.get("fdp_path")      # returns value or None
            sfdp_path = sfdp_ep_content.get("sfdp_path")    # returns value or None
            sfdp_description = sfdp_ep_content.get("sfdp_endpoint_description", "No description")

            if not fdp_path or fdp_path not in fdp_paths:
                logger.warning(f"asg_spec references unknown FDP path {fdp_path} for {sfdp_ep_name} SFDP endpoint, will not include this endpoint")
                continue

            for method, details in fdp_paths[fdp_path].items():
                parameters = [
                    {
                        "name": p["name"],
                        "in": p["in"],
                        "type": p["schema"]["type"],
                        "nullable": p["schema"].get("nullable", False),
                    }
                    for p in details.get("parameters", [])
                ]

                # Resolve response model
                schema = details.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {}).get("schema", {})
                response_ref = schema.get("$ref") or schema.get("items", {}).get("$ref")
                response_model_name = ""
                response_model_spec: dict = {}

                if response_ref:
                    response_model_name = response_ref.split("/")[-1]
                    response_model_spec = ref_resolver.resolve_ref_for_object(
                        fdp_spec,
                        schemas.get(response_model_name, {}),
                    )

                endpoints.append(
                    {
                        "method": method,
                        "path": fdp_path,
                        "sfdp_endpoint_name": sfdp_ep_name,
                        "sfdp_endpoint_path": sfdp_path,
                        "name": details["operationId"],
                        "parameters": parameters,
                        "description": sfdp_description,
                        "response_model": {
                            "name": response_model_name,
                            "properties": response_model_spec.get("properties", response_model_spec),
                        },
                    }
                )

    logger.debug(f"returning {len(endpoints)} endpoints")
    return endpoints

# leaving the old (refactored) version in place, just for checking
#  TODO delete this method
def parse_endpoints(fdp_spec: dict, asg_spec: dict) -> list[dict]:
    """
    Get needed endpoints data from spec to create an operational fast api application
    """
    logger.debug("enter")
    fdp_paths = fdp_spec.get("paths", {})
    endpoints = []
    for path, methods in fdp_paths.items():
        sfdp_endpoint_name = ""
        for sfdp_endpoint in asg_spec["sfdp_endpoints"]:
            # Get the key and the content (dictionary)
            for key, content in sfdp_endpoint.items():
                # Check if the 'fdp_path' matches the desired value
                if "fdp_path" in content and content["fdp_path"] == path:
                    sfdp_endpoint_name = key
                if "sfdp_path" in content and content["fdp_path"] == path:
                    sfdp_endpoint_path = content["sfdp_path"]
            sfdp_endpoint_description = content.get(
                "sfdp_endpoint_description", "No description"
            )
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
                            fdp_spec,
                            fdp_spec["components"]["schemas"][response_model_name],
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
    logger.debug(f"returning {len(endpoints)} endpoints")
    return endpoints
