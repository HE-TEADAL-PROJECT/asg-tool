from __future__ import annotations  # to allow using the defined models as types
from utils.log_helper import logger
from .base import MyBaseModel, Schema, ResolvedSchema
from .openapi_spec import (
    OpenApiParameter,
    OpenApiOperation,
)
from .asg_spec import ASGSpec, ASGEndpointContent, ASGResponseSchema, ASGResponseParam
from .fdp_spec import FDPSpec

# ------------------------------
# INTERNAL RESOLVED SFDP SPEC
# ------------------------------


class SFDPSourceDetails(MyBaseModel):
    fdp_ep_name: str
    fdp_ep_path: str
    fdp_ep_descr: str
    fdp_ep_summary: str
    fdp_ep_params: list[OpenApiParameter] = []
    fdp_ep_response: str

    @classmethod
    def from_spec_path(
        cls, fdp_spec: FDPSpec, fdp_path: str
    ) -> SFDPSourceDetails | None:
        fdp_get_op: OpenApiOperation | None = fdp_spec.paths[fdp_path].http_get
        if not fdp_get_op:
            logger.warning(f"no get operation in details for {fdp_path}, skipping")
            return None

        fdp_ep_name = fdp_get_op.operationId
        fdp_ep_params = fdp_get_op.parameters
        fdp_resp_schema: Schema | None = fdp_get_op.response_schema
        if not fdp_resp_schema:
            logger.warning(f"no response data schema for {fdp_path}, skipping")
            return None
        resolved_fdp_ep_response: ResolvedSchema | None = fdp_spec.resolve_schema(
            fdp_resp_schema
        )
        if not resolved_fdp_ep_response or not resolved_fdp_ep_response.name:
            logger.warning("failed to resolve fdp response schema")
            return None

        fdp_ep_response = resolved_fdp_ep_response.name
        # logger.debug(f"creating SFDPSourceDetails: fdp_ep_name={fdp_ep_name}, fdp_path={fdp_path}, fdp_ep_params={fdp_ep_params}, fdp_ep_response={fdp_ep_response}, fdp_get_op={fdp_get_op}")
        return cls(
            fdp_ep_name=fdp_ep_name,
            fdp_ep_path=fdp_path,
            fdp_ep_descr=fdp_get_op.description or "no path description",
            fdp_ep_summary=fdp_get_op.summary or "no path summary",
            fdp_ep_params=fdp_ep_params,
            fdp_ep_response=fdp_ep_response,
        )


class SFDPTargetDetails(MyBaseModel):
    sfdp_ep_name: str
    sfdp_ep_path: str
    sfdp_ep_descr: str
    sfdp_ep_responses: list[ASGResponseSchema]
    sfdp_ep_params: list[ASGResponseParam]


