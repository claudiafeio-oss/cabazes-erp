from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.inventory_adjustment import InventoryAdjustment
from app.models.inventory_adjustment_line import InventoryAdjustmentLine
from app.models.lot import Lot
from app.models.product import Product
from app.models.stock_move import MoveType, ReferenceType
from app.services.stock_service import create_stock_move, get_stock_balance


# ─────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────

def create_inventory_adjustment(
    session: Session,
    location_id: int,
    lines: list[dict],
) -> InventoryAdjustment:
    if not lines:
        raise ValueError("um ajuste de inventário tem de ter pelo menos uma linha")

    adjustment = InventoryAdjustment(
        location_id=location_id,
        status="draft",
        counted_at=datetime.now(timezone.utc),
    )
    session.add(adjustment)
    session.flush()

    for line in lines:
        product_id = line["product_id"]
        lot_id = line.get("lot_id")

        # validar produto
        product = session.get(Product, product_id)
        if product is None:
            raise ValueError(f"produto {product_id} não encontrado")

        # validar lote se fornecido
        if lot_id is not None:
            lot = session.get(Lot, lot_id)
            if lot is None:
                raise ValueError(f"lote {lot_id} não encontrado")
            if lot.product_id != product_id:
                raise ValueError(
                    f"lote {lot_id} não pertence ao produto {product_id}"
                )

        # ler saldo real do sistema — não confiar no valor enviado pelo utilizador
        quantity_system = get_stock_balance(session, product_id, location_id, lot_id)
        quantity_counted = line["quantity_counted"]
        quantity_difference = quantity_counted - quantity_system

        adjustment_line = InventoryAdjustmentLine(
            adjustment_id=adjustment.id,
            product_id=product_id,
            lot_id=lot_id,
            quantity_counted=quantity_counted,
            quantity_system=quantity_system,
            quantity_difference=quantity_difference,
        )
        session.add(adjustment_line)

    session.flush()
    return adjustment


def apply_inventory_adjustment(
    session: Session,
    adjustment_id: int,
) -> InventoryAdjustment:
    adjustment = session.get(InventoryAdjustment, adjustment_id)
    if adjustment is None:
        raise ValueError(f"ajuste {adjustment_id} não encontrado")

    if adjustment.status != "draft":
        raise ValueError(
            f"ajuste {adjustment_id} já foi aplicado (estado: '{adjustment.status}')"
        )

    for line in adjustment.lines:
        if line.quantity_difference == 0:
            # sem diferença — nenhum movimento necessário
            continue

        create_stock_move(
            session=session,
            product_id=line.product_id,
            location_id=adjustment.location_id,
            lot_id=line.lot_id,
            quantity=line.quantity_difference,
            move_type=MoveType.ADJUSTMENT,
            reference_type=ReferenceType.INVENTORY_ADJUSTMENT,
            reference_id=adjustment.id,
        )

    adjustment.status = "applied"
    session.flush()
    return adjustment
