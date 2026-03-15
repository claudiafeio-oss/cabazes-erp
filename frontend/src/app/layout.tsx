import type { ReactNode } from 'react';
import { GlobalNav } from '../components/GlobalNav';
import './globals.css';

export const metadata = {
  title: 'Cabazes ERP',
  description: 'Backoffice interno',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt">
      <body className="bg-gray-100 min-h-screen">
        <header className="bg-white border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between flex-wrap gap-4">
            <strong className="text-gray-900 font-semibold">Cabazes ERP</strong>
            <GlobalNav />
          </div>
        </header>
        <main className="max-w-6xl mx-auto px-6 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
