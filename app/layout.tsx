import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Script from "next/script";
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
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL || "https://mojoday.app"
  ),
  title: {
    default: "Mojoday - 유튜브로 완성하는 AI 여행 플래너",
    template: "%s | Mojoday",
  },
  description:
    "좋아하는 여행 유튜버의 영상 URL 하나로 일정, 맛집, 숙소, 교통까지 완벽한 여행 계획을 자동으로 만들어드립니다.",
  keywords: [
    "여행 계획",
    "AI 여행 플래너",
    "유튜브 여행",
    "여행 일정",
    "여행지 추천",
    "맛집 추천",
    "자동 여행 계획",
    "도쿄 여행",
    "오사카 여행",
    "파리 여행",
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
    title: "Mojoday - 유튜브로 완성하는 AI 여행 플래너",
    description:
      "좋아하는 여행 유튜버의 영상 URL 하나로 일정, 맛집, 숙소, 교통까지 완벽한 여행 계획을 자동으로 만들어드립니다.",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Mojoday - AI 여행 플래너",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Mojoday - 유튜브로 완성하는 AI 여행 플래너",
    description:
      "좋아하는 여행 유튜버의 영상 URL 하나로 일정, 맛집, 숙소, 교통까지 완벽한 여행 계획을 자동으로 만들어드립니다.",
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
    google: "FNqLbmaC6cPqT60GMc69YeWoyb_qKJucpAtdDYQM-_w",
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
      <head>
        <meta
          name="naver-site-verification"
          content="b0d055f904024ccff65bdfea8bd247cfc47f477e"
        />
        <meta
          name="google-site-verification"
          content="FNqLbmaC6cPqT60GMc69YeWoyb_qKJucpAtdDYQM-_w"
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <script
          src="https://www.googletagmanager.com/gtag/js?id=G-Z3NNQBGBSD"
          async
        />
        <script
          id="google-analytics"
          async
          dangerouslySetInnerHTML={{
            __html: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-Z3NNQBGBSD');
        `,
          }}
        />
        {children}
      </body>
    </html>
  );
}
