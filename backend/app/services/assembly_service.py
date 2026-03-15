from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assembly_order import AssemblyOrder
from app.models.assembly_order_consumption_line import AssemblyOrderConsumptionLine
from app.models.assembly_order_output_line import AssemblyOrderOutputLine
from app.models.assembly_order_planned_line import AssemblyOrderPlannedLine
from app.models.basket_bom_line import BasketBomLine
from app.models.lot import Lot
from app.models.product import Product
from app.services.stock_service import create_stock_move, suggest_fefo


def create_assembly_order(
    session: Session,
    basket_product_id: int,
    planned_quantity: float,
    basket_bom_id: int | None = None,
) -> AssemblyOrder:
    order = AssemblyOrder(
        basket_product_id=basket_product_id,
        basket_bom_id=basket_bom_id,
        planned_quantity=planned_quantity,
        produced_quantity=0,
        status="planned",
        scheduled_at=datetime.now(timezone.utc),
    )
    session.add(order)
    session.flush()

    if basket_bom_id is not None:
        bom_lines = session.execute(
            select(BasketBomLine).where(BasketBomLine.basket_bom_id == basket_bom_id)
        ).scalars()
        for line in bom_lines:
            planned_line = AssemblyOrderPlannedLine(
                assembly_order_id=order.id,
                product_id=line.component_product_id,
                quantity_planned=float(line.quantity) * planned_quantity,
                substitution_group_id=line.substitution_group_id,
            )
            session.add(planned_line)

    session.flush()
    return order


def confirm_assembly_order(session: Session, assembly_order_id: int) -> AssemblyOrder:
    order = session.get(AssemblyOrder, assembly_order_id)
    if order is None:
        raise ValueError("assembly order not found")
    order.status = "confirmed"
    session.flush()
    return order


def record_assembly_consumption(
    session: Session,
    assembly_order_id: int,
    consumptions: list[dict],
    location_id: int,
) -> list[AssemblyOrderConsumptionLine]:
    created_lines: list[AssemblyOrderConsumptionLine] = []
    for item in consumptions:
        product = session.get(Product, item["product_id"])
        if product is None:
            raise ValueError("product not found")
        lot_id = item.get("lot_id")
        if product.track_lot and lot_id is None:
            raise ValueError("lot required for product")
        if product.track_expiry:
            if lot_id is None:
                raise ValueError("lot required for product with expiry")
            lot = session.get(Lot, lot_id)
            if lot is None or lot.expiry_date is None:
                raise ValueError("expiry_date required for product with expiry")
            fefo_lots = suggest_fefo(session, product.id, location_id)
            if fefo_lots and fefo_lots[0].id != lot_id:
                raise ValueError("FEFO violation for product")
        line = AssemblyOrderConsumptionLine(
            assembly_order_id=assembly_order_id,
            product_id=item["product_id"],
            lot_id=lot_id,
            quantity_consumed=item["quantity"],
            planned_product_id=item.get("planned_product_id"),
            substitution_group_id=item.get("substitution_group_id"),
        )
        session.add(line)
        created_lines.append(line)

        create_stock_move(
            session=session,
            product_id=item["product_id"],
            location_id=location_id,
            lot_id=lot_id,
            quantity=-abs(item["quantity"]),
            move_type="assembly_consumption",
            reference_type="assembly_order",
            reference_id=assembly_order_id,
        )

    session.flush()
    return created_lines


def record_assembly_output(
    session: Session,
    assembly_order_id: int,
    basket_product_id: int,
    quantity_produced: float,
    location_id: int,
    lot_code: str,
    expiry_date=None,
) -> AssemblyOrderOutputLine:
    if expiry_date is None:
        consumption_lots = session.execute(
            select(Lot.expiry_date)
            .join(
                AssemblyOrderConsumptionLine,
                AssemblyOrderConsumptionLine.lot_id == Lot.id,
            )
            .where(AssemblyOrderConsumptionLine.assembly_order_id == assembly_order_id)
        ).scalars()
        expiry_dates = [date for date in consumption_lots if date is not None]
        if expiry_dates:
            expiry_date = min(expiry_dates)
    existing = session.execute(
        select(Lot).where(
            Lot.product_id == basket_product_id, Lot.lot_code == lot_code
        )
    ).scalar_one_or_none()
    if existing is None:
        existing = Lot(
            product_id=basket_product_id,
            lot_code=lot_code,
            expiry_date=expiry_date,
        )
        session.add(existing)
        session.flush()

    output_line = AssemblyOrderOutputLine(
        assembly_order_id=assembly_order_id,
        product_id=basket_product_id,
        lot_id=existing.id,
        quantity_produced=quantity_produced,
        expiry_date=expiry_date,
    )
    session.add(output_line)

    create_stock_move(
        session=session,
        product_id=basket_product_id,
        location_id=location_id,
        lot_id=existing.id,
        quantity=quantity_produced,
        move_type="assembly_output",
        reference_type="assembly_order",
        reference_id=assembly_order_id,
    )
    session.flush()
    return output_line


def complete_assembly_order(
    session: Session,
    assembly_order_id: int,
    location_id: int,
    quantity_produced: float,
    lot_code: str,
    expiry_date=None,
) -> AssemblyOrder:
    order = session.get(AssemblyOrder, assembly_order_id)
    if order is None:
        raise ValueError("assembly order not found")
    record_assembly_output(
        session=session,
        assembly_order_id=assembly_order_id,
        basket_product_id=order.basket_product_id,
        quantity_produced=quantity_produced,
        location_id=location_id,
        lot_code=lot_code,
        expiry_date=expiry_date,
    )
    order.status = "completed"
    order.produced_quantity = float(order.produced_quantity) + quantity_produced
    session.flush()
    return order
