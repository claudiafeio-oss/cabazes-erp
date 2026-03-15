import { apiGet } from '../../lib/api';
import type { AssemblyOrder } from '../../lib/types';
import { PageShell, SectionCard, SectionGrid } from '../../components/PageShell';

export default async function AssembliesPage() {
  const ordersResult = await apiGet<AssemblyOrder[]>('/assemblies');
  const orders = ordersResult.data ?? [];

  return (
    <PageShell
      title="Montagem"
      description="Ordens de montagem e consumos reais."
    >
      <SectionGrid>
        <SectionCard title="Criar ordem">
          <p style={{ margin: 0, color: '#555' }}>
            Criação de ordens e seleção de BOM.
          </p>
        </SectionCard>
        <SectionCard title="Ordens de montagem">
          {ordersResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{ordersResult.error}</p>
          ) : orders.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>Sem ordens em aberto.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Produto</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Estado</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td style={{ padding: '6px 0' }}>{order.id}</td>
                    <td style={{ padding: '6px 0' }}>{order.basket_product_id}</td>
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
