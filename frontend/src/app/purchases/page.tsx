import { apiGet } from '../../lib/api';
import type { PurchaseOrder } from '../../lib/types';
import { PageShell, SectionCard, SectionGrid } from '../../components/PageShell';

export default async function PurchasesPage() {
  const ordersResult = await apiGet<PurchaseOrder[]>('/purchase-orders');
  const orders = ordersResult.data ?? [];

  return (
    <PageShell title="Compras" description="Encomendas a fornecedores.">
      <SectionGrid>
        <SectionCard title="Criar encomenda">
          <p style={{ margin: 0, color: '#555' }}>
            Formulário de encomenda será adicionado aqui.
          </p>
        </SectionCard>
        <SectionCard title="Lista de encomendas">
          {ordersResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{ordersResult.error}</p>
          ) : orders.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>Sem encomendas registadas.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Fornecedor</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Estado</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td style={{ padding: '6px 0' }}>{order.id}</td>
                    <td style={{ padding: '6px 0' }}>{order.supplier_id}</td>
                    <td style={{ padding: '6px 0' }}>{order.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </SectionCard>
      </SectionGrid>
    </PageShell>
  );
}
