from typing import Optional

from pydantic import BaseModel


class MetadataScheme(BaseModel):
    quantity: Optional[int] = None
    catalog_id: Optional[int] = None
    main_contact: Optional[bool] = None
    price_id: Optional[int] = None


class LinkScheme(BaseModel):
    to_entity_id: int
    to_entity_type: str
    metadata: Optional[MetadataScheme]
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
