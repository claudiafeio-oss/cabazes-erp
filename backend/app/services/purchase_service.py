from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lot import Lot
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_line import PurchaseOrderLine
from app.models.purchase_receipt import PurchaseReceipt
from app.models.purchase_receipt_line import PurchaseReceiptLine
from app.services.stock_service import create_stock_move


def confirm_purchase_order(session: Session, purchase_order_id: int) -> PurchaseOrder:
    order = session.get(PurchaseOrder, purchase_order_id)
    if order is None:
        raise ValueError("purchase order not found")
    order.status = "confirmed"
    order.confirmed_at = datetime.now(timezone.utc)
    session.flush()
    return order


def create_purchase_order(
    session: Session, supplier_id: int, lines: list[dict]
) -> PurchaseOrder:
    order = PurchaseOrder(supplier_id=supplier_id, status="draft")
    session.add(order)
    session.flush()

    for line in lines:
        session.add(
            PurchaseOrderLine(
                purchase_order_id=order.id,
                product_id=line["product_id"],
                quantity_ordered=line["quantity_ordered"],
                unit_cost=line.get("unit_cost"),
            )
        )

    session.flush()
    return order


def receive_purchase_order(
    session: Session,
    purchase_order_id: int,
    lines: list[dict],
) -> PurchaseReceipt:
    order = session.get(PurchaseOrder, purchase_order_id)
    if order is None:
        raise ValueError("purchase order not found")

    receipt = PurchaseReceipt(
        purchase_order_id=purchase_order_id,
        status="received",
        received_at=datetime.now(timezone.utc),
    )
    session.add(receipt)
    session.flush()

    for line in lines:
        lot_id = line.get("lot_id")
        lot_code = line.get("lot_code")
        product_id = line["product_id"]
        expiry_date = line.get("expiry_date")
        product = session.get(Product, product_id)
        if product is None:
            raise ValueError("product not found")
        if product.track_lot and not (lot_id or lot_code):
            raise ValueError("lot required for product")
        if product.track_expiry and not expiry_date:
            raise ValueError("expiry_date required for product")
        if lot_id is None and lot_code:
            existing = session.execute(
                select(Lot).where(
                    Lot.product_id == product_id, Lot.lot_code == lot_code
                )
            ).scalar_one_or_none()
            if existing is None:
                existing = Lot(
                    product_id=product_id,
                    lot_code=lot_code,
                    expiry_date=expiry_date,
                )
                session.add(existing)
                session.flush()
            elif expiry_date and existing.expiry_date is None:
                existing.expiry_date = expiry_date
            lot_id = existing.id

        receipt_line = PurchaseReceiptLine(
            receipt_id=receipt.id,
            product_id=product_id,
            location_id=line["location_id"],
            lot_id=lot_id,
            expiry_date=expiry_date,
            quantity_received=line["quantity"],
            unit_cost=line.get("unit_cost"),
        )
        session.add(receipt_line)

        create_stock_move(
            session=session,
            product_id=product_id,
            location_id=line["location_id"],
            lot_id=lot_id,
            quantity=line["quantity"],
            move_type="purchase_receipt",
            reference_type="purchase_receipt",
            reference_id=receipt.id,
            unit_cost=line.get("unit_cost"),
        )

    session.flush()
    return receipt
