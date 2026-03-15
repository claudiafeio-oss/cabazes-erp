import type { CSSProperties } from 'react';

const linkStyle: CSSProperties = {
  textDecoration: 'none',
  color: '#222',
  padding: '6px 10px',
  borderRadius: 6,
  background: '#f2f2f2',
  fontSize: 14,
};

const navStyle: CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: 8,
};

export function GlobalNav() {
  return (
    <nav style={navStyle}>
      <a href="/" style={linkStyle}>
        Dashboard
      </a>
      <a href="/stock" style={linkStyle}>
        Stock
      </a>
      <a href="/purchases" style={linkStyle}>
        Compras
      </a>
      <a href="/receipts" style={linkStyle}>
        Receções
      </a>
      <a href="/assemblies" style={linkStyle}>
        Montagem
      </a>
      <a href="/baskets" style={linkStyle}>
        BOMs
      </a>
      <a href="/products" style={linkStyle}>
        Produtos
      </a>
      <a href="/suppliers" style={linkStyle}>
        Fornecedores
      </a>
      <a href="/locations" style={linkStyle}>
        Localizações
      </a>
    </nav>
  );
}
