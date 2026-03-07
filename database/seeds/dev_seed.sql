INSERT INTO products (sku, name, product_type, unit_of_measure)
VALUES
  ('CABAZ-TESTE', 'Cabaz Teste', 'finished_basket', 'un')
ON CONFLICT (sku) DO NOTHING;
