import Link from "next/link";
import Image from "next/image";
import { company } from "@/lib/company";

export function SiteFooter() {
  return (
    <footer className="border-t bg-muted/40">
      <div className="container mx-auto px-4 py-12 md:px-6">
        <div className="mb-10 grid gap-10 md:grid-cols-3">
          {/* 브랜드 */}
          <div className="space-y-4">
            <Link
              href="/"
              className="flex items-center gap-2 text-xl font-bold tracking-tighter"
            >
              <Image
                src="/icon.png"
                alt={`${company.nameEn} 로고`}
                width={28}
                height={28}
                className="rounded-md"
              />
              <span>{company.nameEn}</span>
            </Link>
            <p className="max-w-xs text-sm leading-relaxed text-muted-foreground">
              {company.tagline}
            </p>
          </div>

          {/* 바로가기 */}
          <div>
            <h4 className="mb-4 text-sm font-semibold">바로가기</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/about" className="transition-colors hover:text-foreground">
                  회사 소개
                </Link>
              </li>
              <li>
                <Link href="/services" className="transition-colors hover:text-foreground">
                  서비스
                </Link>
              </li>
              <li>
                <Link href="/contact" className="transition-colors hover:text-foreground">
                  문의하기
                </Link>
              </li>
              <li>
                <Link href="/terms" className="transition-colors hover:text-foreground">
                  이용약관
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="transition-colors hover:text-foreground">
                  개인정보처리방침
                </Link>
              </li>
            </ul>
          </div>

          {/* 회사 정보 */}
          <div>
            <h4 className="mb-4 text-sm font-semibold">회사 정보</h4>
            <ul className="space-y-2 text-sm leading-relaxed text-muted-foreground">
              <li>상호 : {company.name} ({company.nameEn})</li>
              <li>대표 : {company.representative.name}</li>
              <li>
                주소 : {company.address.full} ({company.address.postalCode})
              </li>
              <li>
                전화 :{" "}
                <a
                  href={`tel:${company.phone.tel}`}
                  className="transition-colors hover:text-foreground"
                >
                  {company.phone.display}
                </a>
              </li>
              <li>
                이메일 :{" "}
                <a
                  href={`mailto:${company.email}`}
                  className="transition-colors hover:text-foreground"
                >
                  {company.email}
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="flex flex-col items-center justify-between gap-3 border-t pt-8 text-xs text-muted-foreground sm:flex-row">
          <span>
            © {new Date().getFullYear()} {company.nameEn}. All rights reserved.
          </span>
          <span>{company.address.fullEn}</span>
        </div>
      </div>
    </footer>
  );
}
