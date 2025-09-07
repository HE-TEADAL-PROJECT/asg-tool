from models import FDPSpec, ASGSpec, SFDPSpec
from .gin_helper import GinHelper
from utils.log_helper import logger


class ASGTool:
    sfdp_spec: SFDPSpec
    gin_helper: GinHelper

    def __init__(
        self,
        fdp_spec_path: str,
        fdp_url: str,
        fdp_key: str,
        fdp_timeout: int,
        asg_spec_path: str,
        gin_config_path: str,
        transforms_path: str,
    ):
        fdp_spec = FDPSpec.from_file(fdp_spec_path)
        logger.debug(f"loaded fdp_spec, endpoints: {list(fdp_spec.ep_names)}")
        asg_spec = ASGSpec.from_file(asg_spec_path)
        logger.debug(f"loaded asg_spec, endpoints: {list(asg_spec.ep_names)}")
        sfdp_spec = SFDPSpec.from_specs(
            fdp_spec=fdp_spec,
            asg_spec=asg_spec,
            fdp_url=fdp_url,
            fdp_key=fdp_key,
            fdp_timeout=fdp_timeout,
        )
        if not sfdp_spec or not sfdp_spec.num_eps:
            message = "no sfdp endpoints can be generated from the provided inputs, please check that the provided ASG spec refers to the provided FDP spec"
            logger.warning(message)
            raise Exception(message)
        logger.debug(f"resolved sfdp spec, endpoints: {list(sfdp_spec.ep_names)}")
        self.sfdp_spec = sfdp_spec
        self.gin_helper = GinHelper(
            gin_config_path,
            transforms_path,
        )

    def endpoints_to_generate(self):
        return self.sfdp_spec.num_eps

    def generate_sfdp(self) -> list[dict]:
        endpoint_dicts: list[dict] = []

        for sfdp_ep in self.sfdp_spec.sfdp_endpoints:
            ep_name = sfdp_ep.sfdp_ep_name
            ep_spec = None

            try:
                # here we'll actually use gin
                ep_spec = self.gin_helper.generate_endpoint_spec(sfdp_ep)
            except Exception as e:
                logger.debug(
                    f"failed to generate endpoint spec for:\n{sfdp_ep}\ndue to: {e}",
                    exc_info=True,
                )
                continue

            if not ep_spec:
                logger.debug(f"failed to generate endpoint spec for:\n{sfdp_ep}")
                continue

            logger.debug(
                f"generated endpoint spec for {ep_name}:\n{ep_spec}, converting to dict"
            )
            ep_spec_dict = ep_spec.model_dump(
                mode="json",
                by_alias=True,
                exclude_none=True,
                exclude_unset=True,
            )
            ep_spec_dict["apiKey"] = sfdp_ep.key
            ep_spec_dict["auth"] = "api_token"

            endpoint_dict = {
                "http_method": sfdp_ep.http_method,
                "sfdp_ep_path": sfdp_ep.target.sfdp_ep_path,
                "sfdp_ep_name": sfdp_ep.target.sfdp_ep_name,
                "sfdp_ep_descr": sfdp_ep.target.sfdp_ep_descr,
                "sfdp_ep_params": sfdp_ep.target.sfdp_ep_params,
                "fdp_ep_name": sfdp_ep.source.fdp_ep_name,
                "fdp_ep_descr": sfdp_ep.source.fdp_ep_descr,
                "fdp_ep_sum": sfdp_ep.source.fdp_ep_summary,
                # "fdp_ep_params" : sfdp_ep.fdp_ep_params,
                "fdp_ep_p_params": {name: name for name in sfdp_ep.fdp_ep_p_params},
                "fdp_ep_q_params": {name: name for name in sfdp_ep.fdp_ep_q_params},
                "spec": ep_spec_dict,
            }

            logger.debug(f"endpoint_dict:\n{endpoint_dict}")
            endpoint_dicts.append(endpoint_dict)

        return endpoint_dicts
