from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from get_openapi_paths import load_openapi_spec,parse_endpoints
import yaml
from jinja2 import Environment, FileSystemLoader


def render_fastapi_template(output_file, endpoints, components):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('fast_api_template.jinja2')
    data = {
        "endpoints": endpoints,
        "components" : components
    }
    
    rendered_content = template.render(data)
    
    with open(output_file, 'w') as file:
        file.write(rendered_content)



if __name__ == "__main__":
    yaml_file_path = 'fdp-amts-gtfs-static.yaml'
    #endpoints = get_openapi_paths(yaml_file_path)
    openapi_spec = load_openapi_spec(yaml_file_path)
    endpoints = parse_endpoints(openapi_spec)
    components = openapi_spec.get("components", {}).get("schemas", {})
    render_fastapi_template("generated_fastapi_app.py", endpoints, components)