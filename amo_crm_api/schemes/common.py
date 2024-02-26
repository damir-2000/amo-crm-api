from datetime import datetime
from typing import Annotated, Generic, List, Optional, TypeVar, Union

from pydantic import AliasChoices, BaseModel, BeforeValidator, Field


class ValueItem(BaseModel):
    file_uuid: str
    version_uuid: str
    file_name: str
    file_size: int
    is_deleted: bool


class Value(BaseModel):
    value: Union[Union[bool, int, float, str], ValueItem]
    subtype: Optional[str] = None
    enum_id: Optional[int] = None
    enum_code: Optional[Optional[str]] = None


class CustomFieldsValue(BaseModel):
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
        Union[Value, List[Value]],
        BeforeValidator(
            lambda x: [
                Value(**i)
                if isinstance(i, dict)
                else i
                if isinstance(i, Value)
                else Value(value=i)
                for i in x
            ]
            if isinstance(x, list)
            else x
        ),
    ]


K = TypeVar("K")


class Embedded(BaseModel, Generic[K]):
    objects: Annotated[
        List[K],
        Field(
            validation_alias=AliasChoices(
                "leads", "contacts", "pipelines", "statuses", "custom_fields", "users"
            )
        ),
    ] = []


class ListModel(BaseModel, Generic[K]):
    page: Annotated[Optional[int], Field(alias="_page")] = None
    embedded: Annotated[Embedded[K], Field(alias="_embedded")]


class UpdateResponse(BaseModel):
    id: int
    updated_at: datetime
