
"""Database models used by the shipment management API."""

from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    """The possible states of a shipment."""

    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    PENDING = "Pending"


class Shipment(SQLModel, table=True):
    """
    Database table containing shipment records.

    Each shipment has package information, a destination, a status,
    and the UTC time when it was created.
    """

    __tablename__ = "shipment"

    # The database automatically assigns this value.
    id: int | None = Field(default=None, primary_key=True)

    # A short description of the package contents.
    content: str = Field(
        min_length=1,
        max_length=255,
        description="Description of the package contents",
    )

    # Shipment weight is measured in kilograms.
    weight: float = Field(
        gt=0,
        le=25.0,
        description="Weight in kilograms. Maximum limit is 25 kg.",
    )

    # New shipments are pending unless another valid status is supplied.
    status: ShipmentStatus = Field(
        default=ShipmentStatus.PENDING,
        description="Current shipment tracking status",
    )

    # Address, city, region, or other destination identifier.
    destination: str = Field(
        min_length=1,
        max_length=255,
        description="Destination address or region",
    )

    # Explicitly enforce TIMESTAMPTZ (TIMESTAMP WITH TIME ZONE) in PostgreSQL
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            comment="Timestamp of record creation in UTC",
        ),
    )