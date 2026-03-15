from sqlalchemy import select

from app.models.location import Location
from app.models.lot import Lot
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.models.supplier import Supplier
from app.services.purchase_service import confirm_purchase_order, receive_purchase_order
from app.services.stock_service import get_stock_balance


def test_confirm_and_receive_purchase_order(session):
    supplier = Supplier(code="S1", name="Fornecedor 1")
    product = Product(
        sku="P3",
        name="Produto 3",
        product_type="raw",
        unit_of_measure="kg",
    )
    location = Location(code="A3", name="Armazem 3")
    session.add_all([supplier, product, location])
    session.flush()

    order = PurchaseOrder(supplier_id=supplier.id, status="draft")
    session.add(order)
    session.flush()

    confirm_purchase_order(session, order.id)
    assert order.status == "confirmed"

    receive_purchase_order(
        session,
        order.id,
        [
            {
                "product_id": product.id,
                "location_id": location.id,
                "quantity": 12,
                "lot_code": "LOT-1",
            }
        ],
    )

    lot = session.execute(
        select(Lot).where(Lot.product_id == product.id, Lot.lot_code == "LOT-1")
    ).scalar_one()
    assert get_stock_balance(session, product.id, location.id, lot.id) == 12.0


def test_receive_requires_lot_for_tracked_product(session):
    supplier = Supplier(code="S2", name="Fornecedor 2")
    product = Product(
        sku="P4",
        name="Produto 4",
        product_type="raw",
        unit_of_measure="kg",
        track_lot=True,
    )
    location = Location(code="A6", name="Armazem 6")
    session.add_all([supplier, product, location])
    session.flush()

    order = PurchaseOrder(supplier_id=supplier.id, status="draft")
    session.add(order)
    session.flush()

    try:
        receive_purchase_order(
            session,
            order.id,
            [
                {
                    "product_id": product.id,
                    "location_id": location.id,
                    "quantity": 1,
                }
            ],
        )
        assert False, "expected ValueError for missing lot"
    except ValueError:
        assert True


def test_receive_requires_expiry_for_tracked_product(session):
    supplier = Supplier(code="S3", name="Fornecedor 3")
    product = Product(
        sku="P5",
        name="Produto 5",
        product_type="raw",
        unit_of_measure="kg",
        track_expiry=True,
    )
    location = Location(code="A7", name="Armazem 7")
    session.add_all([supplier, product, location])
    session.flush()

    order = PurchaseOrder(supplier_id=supplier.id, status="draft")
    session.add(order)
    session.flush()

    try:
        receive_purchase_order(
            session,
            order.id,
            [
                {
                    "product_id": product.id,
                    "location_id": location.id,
                    "quantity": 1,
                    "lot_code": "LOT-X",
                }
            ],
        )
        assert False, "expected ValueError for missing expiry_date"
    except ValueError:
        assert True
