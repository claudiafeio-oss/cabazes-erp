import { apiGet } from '../../lib/api';
import type { Supplier } from '../../lib/types';
import { PageShell, SectionCard, SectionGrid } from '../../components/PageShell';

export default async function SuppliersPage() {
  const suppliersResult = await apiGet<Supplier[]>('/suppliers');
  const suppliers = suppliersResult.data ?? [];

  return (
    <PageShell
      title="Fornecedores"
      description="Gestão de fornecedores e custos."
    >
      <SectionGrid>
        <SectionCard title="Criar fornecedor">
          <p style={{ margin: 0, color: '#555' }}>
            Formulário de criação será adicionado.
          </p>
        </SectionCard>
        <SectionCard title="Lista de fornecedores">
          {suppliersResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{suppliersResult.error}</p>
          ) : suppliers.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>
              Sem fornecedores registados.
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
                {suppliers.map((supplier) => (
                  <tr key={supplier.id}>
                    <td style={{ padding: '6px 0' }}>{supplier.id}</td>
                    <td style={{ padding: '6px 0' }}>{supplier.code}</td>
                    <td style={{ padding: '6px 0' }}>{supplier.name}</td>
                    <td style={{ padding: '6px 0' }}>
                      {supplier.active ? 'Sim' : 'Não'}
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
