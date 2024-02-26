from functools import cached_property
from typing import Any, Generic, Iterable, List, Optional, Type, TypeVar, get_args

from .auth import BaseAuth
from .schemes import (
    Contact,
    CustomField,
    Lead,
    ListModel,
    Pipeline,
    Status,
    UpdateResponse,
    User
)

LeadType = TypeVar("LeadType", bound=Lead)
ContactType = TypeVar("ContactType", bound=Contact)


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

    def get_lead_list(self) -> Iterable[LeadType]:
        model = self._lead_model
        params = {"with": "contacts", "limit": 2, "page": 1}
        return self._objects_list_generator(
            object_type=model, path="/leads", params=params
        )

    def create_lead(self, lead: LeadType) -> LeadType:
        response = self.request(
            method="POST", path="/leads", json=[lead.model_dump(exclude_none=True)]
        )
        return response.content

    # def create_complex_lead(self, lead: LeadType) -> LeadType:
    #     ...

    def update_lead(self, lead: LeadType) -> UpdateResponse:
        lead_id = lead.id
        response = self.request(
            method="PATCH",
            path=f"/leads/{lead_id}",
            json=lead.model_dump(exclude_none=True),
        )
        return UpdateResponse.model_validate_json(json_data=response.content)

    def get_contact(self, contact_id: int) -> ContactType:
        response = self.request(
            method="GET", path=f"/contacts/{contact_id}", params={"with": "leads"}
        )
        return self._contact_model.model_validate_json(json_data=response.content)

    def get_contact_list(self) -> Iterable[ContactType]:
        model = self._contact_model
        params = {"with": "leads", "limit": 2, "page": 1}
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

    def update_contact(self, contact: ContactType) -> UpdateResponse:
        contact_id = contact.id
        response = self.request(
            method="PATCH",
            path=f"/contacts/{contact_id}",
            json=contact.model_dump(exclude_none=True),
        )
        return UpdateResponse.model_validate_json(json_data=response.content)

    def get_pipeline(self, pipeline_id: int) -> Pipeline:
        response = self.request(method="GET", path=f"/leads/pipelines/{pipeline_id}")
        return Pipeline.model_validate_json(response.content)

    def get_pipeline_list(self) -> List[Pipeline]:
        response = self.request(method="GET", path="/leads/pipelines")
        return (
            ListModel[Pipeline]
            .model_validate_json(json_data=response.content)
            .embedded.objects
        )

    def get_pipeline_status(self, pipeline_id: int, status_id: int) -> Status:
        response = self.request(
            method="GET", path=f"/leads/pipelines/{pipeline_id}/statuses/{status_id}"
        )
        return Status.model_validate_json(response.content)

    def get_pipeline_status_list(self, pipeline_id: int) -> List[Status]:
        response = self.request(
            method="GET", path=f"/leads/pipelines/{pipeline_id}/statuses"
        )
        return ListModel[Status].model_validate_json(response.content).embedded.objects

    def get_custom_field(self, field_id: int) -> CustomField:
        response = self.request(method="GET", path=f"/leads/custom_fields/{field_id}")
        return CustomField.model_validate_json(response.content)

    def get_custom_field_list(self) -> Iterable[CustomField]:
        # params = {"limit": 2, "page": 1}
        return self._objects_list_generator(
            object_type=CustomField, path="/leads/custom_fields"
        )

    def get_user(self, user_id) -> User:
        response = self.request(method="GET", path=f"/users/{user_id}")
        return User.model_validate_json(response.content)

    def get_users(self) -> Iterable[User]:
        return self._objects_list_generator(
            object_type=User, path="/users"
        )

    @cached_property
    def _lead_model(self) -> type[LeadType]:
        args = get_args(self.__orig_class__)  # type: ignore
        base_type: type[LeadType] = Lead  # type: ignore
        for arg in args:
            if issubclass(arg, base_type):
                return arg
        return base_type

    @cached_property
    def _contact_model(self) -> Type[ContactType]:
        args = get_args(self.__orig_class__)  # type: ignore
        base_type: Type[ContactType] = Contact  # type: ignore
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
                ListModel[object_type]  # type: ignore
                .model_validate_json(response.content)
                .embedded.objects
            )

            for item in item_list:
                yield item

            params["page"] += 1
