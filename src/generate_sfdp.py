import os
from dotenv import load_dotenv
import shutil
import argparse
import sys
import logging
from gin.common.logging import Logging
logger = logging.getLogger(Logging.BASE)

from jinja2 import Environment, FileSystemLoader

import get_openapi_paths
import handle_transform

def generate_sfdp(
        fdp_spec_path: str, 
        fdp_url: str, 
        fdp_key: str, 
        instructions_path: str, 
        gin_config_path: str, 
        transforms_path: str) -> tuple[list[dict], dict]:
    
    fdp_spec = get_openapi_paths.load_openapi_spec(fdp_spec_path)
    instructions = get_openapi_paths.load_openapi_spec(instructions_path)

    endpoints = get_openapi_paths.parse_endpoints(fdp_spec, instructions)
    logger.debug(f"Parsed {len(endpoints)} endpoints")

    results = handle_transform.handle_transform_instructions(instructions, gin_config_path, transforms_path)
    logger.debug(f"After transform, there are {len(results)} results")

    path_params = {}
    query_params= {}
    endpoints_full_connectors_specs = {}
    for endpoint in endpoints:
        for param in endpoint['parameters'] :
            if param['in'] == 'path':
                path_params[param['name']] = param
            if param['in'] == 'query':
                query_params[param['name']]  = param

        con_spec = handle_transform.create_spec_section(endpoint ,fdp_url, fdp_key, "apiToken", path_params, query_params)
        full_spec = handle_transform.add_export_section(endpoint['sfdp_endpoint_name'], con_spec, results)
        endpoints_full_connectors_specs[endpoint['sfdp_endpoint_name']] = full_spec

    return endpoints, endpoints_full_connectors_specs

def _get_next_filename(
        output_folder: str, 
        base_name: str ="app", 
        extension: str =".py") -> str:
    
    index = 0
    while True:
        filename = f"{base_name}{index if index > 0 else ''}{extension}"
        file_path = os.path.join(output_folder, filename)
        if not os.path.exists(file_path):  # Check if file exists
            return file_path, index
        index += 1
    
def _get_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate SFDP for a given FDP and instructions."
    )

    parser.add_argument(
        "-fdp_spec",
        type=str,
        required=True,
        help="The path to the OpenAPI spec file or directory.",
    )

    parser.add_argument(
        "-fdp_url", 
        type=str, 
        required=True, 
        help="The FDP server URL"
    )

    parser.add_argument(
        "-i",
        type=str,
        required=True,
        help="An instructions yaml file to define each SFDP endpoint transformation.",
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

    return parser

def _args_check_file(
        filename: str, 
        argname: str) -> str:
    if not os.path.isfile(filename):
        logger.error(f"Bad parameter {argname}: {filename} is not a file.")
        sys.exit(1)
    return filename

def _render_sfdp_template(
        template_folder_path: str,
        template_file_name: str,
        endpoints: list[dict], 
        endpoints_full_connectors_specs: dict) -> str:

    env = Environment(
        loader=FileSystemLoader(template_folder_path), extensions=["jinja2.ext.loopcontrols"]
    )
    template = env.get_template(template_file_name)
    data = {
        "endpoints": endpoints,
        "endpoints_full_connectors_specs": endpoints_full_connectors_specs,
    }

    rendered_content = template.render(data)

    return rendered_content

def _args_check_folder(
        foldername: str, 
        argname: str) -> str:
    if not os.path.isdir(foldername):
        logger.error(f"Bad parameter {argname}: {foldername} is not a folder.")
        sys.exit(1)
    return foldername

if __name__ == "__main__":
    load_dotenv()
    DEBUG = os.getenv('DEBUG', None)
    if DEBUG:
        Logging(log_level="DEBUG")
    SFDP_TEMPLATE_DIR = os.getenv('SFDP_TEMPLATE_DIR', f".{os.sep}sfdp-template")
    SFDP_TEMPLATE_FILE = os.getenv('SFDP_TEMPLATE_FILE', "sfdp_template.jinja2")

    logger.debug("Starting")
    parser = _get_args_parser()
    args = parser.parse_args()

    fdp_spec_path = _args_check_file(filename = args.fdp_spec, argname = "fdp_spec_path")
    instructions_path = _args_check_file(filename = args.i, argname = "instructions_path")
    gin_config_path = _args_check_file(filename = args.c, argname = "gin_config_path")
    transforms_path = _args_check_folder(foldername = args.t, argname = "transforms_path")
    fdp_url = args.fdp_url
    fdp_key = args.k  
    output_path = args.o

    try:
        endpoints, specs = generate_sfdp(
            fdp_spec_path = fdp_spec_path, 
            fdp_url = fdp_url, 
            fdp_key = fdp_key, 
            instructions_path = instructions_path, 
            gin_config_path = gin_config_path, 
            transforms_path = transforms_path)
        logger.debug(f"SFDP generation suceeded")
    except Exception as e:
        logger.error(f"Error generating the SFDP: {e}")
        exit(1)

    logger.debug(f"Rendering the template {SFDP_TEMPLATE_FILE} in {SFDP_TEMPLATE_DIR}")
    rendered_sfdp = _render_sfdp_template(SFDP_TEMPLATE_DIR, SFDP_TEMPLATE_FILE, endpoints, specs)
    
    logger.debug(f"All good, rendered_sfdp = {rendered_sfdp}, creating output project")
    os.makedirs(output_path, exist_ok=True)
    sfdp_path, index = _get_next_filename(output_path)
    with open(sfdp_path, "w") as file:
        logger.debug(f"Writing SFDP to file: \n{sfdp_path}")
        file.write(rendered_sfdp)

    sfdp_transform_path = f"{output_path}{os.sep}transform{os.sep}"
    if index == 0 :
        logger.debug(f"Copying dependencies to the SFDP project")
        shutil.copy(f"{SFDP_TEMPLATE_DIR}{os.sep}requirements.txt", output_path)
        shutil.copy(f'{SFDP_TEMPLATE_DIR}{os.sep}teadal_executor-0.1.1-py3-none-any.whl', output_path)
        os.makedirs(sfdp_transform_path, exist_ok=True)

    logger.debug(f"Copying .py files from {transforms_path} to  {sfdp_transform_path}")
    for transforms_path_entry in os.listdir(transforms_path):
        transform_source_path = os.path.join(transforms_path, transforms_path_entry)
        if os.path.isfile(transform_source_path):
            shutil.copy(transform_source_path, sfdp_transform_path)
