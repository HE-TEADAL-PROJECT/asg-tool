from get_openapi_paths import load_openapi_spec,parse_endpoints
import os
from jinja2 import Environment, FileSystemLoader


def render_fastapi_template(output_file, endpoints, components, name_suffix):
    env = Environment(loader=FileSystemLoader('.'), extensions=['jinja2.ext.loopcontrols'])
    template = env.get_template('fast_api_from_spec/fast_api_template.jinja2')
    if 'static' in name_suffix:
        tedal_server = 'http://mobility.teadal.ubiwhere.com/'+ name_suffix
    else:
        tedal_server = 'http://industry.teadal.ubiwhere.com/' + name_suffix
    
    data = {
        "endpoints": endpoints,
        "components" : components,
        "tedal_server" : tedal_server
    }
    
    rendered_content = template.render(data)
    
    with open(output_file, 'w') as file:
        file.write(rendered_content)

def generate_app_for_spec(spec_file_name):
    openapi_spec = load_openapi_spec(spec_file_name)
    endpoints = parse_endpoints(openapi_spec)
    components = openapi_spec.get("components", {}).get("schemas", {})
    # Get the name of the endpoint from spec file name
    name_suffix = spec_file_name.split('yaml')[0].split('/')[2].split('.')[0]
    render_fastapi_template(f"fast_api_from_spec/generated_fastapi_app_{name_suffix}.py", endpoints, components, name_suffix)



if __name__ == "__main__":
    path = "./openapi-specs/"
    specs_list = os.listdir(path)
    # Generate FastApi Server for each spec in openapi-specs/ dir.
    for spec in specs_list:
        generate_app_for_spec('./openapi-specs/'+spec)