import { apiGet } from '../../lib/api';
import type { Product } from '../../lib/types';
import { PageShell, SectionCard, SectionGrid } from '../../components/PageShell';

export default async function ProductsPage() {
  const productsResult = await apiGet<Product[]>('/products');
  const products = productsResult.data ?? [];

  return (
    <PageShell title="Produtos" description="Catálogo e parâmetros de stock.">
      <SectionGrid>
        <SectionCard title="Criar produto">
          <p style={{ margin: 0, color: '#555' }}>
            Formulário de criação será adicionado.
          </p>
        </SectionCard>
        <SectionCard title="Lista de produtos">
          {productsResult.error ? (
            <p style={{ margin: 0, color: '#b00020' }}>{productsResult.error}</p>
          ) : products.length === 0 ? (
            <p style={{ margin: 0, color: '#555' }}>Sem produtos registados.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>SKU</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Nome</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Tipo</th>
                  <th style={{ textAlign: 'left', padding: '6px 0' }}>Ativo</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td style={{ padding: '6px 0' }}>{product.id}</td>
                    <td style={{ padding: '6px 0' }}>{product.sku}</td>
                    <td style={{ padding: '6px 0' }}>{product.name}</td>
                    <td style={{ padding: '6px 0' }}>{product.product_type}</td>
                    <td style={{ padding: '6px 0' }}>
                      {product.active ? 'Sim' : 'Não'}
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
