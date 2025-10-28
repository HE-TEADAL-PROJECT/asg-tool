from __future__ import annotations  # to allow using the defined models as types
from pydantic import BaseModel, ConfigDict, model_validator, Field
from typing import Any
from enum import Enum


class SchemaType(str, Enum):
    OBJECT = "object"
    ARRAY = "array"
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NULL = "null"
    FLOAT = "float"      # non-standard
    BOOL = "bool"        # non-standard



class HTTPResponseCode(str, Enum):
    OK = "200"


class HTTPResponseContent(str, Enum):
    DATA = "application/json"


class MyBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    def __str__(self):
        return self.model_dump_json(
            indent=2,
            by_alias=True,
            exclude_none=True,
            # exclude_unset=True,
        )


class Schema(MyBaseModel):
    type: SchemaType | None = (
        None  # string, number, integer, boolean, array, object, null
    )
    nullable: bool = False
    properties: dict[str, Schema] | None = None
    items: Schema | None = None
    example: Any | None = (None,)
    required: list[str] | None = None
    ref: str | None = Field(default=None, alias="$ref")

    @model_validator(mode="after")
    def check_validity(self) -> Schema:
        # If $ref is present, no other fields should be set
        if self.ref:
            if any([self.type, self.properties, self.items]):
                raise ValueError("$ref schemas must not define type/properties/items")
            return self

        if self.type == SchemaType.OBJECT:
            if self.items is not None:
                raise ValueError("object schemas cannot define 'items'")
        elif self.type == SchemaType.ARRAY:
            if self.items is None:
                raise ValueError("array schemas must define 'items'")
            if self.properties is not None:
                raise ValueError("array schemas cannot define 'properties'")
        elif self.type in {
            SchemaType.STRING,
            SchemaType.NUMBER,
            SchemaType.INTEGER,
            SchemaType.BOOLEAN,
            SchemaType.NULL,
        }:
            if self.properties is not None or self.items is not None:
                raise ValueError(
                    f"scalar type '{self.type}' cannot define 'properties' or 'items'"
                )
        elif self.type in {SchemaType.FLOAT, SchemaType.BOOL}:
            self.type = SchemaType.NUMBER if self.type == SchemaType.FLOAT else SchemaType.BOOLEAN
        elif self.type is None:
            raise ValueError("Schema must define either '$ref' or 'type'")

        return self


class ResolvedSchema(MyBaseModel):
    name: str | None = None
    resolved_schema: Schema
