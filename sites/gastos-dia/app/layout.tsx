import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Dia a dia · Gastos",
  description: "Suas compras acompanhadas, uma semana por vez.",
  appleWebApp: { capable: true, title: 'Dia a dia', statusBarStyle: 'default' },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">{children}</body>
    </html>
  );
}
