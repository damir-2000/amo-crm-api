from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import AfterValidator, AliasChoices, BaseModel, Field

from ..utils import set_tz
from .base_model import BaseModelForFieldsScheme
from .common import CustomFieldsValueScheme


class LeadContactScheme(BaseModel):
    id: int
    is_main: bool


class LeadTagScheme(BaseModel):
    id: int
    name: str
    color: Optional[str] = None


class LeadEmbeddedScheme(BaseModel):
    tags: List[LeadTagScheme]
    companies: List
    contacts: List[LeadContactScheme]


class LeadScheme(BaseModelForFieldsScheme):
    id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[int] = None
    responsible_user_id: Optional[int] = None
    group_id: Optional[int] = None
    status_id: Optional[int] = None
    old_status_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    loss_reason_id: Optional[int] = None
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
    closed_at: Annotated[
        Optional[datetime], AfterValidator(set_tz), Field(exclude=True)
    ] = None
    closest_task_at: Annotated[
        Optional[datetime], AfterValidator(set_tz), Field(exclude=True)
    ] = None
    is_deleted: Optional[bool] = None
    custom_fields_values: Annotated[
        List[CustomFieldsValueScheme],
        Field(validation_alias=AliasChoices("custom_fields", "custom_fields_values")),
    ] = []
    score: Optional[float] = None
    account_id: Optional[int] = None
    labor_cost: Optional[float] = None
    embedded: Annotated[Optional[LeadEmbeddedScheme], Field(alias="_embedded")] = None
    contacts: Annotated[List[LeadContactScheme], Field(exclude=True)] = []

    def model_post_init(self, __context) -> None:
        if self.embedded and self.embedded.contacts:
            self.contacts = self.embedded.contacts
        super().model_post_init(__context)
