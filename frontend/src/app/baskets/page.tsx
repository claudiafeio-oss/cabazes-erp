import { apiGet } from '../../lib/api';
import type { BasketBom } from '../../lib/types';
import { PageShell, SectionCard, SectionGrid } from '../../components/PageShell';

export default async function BasketsPage() {
  const bomsResult = await apiGet<BasketBom[]>('/baskets');
  const boms = bomsResult.data ?? [];

  return (
    <PageShell
      title="BOMs"
      description="Definição de cabazes e componentes."
    >
      <SectionGrid>
        <SectionCard title="Criar BOM">
          <p style={{ margin: 0, color: '#555' }}>
            Defina componentes, quantidades e substituições.
          </p>
        </SectionCard>
        <SectionCard title="Lista de BOMs">
          {bomsResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{bomsResult.error}</p>
          ) : boms.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>Sem BOMs registadas.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Produto</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Versão</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Ativo</th>
                </tr>
              </thead>
              <tbody>
                {boms.map((bom) => (
                  <tr key={bom.id}>
                    <td style={{ padding: '6px 0' }}>{bom.id}</td>
                    <td style={{ padding: '6px 0' }}>{bom.basket_product_id}</td>
                    <td style={{ padding: '6px 0' }}>{bom.version}</td>
                    <td style={{ padding: '6px 0' }}>{bom.active ? 'Sim' : 'Não'}</td>
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
