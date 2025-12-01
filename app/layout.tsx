import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "https://mojoday.app"),
  title: {
    default: "Mojoday - Digital Experiences That Transform Businesses",
    template: "%s | Mojoday",
  },
  description:
    "Mojoday is your all-in-one partner for web application development, creative design, and strategic marketing. We build, create, and market digital experiences that turn ideas into reality.",
  keywords: [
    "web development",
    "web design",
    "UI/UX design",
    "digital marketing",
    "Next.js development",
    "React development",
    "e-commerce solutions",
    "SEO optimization",
    "brand identity",
    "full-stack development",
  ],
  authors: [{ name: "Mojoday" }],
  creator: "Mojoday",
  publisher: "Mojoday",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "/",
    siteName: "Mojoday",
    title: "Mojoday - Digital Experiences That Transform Businesses",
    description:
      "We build, create, and market digital experiences. Your all-in-one partner for web development, design, and marketing.",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Mojoday - Digital Experiences",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Mojoday - Digital Experiences That Transform Businesses",
    description:
      "We build, create, and market digital experiences. Your all-in-one partner for web development, design, and marketing.",
    images: ["/og-image.jpg"],
    creator: "@mojoday",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    // Add your verification codes here when available
    // google: "your-google-verification-code",
    // yandex: "your-yandex-verification-code",
    // bing: "your-bing-verification-code",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
