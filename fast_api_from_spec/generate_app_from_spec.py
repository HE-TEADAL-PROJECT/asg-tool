from get_openapi_paths import load_openapi_spec, parse_endpoints
import os
import argparse

from jinja2 import Environment, FileSystemLoader
import sys
import yaml

sys.path.append("./")
from transform.handle_transform import handle_transform_instructions


def render_fastapi_template(
    output_file, endpoints, name_suffix, results, teadal_server
):
    env = Environment(
        loader=FileSystemLoader("."), extensions=["jinja2.ext.loopcontrols"]
    )
    template = env.get_template("fast_api_from_spec/fast_api_template.jinja2")
    data = {
        "endpoints": endpoints,
        "teadal_server": teadal_server + name_suffix,
        "results": results,
    }

    rendered_content = template.render(data)

    with open(output_file, "w") as file:
        file.write(rendered_content)


def generate_app_for_spec(spec_file_name, instructions_file, teadal_server):
    openapi_spec = load_openapi_spec(spec_file_name)
    with open(instructions_file, "r") as f:
        list_of_instructions = yaml.load(f, Loader=yaml.SafeLoader)
    endpoints = parse_endpoints(openapi_spec, list_of_instructions)
    name_suffix = spec_file_name.split("yaml")[0].split("\\")[2].split(".")[0]
    results = handle_transform_instructions(list_of_instructions)
    render_fastapi_template(
        f"fast_api_from_spec/generated_fastapi_app_{name_suffix}.py",
        endpoints,
        name_suffix,
        results,
        teadal_server,
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

    args = parser.parse_args()

    spec_path = args.spec
    instructions_file = args.i
    fdp_server = args.fdp_server

    # Check if the spec_path is a directory or a single file
    if os.path.isdir(spec_path):
        # If it's a directory, generate app for each spec in that directory
        specs_list = os.listdir(spec_path)
        for spec in specs_list:
            generate_app_for_spec(
                os.path.join(spec_path, spec), instructions_file, fdp_server
            )
    elif os.path.isfile(spec_path):
        # If it's a single file, generate app for that specific file
        generate_app_for_spec(spec_path, instructions_file, fdp_server)
    else:
        print(f"Error: {spec_path} is neither a valid directory nor a file.")
