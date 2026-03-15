from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lot import Lot
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_line import PurchaseOrderLine
from app.models.purchase_receipt import PurchaseReceipt
from app.models.purchase_receipt_line import PurchaseReceiptLine
from app.models.stock_move import MoveType, ReferenceType
from app.services.stock_service import create_stock_move


# ─────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────

def create_purchase_order(
    session: Session,
    supplier_id: int,
    lines: list[dict],
) -> PurchaseOrder:
    if not lines:
        raise ValueError("uma encomenda tem de ter pelo menos uma linha")

    order = PurchaseOrder(supplier_id=supplier_id, status="draft")
    session.add(order)
    session.flush()

    for line in lines:
        product = session.get(Product, line["product_id"])
        if product is None:
            raise ValueError(f"produto {line['product_id']} não encontrado")
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


def confirm_purchase_order(session: Session, purchase_order_id: int) -> PurchaseOrder:
    order = _get_order_or_raise(session, purchase_order_id)
    _assert_status(order, "draft")
    order.status = "confirmed"
    order.confirmed_at = datetime.now(timezone.utc)
    session.flush()
    return order


def receive_purchase_order(
    session: Session,
    purchase_order_id: int,
    lines: list[dict],
) -> PurchaseReceipt:
    order = _get_order_or_raise(session, purchase_order_id)
    _assert_status(order, "confirmed", "partially_received")

    # índice de linhas encomendadas para validação
    ordered = {
        line.product_id: line
        for line in order.lines
    }

    receipt = PurchaseReceipt(
        purchase_order_id=purchase_order_id,
        status="received",
        received_at=datetime.now(timezone.utc),
    )
    session.add(receipt)
    session.flush()

    for line in lines:
        product_id = line["product_id"]
        qty = line["quantity"]

        product = session.get(Product, product_id)
        if product is None:
            raise ValueError(f"produto {product_id} não encontrado")

        # produto tem de constar da encomenda
        if product_id not in ordered:
            raise ValueError(
                f"produto {product_id} não consta da encomenda {purchase_order_id}"
            )

        # quantidade recebida não pode exceder a encomendada
        order_line = ordered[product_id]
        already_received = _qty_already_received(session, purchase_order_id, product_id)
        remaining = float(order_line.quantity_ordered) - already_received
        if qty > remaining:
            raise ValueError(
                f"produto {product_id}: quantidade a receber ({qty}) excede "
                f"o que falta receber ({remaining})"
            )

        lot_id = line.get("lot_id")
        lot_code = line.get("lot_code")
        expiry_date = line.get("expiry_date")

        if product.track_lot and not (lot_id or lot_code):
            raise ValueError(f"lote obrigatório para produto {product_id}")

        if product.track_expiry and not expiry_date:
            raise ValueError(f"data de validade obrigatória para produto {product_id}")

        # criar ou reutilizar lote
        if lot_id is None and lot_code:
            lot_id = _get_or_create_lot(
                session, product_id, lot_code, expiry_date
            )

        receipt_line = PurchaseReceiptLine(
            receipt_id=receipt.id,
            product_id=product_id,
            location_id=line["location_id"],
            lot_id=lot_id,
            expiry_date=expiry_date,
            quantity_received=qty,
            unit_cost=line.get("unit_cost"),
        )
        session.add(receipt_line)

        create_stock_move(
            session=session,
            product_id=product_id,
            location_id=line["location_id"],
            lot_id=lot_id,
            quantity=qty,
            move_type=MoveType.RECEIPT,
            reference_type=ReferenceType.PURCHASE_RECEIPT,
            reference_id=receipt.id,
            unit_cost=line.get("unit_cost"),
        )

    # atualizar estado da ordem conforme receção total ou parcial
    order.status = _resolve_order_status(session, order)
    session.flush()
    return receipt


# ─────────────────────────────────────────────
# Privado
# ─────────────────────────────────────────────

def _get_order_or_raise(session: Session, purchase_order_id: int) -> PurchaseOrder:
    order = session.get(PurchaseOrder, purchase_order_id)
    if order is None:
        raise ValueError(f"encomenda {purchase_order_id} não encontrada")
    return order


def _assert_status(order: PurchaseOrder, *allowed: str) -> None:
    if order.status not in allowed:
        raise ValueError(
            f"operação não permitida: encomenda está '{order.status}', "
            f"esperado {list(allowed)}"
        )


def _get_or_create_lot(
    session: Session,
    product_id: int,
    lot_code: str,
    expiry_date,
) -> int:
    existing = session.execute(
        select(Lot).where(
            Lot.product_id == product_id,
            Lot.lot_code == lot_code,
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

    return existing.id


def _qty_already_received(
    session: Session,
    purchase_order_id: int,
    product_id: int,
) -> float:
    """
    Soma as quantidades já recebidas para um produto numa encomenda,
    considerando todas as receções anteriores.
    """
    receipts = session.execute(
        select(PurchaseReceipt).where(
            PurchaseReceipt.purchase_order_id == purchase_order_id
        )
    ).scalars().all()

    total = 0.0
    for receipt in receipts:
        for line in receipt.lines:
            if line.product_id == product_id:
                total += float(line.quantity_received)
    return total


def _resolve_order_status(session: Session, order: PurchaseOrder) -> str:
    """
    Após uma receção, determina se a encomenda está totalmente
    recebida ou apenas parcialmente.
    """
    for order_line in order.lines:
        received = _qty_already_received(session, order.id, order_line.product_id)
        if received < float(order_line.quantity_ordered):
            return "partially_received"
    return "received"