class SFDPEndpoint(MyBaseModel):
    source: SFDPSourceDetails
    target: SFDPTargetDetails
    url: str
    key: str
    timeout: int

    @classmethod
    def from_specs(
        cls,
        ep_name: str,
        asg_ep: ASGEndpointContent,
        fdp_spec: FDPSpec,
        fdp_url: str,
        fdp_timeout: int,
        fdp_key: str,
    ) -> SFDPEndpoint | None:

        #  check ASG spec is complete
        ep_path: str | None = asg_ep.sfdp_ep_path
        if not ep_path:
            logger.warning(
                f"asg_spec for {ep_name} does not have SFDP path, skipping this endpoint"
            )
            return None

        sfdp_ep_responses = asg_ep.response_schemas
        if not sfdp_ep_responses:
            logger.warning(
                f"asg_spec for {ep_name} does not have response schemas, skipping this endpoint"
            )
            return None

        fdp_path: str | None = asg_ep.fdp_ep_path
        if not fdp_path or fdp_path not in fdp_spec.paths:
            logger.warning(
                f"asg_spec references unknown FDP path {fdp_path} for {ep_name}, skipping this endpoint"
            )
            return None

        sfdp_ep_source = SFDPSourceDetails.from_spec_path(
            fdp_spec=fdp_spec,
            fdp_path=fdp_path,
        )
        if not sfdp_ep_source:
            logger.warning(
                f"could not resolve SFDP endpoint source from FDP path {fdp_path}, skipping this endpoint"
            )
            return None

        sfdp_target = SFDPTargetDetails(
            sfdp_ep_name=ep_name,
            sfdp_ep_descr=asg_ep.sfdp_ep_descr or "No description",
            sfdp_ep_path=ep_path,
            sfdp_ep_responses=sfdp_ep_responses,
            sfdp_ep_params=asg_ep.sfdp_ep_params or [],
        )

        result = SFDPEndpoint(
            target=sfdp_target,
            source=sfdp_ep_source,
            url=fdp_url,
            timeout=fdp_timeout,
            key=fdp_key,
        )
        logger.debug(f"resolved endpoint {ep_name} from FDP path {fdp_path}:\n{result}")
        return result

    # shortcuts for source details
    @property
    def fdp_ep_name(self):
        return self.source.fdp_ep_name

    @property
    def fdp_ep_path(self):
        return self.source.fdp_ep_path

    @property
    def fdp_ep_params(self):
        return self.source.fdp_ep_params

    @property
    def fdp_ep_p_params(self) -> dict[str, OpenApiParameter]:
        return {p.name: p for p in self.fdp_ep_params if p.in_ == "path"}

    @property
    def fdp_ep_q_params(self) -> dict[str, OpenApiParameter]:
        return {p.name: p for p in self.fdp_ep_params if p.in_ == "query"}

    @property
    def fdp_ep_response(self):
        return self.source.fdp_ep_response

    # shortcuts for target details
    @property
    def sfdp_ep_name(self) -> str:
        return self.target.sfdp_ep_name

    @property
    def sfdp_ep_descr(self):
        return self.target.sfdp_ep_descr

    @property
    def sfdp_ep_responses(self) -> list[ASGResponseSchema]:
        return self.target.sfdp_ep_responses

    @property
    def sfdp_ep_params_list(self) -> list[ASGResponseParam]:
        return self.target.sfdp_ep_params

    @property
    def sfdp_ep_params_dict(self) -> dict[str, ASGResponseParam]:
        return {p.name: p for p in self.target.sfdp_ep_params}

    @property
    def sfdp_ep_param_names(self) -> set[str]:
        return {p.name for p in (self.target.sfdp_ep_params or [])}

    # generic shortcuts
    @property
    def http_method(self):
        return "get"


class SFDPSpec(MyBaseModel):
    sfdp_endpoints: list[SFDPEndpoint]

    @classmethod
    def from_specs(
        cls,
        fdp_spec: FDPSpec,
        asg_spec: ASGSpec,
        fdp_url: str,
        fdp_timeout: int,
        fdp_key: str,
    ) -> SFDPSpec:
        """
        Cross-reference ASG spec with FDP spec and produce SFDP spec.
        """
        sfdp_eps: list[SFDPEndpoint] = []

        for asg_ep in asg_spec.sfdp_endpoints:
            for asg_ep_name, asg_ep_content in asg_ep.items():
                # logger.debug(f"parsing asg_ep_name={asg_ep_name}")
                sfdp_ep = SFDPEndpoint.from_specs(
                    ep_name=asg_ep_name,
                    asg_ep=asg_ep_content,
                    fdp_spec=fdp_spec,
                    fdp_url=fdp_url,
                    fdp_timeout=fdp_timeout,
                    fdp_key=fdp_key,
                )
                if sfdp_ep:
                    sfdp_eps.append(sfdp_ep)

        return cls(sfdp_endpoints=sfdp_eps)

    @property
    def ep_names(self) -> list[str]:
        """Return all SFDP endpoint names defined in this object."""
        return [ep.target.sfdp_ep_name for ep in self.sfdp_endpoints]

    @property
    def num_eps(self) -> int:
        """Return the number of SFDP endpoints defined in this object."""
        return len(self.sfdp_endpoints)
