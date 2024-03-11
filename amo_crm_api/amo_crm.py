from functools import cached_property
from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar, get_args

from pydantic import TypeAdapter

from .auth import BaseAuth
from .filters import Filter
from .schemes import (
    ComplexCreateResponseScheme,
    ContactScheme,
    CustomFieldScheme,
    LeadScheme,
    ListModelScheme,
    PipelineScheme,
    StatusScheme,
    UpdateResponseScheme,
    UserScheme,
    LinkScheme
)

LeadType = TypeVar("LeadType", bound=LeadScheme)
ContactType = TypeVar("ContactType", bound=ContactScheme)


class AmoCRMApi(Generic[LeadType, ContactType]):
    def __init__(self, auth: BaseAuth) -> None:
        self._auth = auth
        self.request = self._auth.request
        super().__init__()

    def get_lead(self, lead_id: int) -> LeadType:
        response = self.request(
            method="GET", path=f"/leads/{lead_id}", params={"with": "contacts"}
        )
        return self._lead_model.model_validate_json(json_data=response.content)
    
    def get_lead_links(self, lead_id: int) -> List[LinkScheme]:
        response = self.request(
            method="GET", path=f"/leads/{lead_id}/links",
        )
        return ListModelScheme[LinkScheme].model_validate_json(response.content).embedded.objects

    def get_lead_list(self, filters: List[Filter] = [], limit: int = 50) -> Iterable[LeadType]:
        model = self._lead_model
        params = {"with": "contacts", "limit": limit, "page": 1}
        params.update(self._filters_to_params(filters))
        return self._objects_list_generator(
            object_type=model, path="/leads", params=params
        )

    def create_lead(self, lead: LeadType) -> LeadType:
        response = self.request(
            method="POST", path="/leads", json=[lead.model_dump(exclude_none=True)]
        )
        return response.content

    def create_complex_lead(
        self, lead: LeadType, contact: ContactType
    ) -> ComplexCreateResponseScheme:
        lead_data = lead.model_dump(exclude_none=True)
        contact_data = contact.model_dump(exclude_none=True)
        lead_data["_embedded"] = {}
        lead_data["_embedded"]["contacts"] = [contact_data]
        response = self.request(method="POST", path="/leads/complex", json=[lead_data])

        return TypeAdapter(List[ComplexCreateResponseScheme]).validate_json(
            response.content
        )[0]

    def update_lead(self, lead: LeadType) -> UpdateResponseScheme:
        lead_id = lead.id
        response = self.request(
            method="PATCH",
            path=f"/leads/{lead_id}",
            json=lead.model_dump(exclude_none=True),
        )
        return UpdateResponseScheme.model_validate_json(json_data=response.content)

    def get_contact(self, contact_id: int) -> ContactType:
        response = self.request(
            method="GET", path=f"/contacts/{contact_id}", params={"with": "leads"}
        )
        return self._contact_model.model_validate_json(json_data=response.content)
    
    def get_contact_links(self, contact_id: int) -> List[LinkScheme]:
        response = self.request(
            method="GET", path=f"/contacts/{contact_id}/links",
        )
        return ListModelScheme[LinkScheme].model_validate_json(response.content).embedded.objects
    
    def get_contact_list(self, filters: List[Filter] = [], limit: int = 50) -> Iterable[ContactType]:
        model = self._contact_model
        params = {"with": "leads", "limit": limit, "page": 1}
        params.update(self._filters_to_params(filters))
        return self._objects_list_generator(
            object_type=model, path="/contacts", params=params
        )

    def create_contact(self, contact: ContactType) -> ContactType:
        response = self.request(
            method="POST",
            path="/contacts",
            json=[contact.model_dump(exclude_none=True)],
        )
        return response.content

    def update_contact(self, contact: ContactType) -> UpdateResponseScheme:
        contact_id = contact.id
        response = self.request(
            method="PATCH",
            path=f"/contacts/{contact_id}",
            json=contact.model_dump(exclude_none=True),
        )
        return UpdateResponseScheme.model_validate_json(json_data=response.content)

    def get_pipeline(self, pipeline_id: int) -> PipelineScheme:
        response = self.request(method="GET", path=f"/leads/pipelines/{pipeline_id}")
        return PipelineScheme.model_validate_json(response.content)

    def get_pipeline_list(self) -> List[PipelineScheme]:
        response = self.request(method="GET", path="/leads/pipelines")
        return (
            ListModelScheme[PipelineScheme]
            .model_validate_json(json_data=response.content)
            .embedded.objects
        )

    def get_pipeline_status(self, pipeline_id: int, status_id: int) -> StatusScheme:
        response = self.request(
            method="GET", path=f"/leads/pipelines/{pipeline_id}/statuses/{status_id}"
        )
        return StatusScheme.model_validate_json(response.content)

    def get_pipeline_status_list(self, pipeline_id: int) -> List[StatusScheme]:
        response = self.request(
            method="GET", path=f"/leads/pipelines/{pipeline_id}/statuses"
        )
        return (
            ListModelScheme[StatusScheme]
            .model_validate_json(response.content)
            .embedded.objects
        )

    def get_custom_field(self, field_id: int) -> CustomFieldScheme:
        response = self.request(method="GET", path=f"/leads/custom_fields/{field_id}")
        return CustomFieldScheme.model_validate_json(response.content)

    def get_custom_field_list(self) -> Iterable[CustomFieldScheme]:
        # params = {"limit": 2, "page": 1}
        return self._objects_list_generator(
            object_type=CustomFieldScheme, path="/leads/custom_fields"
        )

    def get_user(self, user_id: int) -> UserScheme:
        response = self.request(method="GET", path=f"/users/{user_id}")
        return UserScheme.model_validate_json(response.content)

    def get_users(self) -> Iterable[UserScheme]:
        return self._objects_list_generator(object_type=UserScheme, path="/users")

    @staticmethod
    def _filters_to_params(filters: List[Filter]) -> Dict[str, Any]:
        params = dict()
        for filter_obj in filters:
            params.update(filter_obj._as_params())
        return params

    @cached_property
    def _lead_model(self) -> type[LeadType]:
        args = get_args(self.__orig_class__)  # type: ignore
        base_type: type[LeadType] = LeadScheme  # type: ignore
        for arg in args:
            if issubclass(arg, base_type):
                return arg
        return base_type

    @cached_property
    def _contact_model(self) -> Type[ContactType]:
        args = get_args(self.__orig_class__)  # type: ignore
        base_type: Type[ContactType] = ContactScheme  # type: ignore
        for arg in args:
            if issubclass(arg, base_type):
                return arg
        return base_type

    def _objects_list_generator(
        self, object_type: type, path: str, params: Optional[dict] = None, limit=250
    ) -> Iterable[Any]:
        params = params if params else {}
        params["limit"] = params.get("limit", limit)
        params["page"] = params.get("page", 1)

        while True:
            response = self.request(method="GET", path=path, params=params)

            if response.status_code != 200:
                break
            item_list = (
                ListModelScheme[object_type]  # type: ignore
                .model_validate_json(response.content)
                .embedded.objects
            )

            for item in item_list:
                yield item

            params["page"] += 1
