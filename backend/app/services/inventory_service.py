from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.inventory_adjustment import InventoryAdjustment
from app.models.inventory_adjustment_line import InventoryAdjustmentLine
from app.services.stock_service import create_stock_move


def create_inventory_adjustment(
    session: Session,
    location_id: int,
    lines: list[dict],
) -> InventoryAdjustment:
    adjustment = InventoryAdjustment(
        location_id=location_id,
        status="draft",
        counted_at=datetime.now(timezone.utc),
    )
    session.add(adjustment)
    session.flush()

    for line in lines:
        quantity_counted = line["quantity_counted"]
        quantity_system = line["quantity_system"]
        adjustment_line = InventoryAdjustmentLine(
            adjustment_id=adjustment.id,
            product_id=line["product_id"],
            lot_id=line.get("lot_id"),
            quantity_counted=quantity_counted,
            quantity_system=quantity_system,
            quantity_difference=quantity_counted - quantity_system,
        )
        session.add(adjustment_line)

    session.flush()
    return adjustment


def apply_inventory_adjustment(
    session: Session, adjustment_id: int
) -> InventoryAdjustment:
    adjustment = session.get(InventoryAdjustment, adjustment_id)
    if adjustment is None:
        raise ValueError("inventory adjustment not found")

    for line in adjustment.lines:
        if line.quantity_difference == 0:
            continue
        create_stock_move(
            session=session,
            product_id=line.product_id,
            location_id=adjustment.location_id,
            lot_id=line.lot_id,
            quantity=line.quantity_difference,
            move_type="inventory_adjustment",
            reference_type="inventory_adjustment",
            reference_id=adjustment.id,
        )

    adjustment.status = "applied"
    session.flush()
    return adjustment
