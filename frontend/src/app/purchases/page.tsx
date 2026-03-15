'use client';

import { useEffect, useState } from 'react';

type PurchaseOrderLine = {
  product_id: number;
  quantity_ordered: number;
  unit_cost?: number;
};

type PurchaseOrder = {
  id: number;
  supplier_id: number;
  status: string;
};

type Product = {
  id: number;
  sku: string;
  name: string;
};

type Supplier = {
  id: number;
  code: string;
  name: string;
};

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

const STATUS_LABEL: Record<string, string> = {
  draft: 'Rascunho',
  confirmed: 'Confirmada',
  partially_received: 'Parcialmente recebida',
  received: 'Recebida',
  cancelled: 'Cancelada',
};

const STATUS_COLOR: Record<string, string> = {
  draft: 'bg-gray-100 text-gray-600',
  confirmed: 'bg-blue-100 text-blue-700',
  partially_received: 'bg-yellow-100 text-yellow-700',
  received: 'bg-green-100 text-green-700',
  cancelled: 'bg-red-100 text-red-600',
};

export default function PurchasesPage() {
  const [orders, setOrders] = useState<PurchaseOrder[]>([]);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  // formulário
  const [supplierId, setSupplierId] = useState<number | ''>('');
  const [lines, setLines] = useState<PurchaseOrderLine[]>([
    { product_id: 0, quantity_ordered: 1 },
  ]);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/purchase-orders`).then((r) => r.json()),
      fetch(`${API}/suppliers`).then((r) => r.json()),
      fetch(`${API}/products`).then((r) => r.json()),
    ])
      .then(([ordersData, suppliersData, productsData]) => {
        setOrders(ordersData);
        setSuppliers(suppliersData);
        setProducts(productsData);
      })
      .catch(() => setError('Erro ao carregar dados.'))
      .finally(() => setLoading(false));
  }, []);

  function addLine() {
    setLines((prev) => [...prev, { product_id: 0, quantity_ordered: 1 }]);
  }

  function removeLine(index: number) {
    setLines((prev) => prev.filter((_, i) => i !== index));
  }

  function updateLine(index: number, field: keyof PurchaseOrderLine, value: number) {
    setLines((prev) =>
      prev.map((line, i) => (i === index ? { ...line, [field]: value } : line))
    );
  }

  async function handleConfirm(orderId: number) {
    try {
      const res = await fetch(`${API}/purchase-orders/${orderId}/confirm`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Erro ao confirmar');
      const updated = await res.json();
      setOrders((prev) => prev.map((o) => (o.id === updated.id ? updated : o)));
    } catch {
      alert('Erro ao confirmar encomenda.');
    }
  }

  async function handleSubmit() {
    setFormError(null);
    if (!supplierId) return setFormError('Seleciona um fornecedor.');
    if (lines.some((l) => !l.product_id || l.quantity_ordered <= 0))
      return setFormError('Todas as linhas precisam de produto e quantidade válida.');

    setSubmitting(true);
    try {
      const res = await fetch(`${API}/purchase-orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ supplier_id: supplierId, lines }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail ?? 'Erro ao criar encomenda.');
      }
      const newOrder = await res.json();
      setOrders((prev) => [newOrder, ...prev]);
      setShowForm(false);
      setSupplierId('');
      setLines([{ product_id: 0, quantity_ordered: 1 }]);
    } catch (e: unknown) {
      setFormError(e instanceof Error ? e.message : 'Erro desconhecido.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* cabeçalho */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Compras</h1>
          <p className="text-sm text-gray-500 mt-1">Encomendas a fornecedores</p>
        </div>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          {showForm ? 'Cancelar' : '+ Nova encomenda'}
        </button>
      </div>

      {/* formulário de criação */}
      {showForm && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
          <h2 className="text-base font-semibold text-gray-800">Nova encomenda</h2>

          {formError && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              {formError}
            </p>
          )}

          {/* fornecedor */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Fornecedor
            </label>
            <select
              value={supplierId}
              onChange={(e) => setSupplierId(Number(e.target.value))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Seleciona...</option>
              {suppliers.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.code})
                </option>
              ))}
            </select>
          </div>

          {/* linhas */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Produtos
            </label>
            <div className="space-y-2">
              {lines.map((line, i) => (
                <div key={i} className="flex gap-2 items-center">
                  <select
                    value={line.product_id || ''}
                    onChange={(e) => updateLine(i, 'product_id', Number(e.target.value))}
                    className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Produto...</option>
                    {products.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name} ({p.sku})
                      </option>
                    ))}
                  </select>
                  <input
                    type="number"
                    min={1}
                    step={1}
                    value={line.quantity_ordered}
                    onChange={(e) => updateLine(i, 'quantity_ordered', Number(e.target.value))}
                    placeholder="Qtd"
                    className="w-24 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    type="number"
                    min={0}
                    step={0.01}
                    value={line.unit_cost ?? ''}
                    onChange={(e) =>
                      updateLine(i, 'unit_cost', e.target.value ? Number(e.target.value) : 0)
                    }
                    placeholder="Custo unit."
                    className="w-32 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {lines.length > 1 && (
                    <button
                      onClick={() => removeLine(i)}
                      className="text-red-500 hover:text-red-700 text-sm px-2"
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button
              onClick={addLine}
              className="mt-2 text-sm text-blue-600 hover:text-blue-800"
            >
              + Adicionar linha
            </button>
          </div>

          {/* ações */}
          <div className="flex gap-2 pt-2">
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
            >
              {submitting ? 'A criar...' : 'Criar encomenda'}
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="text-gray-600 hover:text-gray-800 text-sm px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
          </div>
        </div>
      )}

      {/* listagem */}
      <div className="bg-white rounded-xl border border-gray-200">
        {loading ? (
          <div className="p-6 text-sm text-gray-500">A carregar...</div>
        ) : error ? (
          <div className="p-6 text-sm text-red-600">{error}</div>
        ) : orders.length === 0 ? (
          <div className="p-6 text-sm text-gray-500">Sem encomendas registadas.</div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left px-6 py-3 text-gray-500 font-medium">#</th>
                <th className="text-left px-6 py-3 text-gray-500 font-medium">Fornecedor</th>
                <th className="text-left px-6 py-3 text-gray-500 font-medium">Estado</th>
                <th className="text-left px-6 py-3 text-gray-500 font-medium">Ações</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-gray-400 font-mono">#{order.id}</td>
                  <td className="px-6 py-4 text-gray-700">
                    {suppliers.find((s) => s.id === order.supplier_id)?.name ?? `Fornecedor ${order.supplier_id}`}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`text-xs font-medium px-2 py-1 rounded-full ${STATUS_COLOR[order.status] ?? 'bg-gray-100 text-gray-600'}`}>
                      {STATUS_LABEL[order.status] ?? order.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {order.status === 'draft' && (
                      <button
                        onClick={() => handleConfirm(order.id)}
                        className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                      >
                        Confirmar
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
