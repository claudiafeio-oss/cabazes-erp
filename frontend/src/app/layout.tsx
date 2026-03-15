import type { ReactNode } from 'react';

import { GlobalNav } from '../components/GlobalNav';

export const metadata = {
  title: 'Cabazes ERP',
  description: 'Backoffice interno',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt">
      <body style={{ margin: 0, background: '#f6f6f6' }}>
        <header
          style={{
            borderBottom: '1px solid #e0e0e0',
            padding: '16px 24px',
            background: '#fff',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: 16,
              flexWrap: 'wrap',
              maxWidth: 1080,
              margin: '0 auto',
              width: '100%',
            }}
          >
            <strong>Cabazes ERP</strong>
            <GlobalNav />
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
