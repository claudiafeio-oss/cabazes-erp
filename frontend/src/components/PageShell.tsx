import type { CSSProperties, ReactNode } from 'react';

type PageShellProps = {
  title: string;
  description?: string;
  children: ReactNode;
};

const mainStyle: CSSProperties = {
  fontFamily: 'Arial, sans-serif',
  padding: 24,
  maxWidth: 1080,
  margin: '0 auto',
  width: '100%',
};

const headerStyle: CSSProperties = {
  marginBottom: 24,
};

const cardStyle: CSSProperties = {
  border: '1px solid #ddd',
  borderRadius: 8,
  padding: 16,
  background: '#fff',
};

const gridStyle: CSSProperties = {
  display: 'grid',
  gap: 16,
};

export function PageShell({ title, description, children }: PageShellProps) {
  return (
    <main style={mainStyle}>
      <header style={headerStyle}>
        <h1 style={{ margin: '12px 0 8px' }}>{title}</h1>
        {description ? (
          <p style={{ margin: 0, color: '#555' }}>{description}</p>
        ) : null}
      </header>
      {children}
    </main>
  );
}

type SectionCardProps = {
  title: string;
  children: ReactNode;
};

export function SectionCard({ title, children }: SectionCardProps) {
  return (
    <div style={cardStyle}>
      <strong>{title}</strong>
      <div style={{ marginTop: 8 }}>{children}</div>
    </div>
  );
}

export function SectionGrid({ children }: { children: ReactNode }) {
  return <section style={gridStyle}>{children}</section>;
}
