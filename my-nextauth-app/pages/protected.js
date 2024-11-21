import { SessionProvider } from "next-auth/react"; // Importando o SessionProvider
import './globals.css'; // Importando estilos globais

export const metadata = {
  title: "My NextAuth App",
  description: "Next.js with NextAuth integration",
};

export default function RootLayout({ children }) {
  return (
    // O SessionProvider envolve apenas os componentes do cliente
    <SessionProvider>
      <html lang="en">
        <head>
          <title>{metadata.title}</title>
          <meta name="description" content={metadata.description} />
        </head>
        <body>{children}</body>
      </html>
    </SessionProvider>
  );
}
