import os
import shutil
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
     endpoints, endpoints_full_connectors_specs
):

    env = Environment(
        loader=FileSystemLoader("./src"), extensions=["jinja2.ext.loopcontrols"]
    )
    template = env.get_template("fast_api_template.jinja2")
    data = {
        "endpoints": endpoints,
        "endpoints_full_connectors_specs": endpoints_full_connectors_specs,
    }

    rendered_content = template.render(data)

    return rendered_content

def generate_app_for_spec(spec_file_name, instructions_file, fdp_server, api_key, config_file_path, transform_folder_path):
    openapi_spec = load_openapi_spec(spec_file_name)
    with open(instructions_file, "r") as f:
        list_of_instructions = yaml.load(f, Loader=yaml.SafeLoader)
    endpoints = parse_endpoints(openapi_spec, list_of_instructions)
    pprint.pprint(endpoints)
    name_suffix = Path(spec_file_name).stem.replace("-", "_")
    print(f"name_suffix={name_suffix}") 
    results = handle_transform_instructions(list_of_instructions, config_file_path, transform_folder_path)
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

    return render_fastapi_template(
        endpoints,
        endpoints_full_connectors_specs,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate FastAPI Server for a given OpenAPI spec."
    )

    # Add -spec flag to accept a single spec file or directory
    parser.add_argument(
        "-fdp_spec",
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
        "-fdp_url", type=str, required=True, help="The FDP server URL"
    )

    parser.add_argument(
        "-k", 
        type=str, 
        default="DUMMY_KEY", 
        help="Optional API key. Defaults to 'DUMMY_KEY'."
    )

    parser.add_argument(
        "-o", 
        type=str, 
        default="./generated_servers/", 
        help="Output folder location"
    )

    parser.add_argument(
        "-c", 
        type=str, 
        default="./config/gin-teadal-config.yaml", 
        help="GIN configuration file."
    )

    parser.add_argument(
        "-t", 
        type=str, 
        default="./transform/", 
        help="Transformations functions implementation folder"
    )

    args = parser.parse_args()

    spec_path = args.fdp_spec
    instructions_file = args.i
    fdp_server = args.fdp_url
    api_key = args.k  # Optional key, defaults to 'DUMMY_KEY'
    config_file_path = args.c
    transform_folder_path = args.t
    output_folder = args.o
    if os.path.isfile(spec_path):
        # If it's a single file, generate app for that specific file
        try:
            app_content = generate_app_for_spec(spec_path, instructions_file, fdp_server, api_key, config_file_path, transform_folder_path)
        # Ensure the destination folder exists
        except Exception as e:
            print(f"Error: {e}, please make sure you have the needed configurations and access rights")
            exit(1)
        os.makedirs(output_folder, exist_ok=True)

        # Move files
        app_content_output = os.path.join(output_folder, 'app.py')
        with open(app_content_output, "w") as file:
            file.write(app_content)

        destination_path = os.path.join(output_folder, 'requirements.txt')
        shutil.copy('generated_servers/requirements-sfdps.txt', destination_path)
        shutil.copy('.reqs/teadal_executor-0.1.1-py3-none-any.whl', output_folder)
        os.makedirs(output_folder+'/transform/', exist_ok=True)
        for file_name in os.listdir(transform_folder_path):
            source_path = os.path.join(transform_folder_path, file_name)
            destination_path = os.path.join(output_folder+'/transform/', file_name)
            # Move only files, not directories
            if os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)

    else:
        print(f"Error: {spec_path} is not a valid file.")