from typing import Any, List, Optional

from pydantic import BaseModel


class Leads(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class Contacts(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class Companies(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class Tasks(BaseModel):
    edit: str
    delete: str


class StatusRightActions(BaseModel):
    view: str
    edit: str
    delete: str


class StatusRight(BaseModel):
    entity_type: str
    pipeline_id: int
    status_id: int
    rights: StatusRightActions


class Rights(BaseModel):
    leads: Leads
    contacts: Contacts
    companies: Companies
    tasks: Tasks
    mail_access: bool
    catalog_access: bool
    files_access: bool
    status_rights: List[StatusRight]
    catalog_rights: Any
    custom_fields_rights: Any
    oper_day_reports_view_access: bool
    oper_day_user_tracking: bool
    is_admin: bool
    is_free: bool
    is_active: bool
    group_id: int
    role_id: int


class User(BaseModel):
    id: int
    name: str
    email: str
    lang: str
    rights: Rights
