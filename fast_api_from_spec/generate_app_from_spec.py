from get_openapi_paths import load_openapi_spec,parse_endpoints
import os
from jinja2 import Environment, FileSystemLoader
import sys
sys.path.append("./")
from transform.handle_transform import handle_transform_instructions

def render_fastapi_template(output_file, endpoints, name_suffix, results):
    env = Environment(loader=FileSystemLoader('.'), extensions=['jinja2.ext.loopcontrols'])
    template = env.get_template('fast_api_from_spec/fast_api_template.jinja2')
    if 'static' in name_suffix:
        teadal_server = 'http://mobility.teadal.ubiwhere.com/'+ name_suffix
    else:
        teadal_server = 'http://industry.teadal.ubiwhere.com/' + name_suffix
    
    data = {
        "endpoints": endpoints,
        "teadal_server" : teadal_server,
        "results" : results
    }
    
    rendered_content = template.render(data)
    
    with open(output_file, 'w') as file:
        file.write(rendered_content)

def generate_app_for_spec(spec_file_name):
    openapi_spec = load_openapi_spec(spec_file_name)
    endpoints = parse_endpoints(openapi_spec)
    list_of_instructions = ['getShipments: Rename column id to identifier']
    name_suffix = spec_file_name.split('yaml')[0].split('/')[2].split('.')[0]
    #spec = create_spec(endpoints)
    results = handle_transform_instructions(list_of_instructions)
    render_fastapi_template(f"fast_api_from_spec/generated_fastapi_app_{name_suffix}.py", endpoints, name_suffix, results)



if __name__ == "__main__":
    path = "./openapi-specs/"
    specs_list = os.listdir(path)
    # Generate FastApi Server for each spec in openapi-specs/ dir.
    for spec in specs_list:
        generate_app_for_spec('./openapi-specs/'+spec)