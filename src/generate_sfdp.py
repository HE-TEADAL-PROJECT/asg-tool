import os
from dotenv import load_dotenv
import argparse
import sys
from pprint import pformat
from jinja2 import Environment, FileSystemLoader
import files_helper
import gin_helper
from utils import setup_logging, logger

ASG_TOOL_IMPORT = "from gin.common.tool_decorator import make_tool"
ASG_RUNTIME_IMPORT = "from asg_runtime import make_tool"
SFDP_TEMPLATE_DIR = os.getenv("SFDP_TEMPLATE_DIR", f".{os.sep}sfdp-template")
SFDP_TRANSFORMS_DIR = "transforms"
SFDP_TEMPLATE_JINJA = os.getenv("SFDP_TEMPLATE_FILE", "sfdp_template.jinja2")
SFDP_TEMPLATE_FILES = [
    ".dockerignore",
    ".env",
    ".gitattributes",
    ".gitignore",
    ".gitlab-ci.yml",
    "Dockerfile",
    "Dockerfile_from_src",
    "Dockerfile_from_img",
    "pyproject.toml",
    "README.md",
    "requirements-base.txt",
    "requirements-dev.txt",
    "requirements-local.txt",
]


def _write_output(contents) -> str:
    from_dir = SFDP_TEMPLATE_DIR
    from_transforms_dir = args.transforms
    to_dir = args.output
    to_transforms_dir = os.path.join(to_dir, SFDP_TRANSFORMS_DIR)
    os.makedirs(to_dir, exist_ok=True)
    os.makedirs(to_transforms_dir, exist_ok=True)

    app_file, index = files_helper.get_next_filename(
        folder=to_dir, base_name="app", ext=".py"
    )

    logger.debug(f"copying template files from {from_dir} to {to_dir}")
    for fname in SFDP_TEMPLATE_FILES:
        fpath = os.path.join(SFDP_TEMPLATE_DIR, fname)
        files_helper.copy_file_if_newer(fpath, to_dir)

    logger.debug(
        f"copying transform files from {from_transforms_dir} to {to_transforms_dir}"
    )
    files_helper.copy_replacing_line(
        from_dir=from_transforms_dir,
        to_dir=to_transforms_dir,
        ext=".py",
        line_to_replace=ASG_TOOL_IMPORT,
        replacement_line=ASG_RUNTIME_IMPORT,
    )

    with open(app_file, "w", encoding="utf-8", newline="\n") as f:
        logger.debug(f"writing contents to {app_file}")
        f.write(contents)

    return app_file


def _is_valid_file(path: str) -> str:
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File not found: {path}")
    return path


def _is_valid_folder(path: str) -> str:
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Folder not found: {path}")
    return path


def _get_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A CLI tool for generating SFDP applications.",
        epilog="""Example usage:
            python src/generate_sfdp.py 
            -fdp_spec examples/openapi-specs/medical-spec.yaml 
            -fdp_url http://medicine01.teadal.ubiwhere.com/fdp-medicine-node01/ 
            -i examples/asg-instructions/Medical-instructions.yaml 
            -o 2025-07-2-med-sfdp""",
    )

    parser.add_argument(
        "-fdp_spec",
        type=_is_valid_file,
        required=True,
        help="Path to the FDP OpenAPI spec.",
    )
    parser.add_argument("-fdp_url", type=str, required=True, help="The FDP server URL.")
    parser.add_argument(
        "-fdp_timeout", type=int, default=300, help="Timeout for FDP requests."
    )
    parser.add_argument(
        "-i",
        "--instructions",
        type=_is_valid_file,
        required=True,
        help="Transformation instruction YAML.",
    )
    parser.add_argument(
        "-k",
        "--api-key",
        type=str,
        default="DUMMY_KEY",
        help="API key for FDP (optional).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="./generated_servers/",
        help="Output folder.",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=_is_valid_file,
        default="./config/gin-teadal-config.yaml",
        help="GIN config file.",
    )
    parser.add_argument(
        "-t",
        "--transforms",
        type=_is_valid_folder,
        default="./transforms/",
        help="Folder with transformation scripts.",
    )

    return parser


def _render_sfdp_template(
    template_folder_path: str,
    template_file_name: str,
    endpoints: list[dict],
    endpoint_specs: dict,
) -> str:

    env = Environment(
        loader=FileSystemLoader(template_folder_path),
        extensions=["jinja2.ext.loopcontrols"],
    )
    template = env.get_template(template_file_name)
    data = {
        "endpoints": endpoints,
        "endpoint_specs": endpoint_specs,
    }

    rendered_content = template.render(data)

    return rendered_content


def main(args):
    logger.info("Starting SFDP generation")

    try:
        endpoints, endpoint_specs = gin_helper.generate_sfdp(
            fdp_spec_path=args.fdp_spec,
            fdp_url=args.fdp_url,
            fdp_timeout=args.fdp_timeout,
            fdp_key=args.api_key,
            instructions_path=args.instructions,
            gin_config_path=args.config,
            transforms_path=args.transforms,
        )
    except Exception as e:
        logger.error(f"SFDP generation failed: {e}", exc_info=True)
        sys.exit(1)

    logger.info("SFDP generation suceeded, rendering the template")
    rendered = _render_sfdp_template(
        SFDP_TEMPLATE_DIR, SFDP_TEMPLATE_JINJA, endpoints, endpoint_specs
    )

    logger.info("SFDP template rendered, writing output")
    app_file = _write_output(rendered)

    logger.info(f"SFDP app generation complete, the code is in {app_file}")


if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    logger.debug("creating args parser")
    parser = _get_args_parser()
    logger.debug("parsing the args")
    args = parser.parse_args()
    logger.debug(f"ready to go args={pformat(object=args, indent=2)}")
    main(args)
