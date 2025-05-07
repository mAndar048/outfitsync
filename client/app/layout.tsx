import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import AuthMiddleware from "@/components/AuthMiddleware";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "StyleAgent",
  description: "Your AI Fashion Assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthMiddleware>{children}</AuthMiddleware>
      </body>
    </html>
  );
}
