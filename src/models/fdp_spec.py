from __future__ import annotations  # to allow using the defined models as types
from packaging import version
from pydantic import field_validator
from .base import (
    Schema,
    SchemaType,
    ResolvedSchema,
)
from .openapi_spec import OpenApiSpec
from utils.files_helper import dict_from_file
from utils.log_helper import logger


class FDPSpec(OpenApiSpec):
    @field_validator("openapi")
    @classmethod
    def check_openapi_version(cls, v: str) -> str:
        try:
            # normalize value to be a string
            if not isinstance(v, str):
                v = str(v)

            parsed = version.parse(v)
        except Exception:
            raise ValueError(f"FDP spec has invalid OpenAPI version string: {v}")

        if parsed < version.parse("3.0.0"):
            raise ValueError(f"OpenAPI version must be >= 3.0.0, got {v}")

        return v

    @classmethod
    def from_file(cls, fdp_spec_path: str) -> FDPSpec:
        spec_dict = dict_from_file(fdp_spec_path)
        return cls.model_validate(spec_dict)

    @property
    def ep_names(self) -> list[str]:
        """Return all path names defined in this FDP spec."""
        return list(self.paths.keys())

    def resolve_component_schema(self, component_name: str) -> ResolvedSchema | None:

        if not self.components or not self.components.schemas:
            logger.warning(
                "can not resolve {component_name}, no component schemas are included in spec"
            )
            return None

        referenced_schema = self.components.schemas.get(component_name)
        if not referenced_schema:
            logger.warning(
                "can not resolve {component_name}, did not find it among component schemas included in spec"
            )
            return None

        resolved_schema = self.resolve_schema(referenced_schema)
        if not resolved_schema:
            logger.warning(
                "failed to resolve {component_name} from {referenced_schema}"
            )
            return None

        return ResolvedSchema(
            name=component_name, resolved_schema=resolved_schema.resolved_schema
        )

    def resolve_schema(self, schema: Schema | None) -> ResolvedSchema | None:
        if not schema:
            return None
        if schema.ref:
            component_name = schema.ref.split("/")[-1]
            if not component_name:
                logger.debug(f"no component for schema ref: {schema.ref}")
                return None
            # logger.debug(f"resolving {component_name} from ref: {schema.ref}")
            return self.resolve_component_schema(component_name)

        # array → recurse into items
        if schema.type == SchemaType.ARRAY and schema.items:
            # logger.debug(f"resolving from array: schema.items={schema.items}")
            return self.resolve_schema(schema.items)

        # object → properties may themselves need resolution
        if schema.type == SchemaType.OBJECT and schema.properties:
            schemas_dicts = schema.properties
            # logger.debug(f"resolving from object with schema.properties={schema.properties}")

            type_schema = schemas_dicts.get("type")
            if type_schema:
                if isinstance(type_schema, Schema):
                    # this is actually a type reference
                    return self.resolve_schema(type_schema)

            # normal properties
            prop_schemas: dict[str, Schema] = {}
            for prop_name, prop_schema in schemas_dicts.items():
                resolved_prop_schema = self.resolve_schema(prop_schema)
                if resolved_prop_schema:
                    prop_schemas[prop_name] = resolved_prop_schema.resolved_schema
            return ResolvedSchema(
                resolved_schema=Schema(
                    type=SchemaType.OBJECT,
                    properties=prop_schemas,
                )
            )

        # scalars (string, number, etc.) or object without properties
        return ResolvedSchema(resolved_schema=schema)
