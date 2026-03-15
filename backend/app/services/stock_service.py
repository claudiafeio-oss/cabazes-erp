from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.lot import Lot
from app.models.stock_balance import StockBalance
from app.models.stock_move import StockMove


def update_stock_balance(
    session: Session,
    product_id: int,
    location_id: int,
    lot_id: int | None,
    quantity_delta: float,
) -> StockBalance:
    balance = session.execute(
        select(StockBalance).where(
            StockBalance.product_id == product_id,
            StockBalance.location_id == location_id,
            StockBalance.lot_id == lot_id,
        )
    ).scalar_one_or_none()
    delta = _to_decimal(quantity_delta)
    if balance is None:
        balance = StockBalance(
            product_id=product_id,
            location_id=location_id,
            lot_id=lot_id,
            quantity=delta,
        )
        session.add(balance)
    else:
        current = _to_decimal(balance.quantity)
        balance.quantity = current + delta
    session.flush()
    return balance


def create_stock_move(
    session: Session,
    product_id: int,
    location_id: int,
    quantity: float,
    move_type: str,
    lot_id: int | None = None,
    reference_type: str | None = None,
    reference_id: int | None = None,
    unit_cost: float | None = None,
    occurred_at: datetime | None = None,
) -> StockMove:
    move = StockMove(
        product_id=product_id,
        location_id=location_id,
        lot_id=lot_id,
        quantity=quantity,
        move_type=move_type,
        reference_type=reference_type,
        reference_id=reference_id,
        unit_cost=unit_cost,
        occurred_at=occurred_at or datetime.now(timezone.utc),
    )
    session.add(move)
    update_stock_balance(session, product_id, location_id, lot_id, quantity)
    session.flush()
    return move


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
    if balance is None:
        return 0.0
    return float(balance.quantity)


def suggest_fefo(session: Session, product_id: int, location_id: int) -> list[Lot]:
    lots = session.execute(
        select(Lot)
        .join(StockBalance, StockBalance.lot_id == Lot.id)
        .where(
            StockBalance.product_id == product_id,
            StockBalance.location_id == location_id,
            StockBalance.quantity > 0,
        )
        .order_by(Lot.expiry_date.asc().nulls_last(), Lot.id.asc())
    ).scalars()
    return list(lots)


def _to_decimal(value: float | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))
