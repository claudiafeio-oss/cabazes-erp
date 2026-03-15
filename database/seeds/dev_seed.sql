-- Seed minimo para desenvolvimento
-- Produtos
INSERT INTO products (
  sku,
  name,
  product_type,
  unit_of_measure,
  active,
  track_lot,
  track_expiry,
  minimum_stock,
  default_cost
)
VALUES
  ('CABAZ-TESTE', 'Cabaz Teste', 'finished_basket', 'un', true, false, false, 0, 0),
  ('ARROZ-1KG', 'Arroz 1kg', 'raw', 'kg', true, true, false, 0, 0),
  ('FEIJAO-1KG', 'Feijao 1kg', 'raw', 'kg', true, true, true, 0, 0)
ON CONFLICT (sku) DO NOTHING;

-- Localizacoes
INSERT INTO locations (code, name, active)
VALUES
  ('A1', 'Armazem Principal', true),
  ('A2', 'Armazem Secundario', true)
ON CONFLICT (code) DO NOTHING;

-- Fornecedores
INSERT INTO suppliers (code, name, active)
VALUES
  ('FORN-001', 'Fornecedor Central', true),
  ('FORN-002', 'Fornecedor Secundario', true)
ON CONFLICT (code) DO NOTHING;

-- Relacao fornecedor-produto
INSERT INTO supplier_products (supplier_id, product_id, unit_cost)
SELECT s.id, p.id, 1.23
FROM suppliers s
JOIN products p ON p.sku IN ('ARROZ-1KG', 'FEIJAO-1KG')
WHERE s.code = 'FORN-001'
ON CONFLICT (supplier_id, product_id) DO NOTHING;

-- Utilizador admin (password hash placeholder; atualizar antes de usar)
INSERT INTO users (email, full_name, hashed_password, role, is_active)
VALUES
  ('admin@cabazes.local', 'Admin', '$2b$12$EEFq9DbzxvzGV4n7Pf3cSehp3hJGCRHVYbR86mm2BawdVdc7Cpcsu', 'admin', true)
ON CONFLICT (email) DO NOTHING;
