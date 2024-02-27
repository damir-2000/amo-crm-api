from datetime import datetime
from typing import Annotated, Generic, List, Optional, TypeVar, Union

from pydantic import AliasChoices, BaseModel, BeforeValidator, Field


class ValueItemScheme(BaseModel):
    file_uuid: str
    version_uuid: str
    file_name: str
    file_size: int
    is_deleted: bool


class ValueScheme(BaseModel):
    value: Union[Union[bool, int, float, str], ValueItemScheme]
    subtype: Optional[str] = None
    enum_id: Optional[int] = None
    enum_code: Optional[Optional[str]] = None


class CustomFieldsValueScheme(BaseModel):
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
        Union[ValueScheme, List[ValueScheme]],
        BeforeValidator(
            lambda x: [
                ValueScheme(**i)
                if isinstance(i, dict)
                else i
                if isinstance(i, ValueScheme)
                else ValueScheme(value=i)
                for i in x
            ]
            if isinstance(x, list)
            else x
        ),
    ]


K = TypeVar("K")


class EmbeddedScheme(BaseModel, Generic[K]):
    objects: Annotated[
        List[K],
        Field(
            validation_alias=AliasChoices(
                "leads", "contacts", "pipelines", "statuses", "custom_fields", "users"
            )
        ),
    ] = []


class ListModelScheme(BaseModel, Generic[K]):
    page: Annotated[Optional[int], Field(alias="_page")] = None
    embedded: Annotated[EmbeddedScheme[K], Field(alias="_embedded")]


class UpdateResponseScheme(BaseModel):
    id: int
    updated_at: datetime
