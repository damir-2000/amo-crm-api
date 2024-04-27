from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import AliasChoices, BaseModel, Field

from .base_model import BaseModelForFieldsSchema, MultiTextField
from .common import CustomFieldsValueSchema, ValueSchema, TagSchema


class ContactLeadSchema(BaseModel):
    id: int


class ContactEmbeddedSchema(BaseModel):
    tags: List[TagSchema] = []
    leads: List[ContactLeadSchema] = []
    companies: List = []


class ContactSchema(BaseModelForFieldsSchema):
    id: Optional[int] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    created_by: Annotated[
        Optional[int],
        Field(
            validation_alias=AliasChoices("created_by", "created_user_id"), exclude=True
        ),
    ] = None
    updated_by: Annotated[
        Optional[int],
        Field(
            validation_alias=AliasChoices("updated_by", "modified_user_id"),
            exclude=True,
        ),
    ] = None
    created_at: Annotated[
        Optional[datetime], Field(exclude=True)
    ] = None
    updated_at: Annotated[
        Optional[datetime], Field(exclude=True)
    ] = None
    closest_task_at: Annotated[Optional[datetime], Field(exclude=True)] = None
    is_deleted: Optional[bool] = None
    is_unsorted: Optional[bool] = None
    custom_fields_values: Annotated[
        List[CustomFieldsValueSchema],
        Field(validation_alias=AliasChoices("custom_fields", "custom_fields_values")),
    ] = []
    account_id: Optional[int] = None
    embedded: Annotated[
        Optional[ContactEmbeddedSchema],
        Field(alias="_embedded", serialization_alias="_embedded"),
    ] = None
    leads: Annotated[
        List[ContactLeadSchema],
        Field(validation_alias=AliasChoices("leads", "linked_leads_id")),
        Field(exclude=True),
    ] = []
    tags: Annotated[List[TagSchema], Field(exclude=True)] = []
    contact_type: Optional[str] = None
    phone: Annotated[
        Optional[List[ValueSchema]], MultiTextField(field_code="PHONE"), Field(exclude=True)
    ] = None
    email: Annotated[
        Optional[List[ValueSchema]], MultiTextField(field_code="EMAIL"), Field(exclude=True)
    ] = None

    def model_post_init(self, __context) -> None:
        if self.embedded and self.embedded.leads:
            self.leads = self.embedded.leads
            self.tags = self.embedded.tags
        super().model_post_init(__context)
