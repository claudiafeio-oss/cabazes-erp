export type Product = {
  id: number;
  sku: string;
  name: string;
  product_type: string;
  unit_of_measure: string;
  active: boolean;
  track_lot: boolean;
  track_expiry: boolean;
  minimum_stock: number;
  default_cost: number;
};

export type Supplier = {
  id: number;
  code: string;
  name: string;
  active: boolean;
};

export type Location = {
  id: number;
  code: string;
  name: string;
  active: boolean;
};

export type StockBalance = {
  product_id: number;
  location_id: number;
  lot_id: number | null;
  quantity: number;
};

export type StockMove = {
  id: number;
  product_id: number;
  location_id: number;
  lot_id: number | null;
  quantity: number;
  move_type: string;
  occurred_at: string;
};

export type PurchaseOrder = {
  id: number;
  supplier_id: number;
  status: string;
};

export type AssemblyOrder = {
  id: number;
  basket_product_id: number;
  status: string;
};

export type BasketBom = {
  id: number;
  basket_product_id: number;
  version: string;
  active: boolean;
};
