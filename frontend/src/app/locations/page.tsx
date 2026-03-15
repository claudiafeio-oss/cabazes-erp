import { apiGet } from '../../lib/api';
import type { Location } from '../../lib/types';
import { PageShell, SectionCard, SectionGrid } from '../../components/PageShell';

export default async function LocationsPage() {
  const locationsResult = await apiGet<Location[]>('/locations');
  const locations = locationsResult.data ?? [];

  return (
    <PageShell
      title="Localizações"
      description="Armazéns e zonas de stock."
    >
      <SectionGrid>
        <SectionCard title="Criar localização">
          <p style={{ margin: 0, color: '#555' }}>
            Formulário de criação será adicionado.
          </p>
        </SectionCard>
        <SectionCard title="Lista de localizações">
          {locationsResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{locationsResult.error}</p>
          ) : locations.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>
              Sem localizações registadas.
            </p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Código</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Nome</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Ativo</th>
                </tr>
              </thead>
              <tbody>
                {locations.map((location) => (
                  <tr key={location.id}>
                    <td style={{ padding: '6px 0' }}>{location.id}</td>
                    <td style={{ padding: '6px 0' }}>{location.code}</td>
                    <td style={{ padding: '6px 0' }}>{location.name}</td>
                    <td style={{ padding: '6px 0' }}>
                      {location.active ? 'Sim' : 'Não'}
                    </td>
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
