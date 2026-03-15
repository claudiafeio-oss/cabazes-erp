import { apiGet } from '../../lib/api';
import type { StockBalance, StockMove } from '../../lib/types';
import { PageShell, SectionCard, SectionGrid } from '../../components/PageShell';

export default async function StockPage() {
  const onHandResult = await apiGet<StockBalance[]>('/stock/on-hand');
  const movesResult = await apiGet<StockMove[]>('/stock/movements');

  const onHand = onHandResult.data ?? [];
  const moves = movesResult.data ?? [];

  return (
    <PageShell
      title="Stock"
      description="Consulta por produto, localização e lote."
    >
      <SectionGrid>
        <SectionCard title="Saldos on-hand">
          {onHandResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{onHandResult.error}</p>
          ) : onHand.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>Sem dados de stock.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Produto</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Localização</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Lote</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Quantidade</th>
                </tr>
              </thead>
              <tbody>
                {onHand.map((row) => (
                  <tr key={`${row.product_id}-${row.location_id}-${row.lot_id ?? 'none'}`}>
                    <td style={{ padding: '6px 0' }}>{row.product_id}</td>
                    <td style={{ padding: '6px 0' }}>{row.location_id}</td>
                    <td style={{ padding: '6px 0' }}>{row.lot_id ?? '-'}</td>
                    <td style={{ padding: '6px 0' }}>{row.quantity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </SectionCard>
        <SectionCard title="Movimentos recentes">
          {movesResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{movesResult.error}</p>
          ) : moves.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>Sem movimentos registados.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Produto</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Localização</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Qtd</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Tipo</th>
                </tr>
              </thead>
              <tbody>
                {moves.map((move) => (
                  <tr key={move.id}>
                    <td style={{ padding: '6px 0' }}>{move.id}</td>
                    <td style={{ padding: '6px 0' }}>{move.product_id}</td>
                    <td style={{ padding: '6px 0' }}>{move.location_id}</td>
                    <td style={{ padding: '6px 0' }}>{move.quantity}</td>
                    <td style={{ padding: '6px 0' }}>{move.move_type}</td>
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
