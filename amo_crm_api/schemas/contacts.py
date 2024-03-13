from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import AfterValidator, AliasChoices, BaseModel, Field

from ..utils import set_tz
from .base_model import BaseModelForFieldsSchema, MultiTextField
from .common import CustomFieldsValueSchema, ValueSchema


class ContactLeadSchema(BaseModel):
    id: int


class ContactEmbeddedSchema(BaseModel):
    tags: List
    leads: List[ContactLeadSchema]
    companies: List


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
        Optional[datetime], AfterValidator(set_tz), Field(exclude=True)
    ] = None
    updated_at: Annotated[
        Optional[datetime], AfterValidator(set_tz), Field(exclude=True)
    ] = None
    closest_task_at: Annotated[Optional[datetime], AfterValidator(set_tz)] = None
    is_deleted: Optional[bool] = None
    is_unsorted: Optional[bool] = None
    custom_fields_values: Annotated[
        Optional[List[CustomFieldsValueSchema]],
        Field(validation_alias=AliasChoices("custom_fields", "custom_fields_values")),
    ] = None
    account_id: Optional[int] = None
    embedded: Annotated[
        Optional[ContactEmbeddedSchema], Field(alias="_embedded")
    ] = None
    leads: Annotated[
        List[ContactLeadSchema],
        Field(validation_alias=AliasChoices("leads", "linked_leads_id")),
        Field(exclude=True),
    ] = []
    contact_type: Optional[str] = None
    phone: Annotated[
        List[ValueSchema], MultiTextField(field_code="PHONE"), Field(exclude=True)
    ] = []
    email: Annotated[
        List[ValueSchema], MultiTextField(field_code="EMAIL"), Field(exclude=True)
    ] = []

    def model_post_init(self, __context) -> None:
        if self.embedded and self.embedded.leads:
            self.leads = self.embedded.leads
        super().model_post_init(__context)
