import Link from "next/link";
import Image from "next/image";

export function SiteFooter() {
  return (
    <footer className="border-t bg-muted/50 py-12">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* 브랜드 */}
          <div className="space-y-4">
            <Link href="/" className="flex items-center gap-2 font-bold text-xl tracking-tighter">
              <Image src="/icon.png" alt="Mojoday" width={28} height={28} className="rounded-md" />
              <span>Mojoday</span>
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              유튜브 영상 하나로 완성하는<br />나만의 AI 여행 계획
            </p>
          </div>

          {/* 여행지 */}
          <div>
            <h4 className="font-semibold mb-4 text-sm">여행지</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/#plans" className="hover:text-primary transition-colors">인기 여행 계획</Link></li>
              <li><Link href="/country/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%20(South%20Korea)" className="hover:text-primary transition-colors">국내 여행</Link></li>
              <li><Link href="/#plans" className="hover:text-primary transition-colors">해외 여행</Link></li>
            </ul>
          </div>

          {/* 서비스 */}
          <div>
            <h4 className="font-semibold mb-4 text-sm">서비스</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/about" className="hover:text-primary transition-colors">Mojoday 소개</Link></li>
              <li><Link href="/login" className="hover:text-primary transition-colors">로그인</Link></li>
            </ul>
          </div>

          {/* 정보 */}
          <div>
            <h4 className="font-semibold mb-4 text-sm">정보</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/about" className="hover:text-primary transition-colors">About</Link></li>
              <li><Link href="/contact" className="hover:text-primary transition-colors">Contact</Link></li>
              <li><Link href="/terms" className="hover:text-primary transition-colors">이용약관</Link></li>
              <li><Link href="/privacy" className="hover:text-primary transition-colors">개인정보처리방침</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t pt-8 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-muted-foreground">
          <span>© {new Date().getFullYear()} Mojoday. All rights reserved.</span>
          <div className="flex items-center gap-4">
            <Link href="/terms" className="hover:text-primary transition-colors">이용약관</Link>
            <Link href="/privacy" className="hover:text-primary transition-colors">개인정보처리방침</Link>
            <Link href="/contact" className="hover:text-primary transition-colors">문의하기</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
