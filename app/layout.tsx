import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Script from "next/script";
import { company } from "@/lib/company";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const siteTitle = `${company.name}(${company.nameEn}) - 웹페이지 디자인 · 디지털 마케팅`;

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || company.website),
  title: {
    default: siteTitle,
    template: `%s | ${company.nameEn}`,
  },
  description: company.description,
  keywords: [
    "모조데이",
    "Mojoday",
    "웹페이지 디자인",
    "웹사이트 제작",
    "홈페이지 제작",
    "랜딩페이지 제작",
    "디지털 마케팅",
    "검색 최적화",
    "SEO 컨설팅",
    "영등포 웹에이전시",
  ],
  authors: [{ name: company.nameEn, url: company.website }],
  creator: company.nameEn,
  publisher: company.nameEn,
  alternates: { canonical: "/" },
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "ko_KR",
    url: "/",
    siteName: company.nameEn,
    title: siteTitle,
    description: company.description,
    images: [
      {
        url: "/logo.png",
        width: 1200,
        height: 630,
        alt: `${company.nameEn} 로고`,
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: siteTitle,
    description: company.description,
    images: ["/logo.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "FNqLbmaC6cPqT60GMc69YeWoyb_qKJucpAtdDYQM-_w",
  },
};

const organizationJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: company.nameEn,
  alternateName: company.name,
  url: company.website,
  logo: `${company.website}/logo.png`,
  description: company.description,
  founder: { "@type": "Person", name: company.representative.nameEn },
  foundingDate: company.founded,
  email: company.email,
  telephone: company.phone.tel,
  address: {
    "@type": "PostalAddress",
    streetAddress: company.address.streetEn,
    addressLocality: company.address.localityEn,
    addressRegion: company.address.regionEn,
    postalCode: company.address.postalCode,
    addressCountry: "KR",
  },
  contactPoint: {
    "@type": "ContactPoint",
    contactType: "customer support",
    telephone: company.phone.tel,
    email: company.email,
    areaServed: "KR",
    availableLanguage: ["Korean", "English"],
  },
  knowsAbout: [company.industry.majorEn, company.industry.subEn],
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
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organizationJsonLd),
          }}
        />
        {children}
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-Z3NNQBGBSD"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-Z3NNQBGBSD');
          `}
        </Script>
      </body>
    </html>
  );
}
