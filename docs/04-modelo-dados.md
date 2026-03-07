# Modelo de Dados

## Entidades principais

- products
- suppliers
- supplier_products
- locations
- lots
- purchase_orders
- purchase_order_lines
- purchase_receipts
- purchase_receipt_lines
- basket_boms
- basket_bom_lines
- substitution_groups
- substitution_group_items
- assembly_orders
- assembly_order_planned_lines
- assembly_order_consumption_lines
- assembly_order_output_lines
- stock_moves
- stock_balance
- inventory_adjustments
- inventory_adjustment_lines
- users
- audit_logs

## Princípios

- `stock_moves` é a fonte da verdade.
- `stock_balance` é um saldo derivado para performance.
- Ordens de montagem guardam snapshot da BOM.
- Consumo real é separado do planeado.
