"""API route handlers for shipment endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import select

from database.session import SessionDep
from models.models import Shipment, ShipmentStatus
from schemas.shipment import (
    ShipmentCreate,
    ShipmentDelete,
    ShipmentRead,
    ShipmentUpdate,
)
from services.shipment import ShipmentService

router = APIRouter(prefix="/shipment", tags=["Shipments"])

# Rate limiter setup referenced across router endpoints
limiter = Limiter(key_func=get_remote_address)


def get_shipment_service(session: SessionDep) -> ShipmentService:
    """Dependency helper to instantiate ShipmentService."""
    return ShipmentService(session)


@router.get("/health", tags=["Monitoring"])
async def health_check() -> dict[str, str]:
    """Confirm that the API is running."""
    return {"status": "healthy"}


@router.post(
    "",
    response_model=ShipmentRead,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
async def create_shipment(
    request: Request,
    new_shipment: ShipmentCreate,
    service: ShipmentService = Depends(get_shipment_service),
) -> Shipment:
    """Create and save a new shipment."""
    return await service.add(new_shipment)

@router.get("", response_model=list[ShipmentRead])
@limiter.limit("30/minute")
async def get_shipments(
    request: Request,
    session: SessionDep,
    status_filter: Annotated[
        ShipmentStatus | None,
        Query(alias="status"),
    ] = None,
    content_filter: Annotated[
        str | None,
        Query(alias="content", min_length=1),
    ] = None,
    weight_filter: Annotated[
        float | None,
        Query(alias="weight", gt=0, le=25),
    ] = None,
) -> list[Shipment]:
    """Return shipments, optionally filtered by status, content, or weight."""
    query = select(Shipment)

    if status_filter is not None:
        query = query.where(Shipment.status == status_filter)

    if content_filter is not None:
        query = query.where(Shipment.content.ilike(f"%{content_filter}%"))

    if weight_filter is not None:
        query = query.where(Shipment.weight == weight_filter)

    results = await session.scalars(query)
    return list(results.all())


@router.get("/{shipment_id}", response_model=ShipmentRead)
@limiter.limit("60/minute")
async def get_shipment_by_id(
    request: Request,
    shipment_id: int,
    service: ShipmentService = Depends(get_shipment_service),
) -> Shipment:
    """Return one shipment by its database ID."""
    return await service.get(shipment_id)


@router.patch("/{shipment_id}", response_model=ShipmentRead)
@limiter.limit("15/minute")
async def update_shipment(
    request: Request,
    shipment_id: int,
    shipment_update: ShipmentUpdate,
    service: ShipmentService = Depends(get_shipment_service),
) -> Shipment:
    """Update only the fields supplied by the client."""
    return await service.update(shipment_id, shipment_update)


@router.delete("/{shipment_id}", response_model=ShipmentDelete)
@limiter.limit("10/minute")
async def delete_shipment(
    request: Request,
    shipment_id: int,
    service: ShipmentService = Depends(get_shipment_service),
) -> ShipmentDelete:
    """Delete a shipment by ID."""
    return await service.delete(shipment_id)