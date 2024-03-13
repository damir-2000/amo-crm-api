from typing import Any, List, Optional

from pydantic import BaseModel


class LeadsSchema(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class ContactsSchema(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class CompaniesSchema(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class TasksSchema(BaseModel):
    edit: str
    delete: str


class StatusRightActionsSchema(BaseModel):
    view: str
    edit: str
    delete: str


class StatusRightSchema(BaseModel):
    entity_type: str
    pipeline_id: int
    status_id: int
    rights: StatusRightActionsSchema


class RightsSchema(BaseModel):
    leads: LeadsSchema
    contacts: ContactsSchema
    companies: CompaniesSchema
    tasks: TasksSchema
    mail_access: bool
    catalog_access: bool
    files_access: bool
    status_rights: List[StatusRightSchema]
    catalog_rights: Any
    custom_fields_rights: Any
    oper_day_reports_view_access: bool
    oper_day_user_tracking: bool
    is_admin: bool
    is_free: bool
    is_active: bool
    group_id: Optional[int] = None
    role_id: Optional[int] = None


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    lang: str
    rights: RightsSchema
