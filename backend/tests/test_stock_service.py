from datetime import date

from app.models.location import Location
from app.models.lot import Lot
from app.models.product import Product
from app.services.stock_service import create_stock_move, get_stock_balance, suggest_fefo


def test_create_stock_move_updates_balance(session):
    product = Product(
        sku="P1",
        name="Produto 1",
        product_type="raw",
        unit_of_measure="kg",
    )
    location = Location(code="A1", name="Armazem")
    session.add_all([product, location])
    session.flush()

    create_stock_move(
        session=session,
        product_id=product.id,
        location_id=location.id,
        quantity=10,
        move_type="purchase_receipt",
    )

    assert get_stock_balance(session, product.id, location.id) == 10.0


def test_suggest_fefo_orders_by_expiry(session):
    product = Product(
        sku="P2",
        name="Produto 2",
        product_type="raw",
        unit_of_measure="kg",
        track_lot=True,
        track_expiry=True,
    )
    location = Location(code="A2", name="Armazem 2")
    session.add_all([product, location])
    session.flush()

    lot1 = Lot(product_id=product.id, lot_code="L1", expiry_date=date(2026, 1, 1))
    lot2 = Lot(product_id=product.id, lot_code="L2", expiry_date=date(2025, 12, 1))
    session.add_all([lot1, lot2])
    session.flush()

    create_stock_move(
        session=session,
        product_id=product.id,
        location_id=location.id,
        lot_id=lot1.id,
        quantity=5,
        move_type="purchase_receipt",
    )
    create_stock_move(
        session=session,
        product_id=product.id,
        location_id=location.id,
        lot_id=lot2.id,
        quantity=5,
        move_type="purchase_receipt",
    )

    ordered = suggest_fefo(session, product.id, location.id)
    assert [lot.id for lot in ordered] == [lot2.id, lot1.id]
