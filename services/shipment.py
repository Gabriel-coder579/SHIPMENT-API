
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Shipment
from schemas.shipment import (
    ShipmentCreate,
    ShipmentDelete,
    ShipmentUpdate,
)


class ShipmentService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, shipment_id: int) -> Shipment:
        """Retrieve a shipment by ID or raise a 404 exception if not found."""
        shipment = await self.session.get(Shipment, shipment_id)

        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with ID {shipment_id} not found",
            )

        return shipment

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        """Create and save a new shipment record."""
        new_shipment = Shipment(**shipment_create.model_dump())

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def update(
        self, shipment_id: int, shipment_update: ShipmentUpdate
    ) -> Shipment:
        """Update only the fields supplied in a partial update (PATCH)."""
        shipment = await self.get(shipment_id)

        update_data = shipment_update.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field is required for an update",
            )

        for field_name, value in update_data.items():
            setattr(shipment, field_name, value)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, shipment_id: int) -> ShipmentDelete:
        """Delete a shipment record by ID."""
        shipment = await self.get(shipment_id)

        await self.session.delete(shipment)
        await self.session.commit()

        return ShipmentDelete(
            id=shipment_id,
            message=f"Shipment with ID {shipment_id} deleted successfully.",
        )