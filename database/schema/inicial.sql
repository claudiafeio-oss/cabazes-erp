-- Esquema inicial de referência
-- Fonte da verdade funcional: docs/04-modelo-dados.md

CREATE TABLE IF NOT EXISTS products (
  id BIGSERIAL PRIMARY KEY,
  sku VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  product_type VARCHAR(32) NOT NULL,
  unit_of_measure VARCHAR(32) NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  track_lot BOOLEAN NOT NULL DEFAULT FALSE,
  track_expiry BOOLEAN NOT NULL DEFAULT FALSE,
  minimum_stock NUMERIC(14, 3) NOT NULL DEFAULT 0,
  default_cost NUMERIC(14, 4) NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
