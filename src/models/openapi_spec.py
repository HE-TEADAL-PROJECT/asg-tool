from __future__ import annotations  # to allow using the defined models as types
from pydantic import Field, model_validator
from typing import Literal
import re
from .base import (
    MyBaseModel,
    HTTPResponseCode,
    HTTPResponseContent,
    Schema,
)
from utils.log_helper import logger

# ------------------------------
# FDP SPEC (OpenAPI)
# ------------------------------


class OpenApiResponseContent(MyBaseModel):
    schema_: Schema | None = Field(default=None, alias="schema")  # TODO none?


class OpenApiResponse(MyBaseModel):
    description: str | None = None
    content: dict[str, OpenApiResponseContent] | None = (
        None  # 'application/json':'schema'
    )
    # TODO what about
    # '301':
    #   $ref: '#/components/responses/301'


# in can be 'path' meaning it is path parameter like '/path/{path_param}'
class OpenApiParameter(MyBaseModel):
    in_: Literal["query", "path", "header", "cookie"] = Field(alias="in")
    name: str
    required: bool = False  # <-- make optional with default
    schema_: Schema | None = Field(default=None, alias="schema")
    type: str | None = None  # ?


class OpenApiOperation(MyBaseModel):
    summary: str | None = None
    operationId: str | None = None
    description: str | None = None
    parameters: list[OpenApiParameter] = []
    responses: dict[str, OpenApiResponse] = {}


    @model_validator(mode="before")
    def ensure_operation_id(cls, values: dict) -> dict:
        if not values.get("operationId"):
            # logger.warning(f"no operationID: values={values}")
            # Get method and path from context if available
            method = values.get("__method__")  # inject during parsing
            path = values.get("__path__")      # inject during parsing
            if method and path:
                normalized = re.sub(r"[{}]", "", path).strip("/")
                normalized = normalized.replace("/", "_")
                values["operationId"] = f"{method}_{normalized}"

        return values

    @property
    def response_schema(self) -> Schema | None:
        # OpenApiOperation.responses: dict[str, OpenApiResponse] = {}
        fdp_ok_response = self.responses.get(HTTPResponseCode.OK)
        if not fdp_ok_response:
            logger.warning("no ok response")
            return None

        # OpenApiResponse.content: dict[str, OpenApiResponseContent] | None = None
        fdp_resp_content = fdp_ok_response.content
        if not fdp_resp_content:
            logger.warning("no contents in ok responses")
            return None

        fdp_resp_data = fdp_resp_content.get(HTTPResponseContent.DATA)
        if not fdp_resp_data:
            logger.warning("no json in ok responses")
            return None

        # OpenApiResponseContent.schema_: Schema | None = Field(default=None, alias="schema")
        return fdp_resp_data.schema_


class OpenApiPathItem(MyBaseModel):
    http_get: OpenApiOperation | None = Field(default=None, alias="get")
    http_post: OpenApiOperation | None = Field(default=None, alias="post")
    http_put: OpenApiOperation | None = Field(default=None, alias="put")
    http_delete: OpenApiOperation | None = Field(default=None, alias="delete")
    http_patch: OpenApiOperation | None = Field(default=None, alias="patch")


class OpenApiComponents(MyBaseModel):
    schemas: dict[str, Schema] = {}


class OpenApiSpec(MyBaseModel):
    openapi: str
    paths: dict[str, OpenApiPathItem]
    components: OpenApiComponents | None = None

    @model_validator(mode="before")
    def normalize_openapi(cls, values: dict) -> dict:
        # Normalize response keys to strings
        for path, path_item in values.get("paths", {}).items():
            for method in ["get", "post", "put", "delete", "patch"]:
                operation = path_item.get(method)
                if not operation:
                    continue
                # Normalize response keys
                if "responses" in operation:
                    operation["responses"] = {str(k): v for k, v in operation["responses"].items()}
                # Inject context for operationId generation
                operation["__method__"] = method
                operation["__path__"] = path
        return values

@model_validator(mode="before")
def normalize_openapi(cls, values: dict) -> dict:
    for path, path_item in values.get("paths", {}).items():
        for method in ["get", "post", "put", "delete", "patch"]:
            operation = path_item.get(method)
            if operation:
                # Normalize response keys
                if "responses" in operation:
                    operation["responses"] = {str(k): v for k, v in operation["responses"].items()}
                # Inject context for operationId generation
                operation["__method__"] = method
                operation["__path__"] = path
    return values
