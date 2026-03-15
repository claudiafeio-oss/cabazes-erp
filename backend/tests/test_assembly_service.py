from app.models.basket_bom import BasketBom
from app.models.basket_bom_line import BasketBomLine
from datetime import date

from app.models.location import Location
from app.models.lot import Lot
from app.models.product import Product
from app.services.assembly_service import (
    create_assembly_order,
    record_assembly_consumption,
    record_assembly_output,
)
from app.services.stock_service import get_stock_balance, create_stock_move


def test_create_assembly_order_snapshots_bom(session):
    basket = Product(
        sku="B1",
        name="Cabaz",
        product_type="basket",
        unit_of_measure="un",
    )
    component = Product(
        sku="C1",
        name="Componente",
        product_type="raw",
        unit_of_measure="kg",
    )
    session.add_all([basket, component])
    session.flush()

    bom = BasketBom(basket_product_id=basket.id, version="v1", active=True)
    session.add(bom)
    session.flush()
    session.add(
        BasketBomLine(
            basket_bom_id=bom.id, component_product_id=component.id, quantity=2
        )
    )
    session.flush()

    order = create_assembly_order(session, basket.id, planned_quantity=3, basket_bom_id=bom.id)
    assert len(order.planned_lines) == 1
    assert float(order.planned_lines[0].quantity_planned) == 6.0


def test_record_consumption_and_output(session):
    basket = Product(
        sku="B2",
        name="Cabaz 2",
        product_type="basket",
        unit_of_measure="un",
    )
    component = Product(
        sku="C2",
        name="Componente 2",
        product_type="raw",
        unit_of_measure="kg",
    )
    location = Location(code="A4", name="Armazem 4")
    session.add_all([basket, component, location])
    session.flush()

    create_stock_move(
        session,
        product_id=component.id,
        location_id=location.id,
        quantity=10,
        move_type="purchase_receipt",
    )

    order = create_assembly_order(session, basket.id, planned_quantity=1)

    record_assembly_consumption(
        session,
        assembly_order_id=order.id,
        location_id=location.id,
        consumptions=[{"product_id": component.id, "quantity": 3}],
    )
    assert get_stock_balance(session, component.id, location.id) == 7.0

    record_assembly_output(
        session,
        assembly_order_id=order.id,
        basket_product_id=basket.id,
        quantity_produced=1,
        location_id=location.id,
        lot_code="CAB-1",
    )
    assert get_stock_balance(session, basket.id, location.id) == 1.0


def test_fefo_violation_raises(session):
    component = Product(
        sku="C3",
        name="Componente 3",
        product_type="raw",
        unit_of_measure="kg",
        track_lot=True,
        track_expiry=True,
    )
    location = Location(code="A8", name="Armazem 8")
    session.add_all([component, location])
    session.flush()

    lot_old = Lot(
        product_id=component.id, lot_code="L-OLD", expiry_date=date(2025, 1, 1)
    )
    lot_new = Lot(
        product_id=component.id, lot_code="L-NEW", expiry_date=date(2026, 1, 1)
    )
    session.add_all([lot_old, lot_new])
    session.flush()

    create_stock_move(
        session,
        product_id=component.id,
        location_id=location.id,
        lot_id=lot_old.id,
        quantity=5,
        move_type="purchase_receipt",
    )
    create_stock_move(
        session,
        product_id=component.id,
        location_id=location.id,
        lot_id=lot_new.id,
        quantity=5,
        move_type="purchase_receipt",
    )

    order = create_assembly_order(session, component.id, planned_quantity=1)

    try:
        record_assembly_consumption(
            session,
            assembly_order_id=order.id,
            location_id=location.id,
            consumptions=[{"product_id": component.id, "quantity": 1, "lot_id": lot_new.id}],
        )
        assert False, "expected ValueError for FEFO violation"
    except ValueError:
        assert True
