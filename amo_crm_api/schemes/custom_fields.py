from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Enum(BaseModel):
    id: int
    value: str
    sort: int
    code: Optional[str] = None


class RequiredStatus(BaseModel):
    pipeline_id: int
    status_id: int


class CustomField(BaseModel):
    id: int
    name: str
    type: str
    account_id: int
    code: Optional[str]
    sort: int
    is_api_only: bool
    enums: Optional[List[Enum]]
    group_id: Optional[str]
    required_statuses: List[RequiredStatus]
    is_deletable: bool
    is_predefined: bool
    entity_type: str
    tracking_callback: Any
    remind: Optional[str]
    triggers: List
    currency: Any
    hidden_statuses: List
    chained_lists: Any
