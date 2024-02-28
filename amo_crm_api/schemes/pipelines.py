from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class StatusScheme(BaseModel):
    id: int
    name: str
    sort: int
    is_editable: bool
    pipeline_id: int
    color: str
    type: int
    account_id: int


class PipelineEmbeddedScheme(BaseModel):
    statuses: List[StatusScheme]


class PipelineScheme(BaseModel):
    id: int
    name: str
    sort: int
    is_main: bool
    is_unsorted_on: bool
    is_archive: bool
    account_id: int
    embedded: Annotated[
        Optional[PipelineEmbeddedScheme], Field(alias="_embedded")
    ] = None
    statuses: List[StatusScheme] = []

    def model_post_init(self, __context) -> None:
        if self.embedded and self.embedded.statuses:
            self.statuses = self.embedded.statuses
        super().model_post_init(__context)
