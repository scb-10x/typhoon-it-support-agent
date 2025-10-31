import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono, Pridi, Noto_Sans_Thai } from "next/font/google";
import "./globals.css";
import { UserProvider } from "./contexts/UserContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const pridi = Pridi({
  weight: ["200", "300", "400", "500", "600", "700"],
  subsets: ["latin", "thai"],
  variable: "--font-pridi",
});

const notoSansThai = Noto_Sans_Thai({
  weight: ["300", "400", "500", "600", "700"],
  subsets: ["latin", "thai"],
  variable: "--font-noto-sans-thai",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: "ผู้ช่วย IT Support - Powered by Typhoon AI",
  description: "ระบบช่วยเหลือด้านไอทีอัจฉริยะที่ขับเคลื่อนด้วย Typhoon 2.5 AI รองรับภาษาไทยและภาษาอังกฤษ สำหรับแก้ไขปัญหา IT ต่างๆ",
  keywords: ["IT Support", "Typhoon AI", "Thai AI", "Tech Support", "Help Desk"],
  authors: [{ name: "Typhoon IT Support" }],
  themeColor: "#726bdf", // Typhoon Primary Color
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="th" className="dark scroll-smooth">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${pridi.variable} ${notoSansThai.variable} antialiased`}
      >
        <UserProvider>
          {children}
        </UserProvider>
      </body>
    </html>
  );
}
