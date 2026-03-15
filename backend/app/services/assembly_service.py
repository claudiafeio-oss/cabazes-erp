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
from app.models.stock_move import MoveType, ReferenceType
from app.services.stock_service import create_stock_move, get_stock_balance, suggest_fefo


# estados válidos e transições permitidas
_VALID_STATUSES = {"draft", "planned", "confirmed", "in_progress", "completed", "cancelled"}
_TRANSITIONS = {
    "draft": {"planned"},
    "planned": {"confirmed", "cancelled"},
    "confirmed": {"in_progress", "cancelled"},
    "in_progress": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}


def _assert_status(order: AssemblyOrder, *allowed: str) -> None:
    if order.status not in allowed:
        raise ValueError(
            f"operação não permitida: ordem está '{order.status}', "
            f"esperado {list(allowed)}"
        )


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
        status="draft",
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
    order = _get_order_or_raise(session, assembly_order_id)
    _assert_status(order, "draft", "planned")
    order.status = "confirmed"
    session.flush()
    return order


def record_assembly_consumption(
    session: Session,
    assembly_order_id: int,
    consumptions: list[dict],
    location_id: int,
) -> list[AssemblyOrderConsumptionLine]:
    order = _get_order_or_raise(session, assembly_order_id)
    _assert_status(order, "confirmed", "in_progress")

    created_lines: list[AssemblyOrderConsumptionLine] = []

    for item in consumptions:
        product = session.get(Product, item["product_id"])
        if product is None:
            raise ValueError(f"produto {item['product_id']} não encontrado")

        lot_id = item.get("lot_id")

        if product.track_lot and lot_id is None:
            raise ValueError(f"lote obrigatório para produto {product.id}")

        if product.track_expiry:
            if lot_id is None:
                raise ValueError(f"lote obrigatório para produto com validade {product.id}")
            lot = session.get(Lot, lot_id)
            if lot is None or lot.expiry_date is None:
                raise ValueError(f"lote {lot_id} sem data de validade")
            fefo_lots = suggest_fefo(session, product.id, location_id)
            if fefo_lots and fefo_lots[0].id != lot_id:
                raise ValueError(f"violação FEFO para produto {product.id}")

        # verificar stock disponível antes de consumir
        available = get_stock_balance(session, product.id, location_id, lot_id)
        qty = item["quantity"]
        if available < qty:
            raise ValueError(
                f"stock insuficiente para produto {product.id}: "
                f"disponível {available}, necessário {qty}"
            )

        line = AssemblyOrderConsumptionLine(
            assembly_order_id=assembly_order_id,
            product_id=item["product_id"],
            lot_id=lot_id,
            quantity_consumed=qty,
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
            quantity=-abs(qty),
            move_type=MoveType.ASSEMBLY_CONSUMPTION,
            reference_type=ReferenceType.ASSEMBLY_ORDER,
            reference_id=assembly_order_id,
        )

    # atualiza estado para in_progress após primeiro consumo
    if order.status == "confirmed":
        order.status = "in_progress"

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
    order = _get_order_or_raise(session, assembly_order_id)
    _assert_status(order, "in_progress", "confirmed")

    # herdar validade mínima dos componentes consumidos se não fornecida
    if expiry_date is None:
        consumption_lots = session.execute(
            select(Lot.expiry_date)
            .join(
                AssemblyOrderConsumptionLine,
                AssemblyOrderConsumptionLine.lot_id == Lot.id,
            )
            .where(AssemblyOrderConsumptionLine.assembly_order_id == assembly_order_id)
        ).scalars()
        expiry_dates = [d for d in consumption_lots if d is not None]
        if expiry_dates:
            expiry_date = min(expiry_dates)

    existing = session.execute(
        select(Lot).where(
            Lot.product_id == basket_product_id,
            Lot.lot_code == lot_code,
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
        move_type=MoveType.ASSEMBLY_OUTPUT,
        reference_type=ReferenceType.ASSEMBLY_ORDER,
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
    order = _get_order_or_raise(session, assembly_order_id)
    _assert_status(order, "in_progress", "confirmed")

    # verificar se todos os componentes planeados foram consumidos
    _assert_planned_lines_consumed(session, order)

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


# ─────────────────────────────────────────────
# Privado
# ─────────────────────────────────────────────

def _get_order_or_raise(session: Session, assembly_order_id: int) -> AssemblyOrder:
    order = session.get(AssemblyOrder, assembly_order_id)
    if order is None:
        raise ValueError(f"ordem de montagem {assembly_order_id} não encontrada")
    return order


def _assert_planned_lines_consumed(session: Session, order: AssemblyOrder) -> None:
    """
    Verifica se todos os componentes planeados têm pelo menos um registo
    de consumo associado. Não valida quantidades — isso é responsabilidade
    do operador via record_assembly_consumption.
    """
    planned_product_ids = {line.product_id for line in order.planned_lines}
    consumed_product_ids = {line.product_id for line in order.consumption_lines}
    missing = planned_product_ids - consumed_product_ids
    if missing:
        raise ValueError(
            f"componentes planeados sem consumo registado: {missing}"
        )