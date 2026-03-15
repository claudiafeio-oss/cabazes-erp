import { apiGet } from '../lib/api';
import { PageShell, SectionCard, SectionGrid } from '../components/PageShell';

type HealthPayload = {
  status?: string;
};

export default async function Home() {
  const healthResult = await apiGet<HealthPayload>('/health');
  const healthStatus = healthResult.data?.status ?? healthResult.error ?? 'indisponivel';

  return (
    <PageShell title="Cabazes ERP" description="Backoffice interno em construção.">
      <SectionGrid>
        <SectionCard title="Estado da API">
          <p style={{ margin: 0, color: '#555' }}>
            Estado atual: <strong>{healthStatus}</strong>
          </p>
        </SectionCard>
        <SectionCard title="Acessos rápidos">
          <ul style={{ margin: 0, paddingLeft: 18, color: '#555' }}>
            <li>
              <a href="/stock">Stock e movimentos</a>
            </li>
            <li>
              <a href="/purchases">Compras</a>
            </li>
            <li>
              <a href="/receipts">Receções</a>
            </li>
            <li>
              <a href="/assemblies">Montagem</a>
            </li>
          </ul>
        </SectionCard>
      </SectionGrid>
    </PageShell>
  );
}
