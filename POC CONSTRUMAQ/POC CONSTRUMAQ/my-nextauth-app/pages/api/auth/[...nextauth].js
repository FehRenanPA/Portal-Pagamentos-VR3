import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";  // Provedor para credenciais personalizadas

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // Verifique as credenciais pré-cadastradas diretamente no código
        const users = [
          { email: "user@example.com", password: "password123" },
          { email: "admin@example.com", password: "admin123" }
        ];

        const user = users.find(
          (user) => user.email === credentials.email && user.password === credentials.password
        );

        if (user) {
          return { email: user.email }; // Retorne os dados do usuário se encontrado
        } else {
          return null; // Se não encontrar o usuário, retorna null (erro de login)
        }
      },
    }),
  ],
  pages: {
    signIn: "/auth/signin", // Página personalizada de login (opcional)
  },
  session: {
    strategy: "jwt", // Usar JWT para gerenciar a sessão
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.email = user.email; // Armazena o e-mail no JWT
      }
      return token;
    },
    async session({ session, token }) {
      session.user.email = token.email; // Passa o e-mail para a sessão
      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET, // Configure a chave secreta no seu .env
};

export default NextAuth(authOptions);
