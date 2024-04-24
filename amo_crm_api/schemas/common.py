from datetime import datetime
from typing import Annotated, Generic, List, Optional, TypeVar, Union

from pydantic import AliasChoices, BaseModel, BeforeValidator, Field


class ValueItemSchema(BaseModel):
    file_uuid: str
    version_uuid: str
    file_name: str
    file_size: int
    is_deleted: bool


class ValueSchema(BaseModel):
    value: Union[Union[bool, int, float, str], ValueItemSchema, None] = None
    subtype: Optional[str] = None
    enum_id: Annotated[
        Optional[int],
        Field(validation_alias=AliasChoices("enum_id", "enum")),
    ] = None
    enum_code: Annotated[
        Optional[str], Field(validation_alias=AliasChoices("enum_code", "code"))
    ] = None


class CustomFieldsValueSchema(BaseModel):
    field_id: Annotated[
        Optional[int], Field(validation_alias=AliasChoices("id", "field_id"))
    ] = None
    field_name: Annotated[
        Optional[str], Field(validation_alias=AliasChoices("name", "field_name"))
    ] = None
    field_code: Annotated[
        Optional[str], Field(validation_alias=AliasChoices("code", "field_code"))
    ] = None
    field_type: Optional[str] = None
    values: Annotated[
        Union[ValueSchema, List[ValueSchema], None],
        BeforeValidator(
            lambda x: (
                [
                    (
                        ValueSchema(**i)
                        if isinstance(i, dict)
                        else i if isinstance(i, ValueSchema) else ValueSchema(value=i)
                    )
                    for i in x
                ]
                if isinstance(x, list)
                else x
            )
        ),
    ] = None


K = TypeVar("K")


class EmbeddedSchema(BaseModel, Generic[K]):
    objects: Annotated[
        List[K],
        Field(
            validation_alias=AliasChoices(
                "leads",
                "contacts",
                "pipelines",
                "statuses",
                "custom_fields",
                "users",
                "links",
                "loss_reasons",
                "tags"
            )
        ),
    ] = []


class ListModelSchema(BaseModel, Generic[K]):
    page: Annotated[Optional[int], Field(alias="_page")] = None
    embedded: Annotated[EmbeddedSchema[K], Field(alias="_embedded")]


class UpdateResponseSchema(BaseModel):
    id: int
    updated_at: datetime


class ComplexCreateResponseSchema(BaseModel):
    id: Optional[int] = None
    contact_id: Optional[int] = None
    company_id: Optional[int] = None
    merged: Optional[bool] = None


class TagSchema(BaseModel):
    id: int
    name: Optional[str] = None
    color: Annotated[Optional[str], Field(exclude=True)] = None
