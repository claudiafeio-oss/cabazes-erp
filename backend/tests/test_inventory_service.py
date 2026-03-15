from app.models.location import Location
from app.models.product import Product
from app.services.inventory_service import (
    apply_inventory_adjustment,
    create_inventory_adjustment,
)
from app.services.stock_service import get_stock_balance, create_stock_move


def test_inventory_adjustment_creates_stock_moves(session):
    product = Product(
        sku="P4",
        name="Produto 4",
        product_type="raw",
        unit_of_measure="kg",
    )
    location = Location(code="A5", name="Armazem 5")
    session.add_all([product, location])
    session.flush()

    create_stock_move(
        session,
        product_id=product.id,
        location_id=location.id,
        quantity=5,
        move_type="purchase_receipt",
    )

    adjustment = create_inventory_adjustment(
        session,
        location_id=location.id,
        lines=[
            {
                "product_id": product.id,
                "quantity_counted": 3,
                "quantity_system": 5,
            }
        ],
    )
    apply_inventory_adjustment(session, adjustment.id)

    assert get_stock_balance(session, product.id, location.id) == 3.0
