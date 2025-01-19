import os
import argparse
import sys
import yaml
import pprint
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from get_openapi_paths import load_openapi_spec, parse_endpoints


sys.path.append("./")
import handle_transform
from src.handle_transform import handle_transform_instructions


def render_fastapi_template(
    output_file, endpoints, endpoints_full_connectors_specs
):

    env = Environment(
        loader=FileSystemLoader("./src"), extensions=["jinja2.ext.loopcontrols"]
    )
    template = env.get_template("fast_api_template.jinja2")
    data = {
        "endpoints": endpoints,
        #"teadal_server": fdp_server + name_suffix,
        #"results": results,
        #"apiKey": api_key,
        "endpoints_full_connectors_specs": endpoints_full_connectors_specs,
    }

    rendered_content = template.render(data)

    with open(output_file, "w") as file:
        file.write(rendered_content)

def generate_app_for_spec(spec_file_name, instructions_file, fdp_server, api_key, config_file_path):
    openapi_spec = load_openapi_spec(spec_file_name)
    with open(instructions_file, "r") as f:
        list_of_instructions = yaml.load(f, Loader=yaml.SafeLoader)
    endpoints = parse_endpoints(openapi_spec, list_of_instructions)
    pprint.pprint(endpoints)
    # name_suffix = spec_file_name.split("yaml")[0].split("\\")[2].split(".")[0] # does not work on lnx
    # name_suffix = spec_file_name.split("yaml")[0].split(os.sep)[-1].split(".")[0] # fixed 
    name_suffix = Path(spec_file_name).stem
    print(f"name_suffix={name_suffix}") 
    results = handle_transform_instructions(list_of_instructions, config_file_path)
    path_params = {}
    query_params= {}
    endpoints_full_connectors_specs = {}
    for endpoint in endpoints:
        for param in endpoint['parameters'] :
            if param['in'] == 'path':
                path_params[param['name']] = param
            if param['in'] == 'query':
                query_params[param['name']]  = param

        con_spec = handle_transform.create_spec_section(endpoint ,fdp_server, api_key, "apiToken", path_params, query_params)
        full_spec = handle_transform.add_export_section(endpoint['sfdp_endpoint_name'], con_spec, results)
        endpoints_full_connectors_specs[endpoint['sfdp_endpoint_name']] = full_spec

    render_fastapi_template(
        f"generated_servers/generated_fastapi_app_{name_suffix}.py",
        endpoints,
        endpoints_full_connectors_specs,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate FastAPI Server for a given OpenAPI spec."
    )

    # Add -spec flag to accept a single spec file or directory
    parser.add_argument(
        "-spec",
        type=str,
        required=True,
        help="The path to the OpenAPI spec file or directory.",
    )

    parser.add_argument(
        "-i",
        type=str,
        required=True,
        help="An instructions yaml file to define each SFDP endpoint transformation.",
    )

    parser.add_argument(
        "-fdp_server", type=str, required=True, help="The FDP server URL"
    )

    parser.add_argument(
        "-k", 
        type=str, 
        default="DUMMY_KEY", 
        help="Optional API key. Defaults to 'DUMMY_KEY'."
    )

    parser.add_argument(
        "-c", 
        type=str, 
        default="./config/gin-teadal-config.yaml", 
        help="GIN configuration file."
    )

    args = parser.parse_args()

    spec_path = args.spec
    instructions_file = args.i
    fdp_server = args.fdp_server
    api_key = args.k  # Optional key, defaults to 'DUMMY_KEY'
    config_file_path = args.c
    # Check if the spec_path is a directory or a single file
    if os.path.isdir(spec_path):
        # If it's a directory, generate app for each spec in that directory
        specs_list = os.listdir(spec_path)
        for spec in specs_list:
            generate_app_for_spec(
                os.path.join(spec_path, spec), instructions_file, fdp_server, api_key, config_file_path
            )
    elif os.path.isfile(spec_path):
        # If it's a single file, generate app for that specific file
        generate_app_for_spec(spec_path, instructions_file, fdp_server, api_key, config_file_path)
    else:
        print(f"Error: {spec_path} is neither a valid directory nor a file.")
