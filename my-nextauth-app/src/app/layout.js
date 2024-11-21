// src/app/layout.js
import './globals.css'; // Seu arquivo de estilo global
import SessionWrapper from './SessionWrapper'; // Importando o SessionWrapper

// Definindo os metadados da página, como título e descrição
export const metadata = {
  title: 'Meu Aplicativo Next.js',
  description: 'Aplicativo de exemplo usando Next.js e NextAuth',
};

export default function Layout({ children }) {
  return (
    <html lang="pt-br"> {/* A tag <html> deve ser definida no Root Layout */}
      <body> {/* A tag <body> deve envolver o conteúdo da página */}
        <SessionWrapper> {/* Envolvendo os filhos com o SessionProvider */}
          {children} {/* Aqui é onde o conteúdo da página será renderizado */}
        </SessionWrapper>
      </body>
    </html>
  );
}
