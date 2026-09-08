from enum import Enum

from pydantic import BaseModel, Field


class EntityType(str, Enum):
    PERSON = "PERSON"
    COUNTRY = "COUNTRY"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    OTHER = "OTHER"


class Entity(BaseModel):
    text: str
    type: EntityType


class ClassificationResult(BaseModel):
    is_political: bool
    confidence: float = Field(ge=0.0, le=1.0)

    entities: list[Entity] = Field(default_factory=list)

    reason: str
