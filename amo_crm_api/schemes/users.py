from typing import Any, List, Optional

from pydantic import BaseModel


class LeadsScheme(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class ContactsScheme(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class CompaniesScheme(BaseModel):
    view: str
    edit: str
    add: str
    delete: str
    export: str


class TasksScheme(BaseModel):
    edit: str
    delete: str


class StatusRightActionsScheme(BaseModel):
    view: str
    edit: str
    delete: str


class StatusRightScheme(BaseModel):
    entity_type: str
    pipeline_id: int
    status_id: int
    rights: StatusRightActionsScheme


class RightsScheme(BaseModel):
    leads: LeadsScheme
    contacts: ContactsScheme
    companies: CompaniesScheme
    tasks: TasksScheme
    mail_access: bool
    catalog_access: bool
    files_access: bool
    status_rights: List[StatusRightScheme]
    catalog_rights: Any
    custom_fields_rights: Any
    oper_day_reports_view_access: bool
    oper_day_user_tracking: bool
    is_admin: bool
    is_free: bool
    is_active: bool
    group_id: Optional[int] = None
    role_id: Optional[int] = None


class UserScheme(BaseModel):
    id: int
    name: str
    email: str
    lang: str
    rights: RightsScheme
