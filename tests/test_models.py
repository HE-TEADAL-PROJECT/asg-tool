from  models import FDPSpec, ASGSpec, SFDPSpec
from utils.files_helper import iter_files_from_dir
import pytest
import logging
import os
logger = logging.getLogger("test_models")

FDP_SPECS_DIR = "examples/openapi-specs"
ASG_SPECS_DIR = "tests/data/asg-instructions"


def test_fdp_spec():
    for spec_file in iter_files_from_dir(FDP_SPECS_DIR, "yaml"):
        fdp_spec = FDPSpec.from_file(spec_file)
        logger.debug(f"loaded {spec_file}: {list(fdp_spec.ep_names)}")
        # logger.debug(f"{fdp_spec}")

def test_asg_spec():
    for spec_file in iter_files_from_dir(ASG_SPECS_DIR, "yaml"):
        asg_spec = ASGSpec.from_file(spec_file)
        logger.debug(f"loaded {spec_file}: {list(asg_spec.ep_names)}")
        logger.debug(f"{asg_spec}")

SPEC_PAIRS = [
    # ("fdp-ind-czech-plant.yaml", "asg-ind-sales.yaml"),
    # ("fdp-ind-czech-plant.yaml", "asg-ind-shipments.yaml"),
    # ("fdp-mob-amts-gtfs-static.yaml", "asg-mob-stops.yaml"),
    # ("fdp-med-node01.yaml", "asg-med-persons.yaml"),
    ("fdp-med-node01.yaml", "asg_med_persons.yaml"),
    # ...
]
@pytest.mark.parametrize("fdp_file, asg_file", SPEC_PAIRS)
def test_sfdp_spec(fdp_file, asg_file):
    fdp_spec = FDPSpec.from_file(f"{FDP_SPECS_DIR}{os.sep}{fdp_file}")
    logger.debug(f"loaded {fdp_file}: {list(fdp_spec.ep_names)}")

    asg_spec = ASGSpec.from_file(f"{ASG_SPECS_DIR}{os.sep}{asg_file}")
    logger.debug(f"loaded {asg_file}: {list(asg_spec.ep_names)}")

    sfdp_spec: SFDPSpec  = SFDPSpec.from_specs(
        fdp_spec=fdp_spec,
        asg_spec=asg_spec,
        fdp_url="dummy_url",
        fdp_key="dummy_key",
        fdp_timeout=10,
    )

    logger.debug(f"\n\nloaded sfdp_spec: {list(sfdp_spec.ep_names)}")
    # for sfdp_ep in sfdp_spec.sfdp_endpoints:
    #     logger.debug(f"source: {sfdp_ep.source}")
    #     logger.debug(f"target: {sfdp_ep.target}")
    #     logger.debug(f"connection: {sfdp_ep.connection}")


