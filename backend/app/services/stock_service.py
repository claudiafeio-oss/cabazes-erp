from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.lot import Lot
from app.models.stock_balance import StockBalance
from app.models.stock_move import MoveType, ReferenceType, StockMove


# ─────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────

def create_stock_move(
    session: Session,
    product_id: int,
    location_id: int,
    quantity: float,
    move_type: MoveType,
    lot_id: int | None = None,
    reference_type: ReferenceType | None = None,
    reference_id: int | None = None,
    unit_cost: float | None = None,
    occurred_at: datetime | None = None,
) -> StockMove:
    """
    Único ponto de entrada para criar movimentos de stock.
    Garante que o saldo é sempre atualizado junto com o movimento.
    """
    qty = _to_decimal(quantity)
    move = StockMove(
        product_id=product_id,
        location_id=location_id,
        lot_id=lot_id,
        quantity=qty,
        move_type=move_type.value,
        reference_type=reference_type.value if reference_type else None,
        reference_id=reference_id,
        unit_cost=_to_decimal(unit_cost) if unit_cost is not None else None,
        occurred_at=occurred_at or datetime.now(timezone.utc),
    )
    session.add(move)
    _update_stock_balance(session, product_id, location_id, lot_id, qty)
    session.flush()
    return move


def adjust_stock_balance(
    session: Session,
    product_id: int,
    location_id: int,
    lot_id: int | None,
    new_quantity: float,
    reason: str,
) -> StockMove:
    """
    Ajuste de inventário manual — cria movimento de ADJUSTMENT
    e acerta o saldo para o valor real contado.
    Não usar para receções ou consumos — usar create_stock_move.
    """
    current = get_stock_balance(session, product_id, location_id, lot_id)
    delta = _to_decimal(new_quantity) - _to_decimal(current)

    return create_stock_move(
        session=session,
        product_id=product_id,
        location_id=location_id,
        quantity=float(delta),
        move_type=MoveType.ADJUSTMENT,
        lot_id=lot_id,
        reference_type=ReferenceType.INVENTORY_ADJUSTMENT,
    )


def get_stock_balance(
    session: Session,
    product_id: int,
    location_id: int,
    lot_id: int | None = None,
) -> float:
    if lot_id is None:
        total = session.execute(
            select(func.coalesce(func.sum(StockBalance.quantity), 0)).where(
                StockBalance.product_id == product_id,
                StockBalance.location_id == location_id,
            )
        ).scalar_one()
        return float(total)

    balance = session.execute(
        select(StockBalance).where(
            StockBalance.product_id == product_id,
            StockBalance.location_id == location_id,
            StockBalance.lot_id == lot_id,
        )
    ).scalar_one_or_none()
    return float(balance.quantity) if balance else 0.0


def suggest_fefo(
    session: Session,
    product_id: int,
    location_id: int,
    reference_date: date | None = None,
    include_expired: bool = False,
) -> list[Lot]:
    """
    Devolve lotes com stock disponível ordenados por FEFO.
    - reference_date: data de referência (default: hoje)
    - include_expired: se False (default), exclui lotes já expirados
    """
    today = reference_date or date.today()

    query = (
        select(Lot)
        .join(StockBalance, StockBalance.lot_id == Lot.id)
        .where(
            StockBalance.product_id == product_id,
            StockBalance.location_id == location_id,
            StockBalance.quantity > 0,
        )
    )

    if not include_expired:
        # lotes sem data de validade são sempre incluídos (nulls_last já trata a ordenação)
        query = query.where(
            (Lot.expiry_date == None) | (Lot.expiry_date >= today)
        )

    query = query.order_by(Lot.expiry_date.asc().nulls_last(), Lot.id.asc())
    return list(session.execute(query).scalars())


# ─────────────────────────────────────────────
# API privada — não usar fora deste módulo
# ─────────────────────────────────────────────

def _update_stock_balance(
    session: Session,
    product_id: int,
    location_id: int,
    lot_id: int | None,
    quantity_delta: Decimal,
) -> StockBalance:
    """
    Privado. Só deve ser chamado por create_stock_move.
    Atualizar o saldo sem criar movimento quebra a rastreabilidade.
    """
    balance = session.execute(
        select(StockBalance).where(
            StockBalance.product_id == product_id,
            StockBalance.location_id == location_id,
            StockBalance.lot_id == lot_id,
        )
    ).scalar_one_or_none()

    if balance is None:
        balance = StockBalance(
            product_id=product_id,
            location_id=location_id,
            lot_id=lot_id,
            quantity=quantity_delta,
        )
        session.add(balance)
    else:
        balance.quantity = _to_decimal(balance.quantity) + quantity_delta

    session.flush()
    return balance


def _to_decimal(value: float | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))