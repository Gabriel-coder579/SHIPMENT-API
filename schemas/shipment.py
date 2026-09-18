"""Request and response schemas for the shipment API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.models import ShipmentStatus


class ShipmentBase(BaseModel):
    """Fields shared by shipment creation and response schemas."""

    content: str = Field(
        min_length=1,
        max_length=255,
        description="Brief description of the package contents",
    )

    weight: float = Field(
        gt=0,
        le=25.0,
        description="Package weight in kilograms",
    )

    status: ShipmentStatus = Field(
        default=ShipmentStatus.PENDING,
        description="Current shipment status",
    )

    destination: str = Field(
        min_length=1,
        max_length=255,
        description="Shipment destination",
    )


class ShipmentCreate(ShipmentBase):
    """
    Data accepted when creating a shipment.

    This class currently uses all fields from ShipmentBase.
    """

    pass


class ShipmentUpdate(BaseModel):
    """
    Optional fields accepted when partially updating a shipment.

    Fields not included in the request are left unchanged.
    """

    content: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    weight: float | None = Field(
        default=None,
        gt=0,
        le=25.0,
    )

    status: ShipmentStatus | None = None

    destination: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class ShipmentRead(ShipmentBase):
    """
    Data returned to API clients.

    The response includes the database ID and creation timestamp.
    """

    id: int
    created_at: datetime

    # Allows Pydantic to read values directly from SQLModel objects.
    model_config = ConfigDict(from_attributes=True)

class ShipmentDelete(BaseModel):
    """
    Data returned to API clients after a shipment is deleted.

    The response includes the database ID and a confirmation message.
    """

    id: int = Field("ID of the deleted shipment")
    message: str = Field(
        default="Shipment deleted successfully.",
        description="Confirmation message for the deletion operation",
    )
