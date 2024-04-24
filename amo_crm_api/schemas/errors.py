from typing import List, Annotated

from pydantic import BaseModel, Field


class Error(BaseModel):
    code: str
    path: str
    detail: str


class ValidationError(BaseModel):
    request_id: str
    errors: List[Error]


class Model(BaseModel):
    validation_errors: Annotated[List[ValidationError], Field(alias='validation-errors')]
    title: str
    type: str
    status: int
