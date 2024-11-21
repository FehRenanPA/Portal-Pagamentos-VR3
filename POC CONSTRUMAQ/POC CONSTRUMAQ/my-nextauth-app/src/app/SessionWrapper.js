// src/app/SessionWrapper.js
'use client'; // Defina como 'use client' para que esse seja um Client Component

import { SessionProvider } from 'next-auth/react'; // Importando o SessionProvider

export default function SessionWrapper({ children }) {
  return <SessionProvider>{children}</SessionProvider>;
}
