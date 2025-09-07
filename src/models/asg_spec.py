from __future__ import annotations  # to allow using the defined models as types
from pydantic import Field, RootModel, field_validator, model_validator
from typing import Any
import re
from utils.files_helper import dict_from_file
from utils.log_helper import logger
from .base import MyBaseModel


# ------------------------------
# ASG SPEC - do not change the models as they must follow file format
# ------------------------------

ASG_PARAM_REF_MARKER = "sfdp_ep_param:"
param_ref_pattern = re.compile(rf"{re.escape(ASG_PARAM_REF_MARKER)}:([a-zA-Z_]\w*)")


class ASGResponseSchema(MyBaseModel):
    name: str
    type: str  # we expect "object"
    properties: dict


_type_map = {
    "int": int,
    "str": str,
    "float": float,
    "bool": bool,
}


class ASGResponseParam(MyBaseModel):
    name: str
    py_type: str
    python_type: type | None = Field(default=None, exclude=True)  # <- exclude here
    nullable: bool = False
    example: Any
    ref: str | None = None

    @field_validator("python_type", mode="before")
    def set_python_type(cls, v, info):
        """Auto-derive python_type from py_type string if not explicitly provided."""
        if v is not None:
            return v
        py_type = info.data.get("py_type")
        if py_type in _type_map:
            return _type_map[py_type]
        raise ValueError(f"Unsupported py_type string: {py_type}")

    @field_validator("example")
    def validate_example_matches_type(cls, v, info):
        python_type = info.data.get("python_type")
        if python_type is None:
            return v
        if not isinstance(v, python_type):
            raise TypeError(f"Example {v!r} is not of type {python_type.__name__}")
        return v


class ASGEndpointContent(MyBaseModel):
    fdp_ep_path: str | None = Field(default=None, alias="fdp_path")
    sfdp_ep_path: str | None = Field(default=None, alias="sfdp_path")
    sfdp_ep_descr: str = Field(
        default="No description", alias="sfdp_endpoint_description"
    )
    sfdp_ep_schemas: dict[str, dict] | None = Field(default=None, alias="schema")
    sfdp_ep_params: list[ASGResponseParam] | None = None

    response_schemas: list[ASGResponseSchema] | None = None

    @property
    def sfdp_ep_param_names(self) -> set[str]:
        return {p.name for p in (self.sfdp_ep_params or [])}

    @property
    def sfdp_ep_param_dict(self) -> dict[str, ASGResponseParam]:
        return {p.name: p for p in (self.sfdp_ep_params or [])}

    @model_validator(mode="after")
    def resolve_responses(self) -> "ASGEndpointContent":
        # logger.debug(f"resolving schema params for {self}")
        if not self.sfdp_ep_schemas:
            self.response_schemas = None
            return self

        schemas: list[ASGResponseSchema] = []
        param_ref_pattern = re.compile(r"sfdp_ep_param:([a-zA-Z_]\w*)")
        for schema_name, schema_details in self.sfdp_ep_schemas.items():
            type_ = schema_details["type"]
            if type_ != "object":
                logger.warning(
                    f"response schema contains non-object element: {schema_details}"
                )
                continue

            props = schema_details["properties"]
            resolved_props: dict = {}

            for prop_name, prop_details in props.items():
                if not prop_details or not prop_details.get("description"):
                    logger.warning(
                        f"no description for {prop_name}, nothing to resolve"
                    )
                    resolved_props[prop_name] = []
                    continue

                # Copy to avoid mutating input dict
                prop_copy = dict(prop_details)
                raw_descr = prop_copy.get("description") or ""
                resolved_descr = raw_descr
                linked_params = []
                for param_ref in param_ref_pattern.findall(raw_descr):
                    if param_ref not in self.sfdp_ep_param_dict:
                        raise ValueError(
                            f"Schema property '{prop_name}' in schema '{schema_name}' "
                            f"references missing parameter '{param_ref}'"
                        )
                    param = self.sfdp_ep_param_dict[param_ref]
                    param.ref = f"{ASG_PARAM_REF_MARKER}{param_ref}"
                    linked_params.append(param)
                    # substitute with example in resolved version
                    resolved_descr = resolved_descr.replace(
                        param.ref, str(param.example)
                    )
                prop_copy["resolved_description"] = resolved_descr
                prop_copy["linked_params"] = linked_params
                resolved_props[prop_name] = prop_copy

            schemas.append(
                ASGResponseSchema(
                    name=schema_name,
                    type=type_,
                    properties=resolved_props,
                )
            )

        self.response_schemas = schemas
        return self


class ASGEndpoint(RootModel[dict[str, ASGEndpointContent]]):
    def items(self):
        return self.root.items()

    def keys(self):
        return self.root.keys()

    def values(self):
        return self.root.values()


class ASGSpec(MyBaseModel):
    # should be better called asg_endpoints but we have to follow the file format
    sfdp_endpoints: list[ASGEndpoint]

    @classmethod
    def from_file(cls, asg_spec_path: str) -> ASGSpec:
        spec_dict = dict_from_file(asg_spec_path)
        return cls.model_validate(spec_dict)

    @property
    def ep_names(self) -> list[str]:
        """Return all endpoint names defined in this spec."""
        names: list[str] = []
        for endpoint in self.sfdp_endpoints:
            names.extend(endpoint.root.keys())
        return names
