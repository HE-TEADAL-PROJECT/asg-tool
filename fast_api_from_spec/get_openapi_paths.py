import sys
import yaml

'''
Helper functions
'''
def load_openapi_spec(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


'''
Get needed endpoints data from spec to create an operational fast api application
'''
def parse_endpoints(openapi_spec):
    paths = openapi_spec.get("paths", {})
    endpoints = []
    for path, methods in paths.items():
        for method, details in methods.items():
            parameters = [
                {"name": param["name"], "in": param["in"], "type": param["schema"]["type"], "nullable": param["schema"].get("nullable", False)}
                for param in details.get("parameters", [])
            ]
            response_ref = details["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
            response_model_name = response_ref.split('/')[-1]
            response_model_spec = openapi_spec["components"]["schemas"][response_model_name]
            if "properties" in response_model_spec:
                endpoints.append({
                    "method": method,
                    "path": path,
                    "name": details["operationId"],
                    "parameters": parameters,
                    "description": details.get("description", ""),
                    "response_model": {
                        "name": response_model_name,
                        "properties": response_model_spec["properties"]
                    }
                })
            else:
                    endpoints.append({
                    "method": method,
                    "path": path,
                    "name": details["operationId"],
                    "parameters": parameters,
                    "description": details.get("description", ""),
                    "response_model": {
                        "name": response_model_name,
                        "properties": response_model_spec
                    }
                })
    return endpoints