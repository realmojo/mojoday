import Link from "next/link";
import { MapPin } from "lucide-react";

export function SiteFooter() {
  return (
    <footer className="border-t bg-muted/50 py-12">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-4">
            <div className="flex items-center gap-2 font-bold text-xl">
              <MapPin className="h-6 w-6 text-primary" />
              <span>Mojoday</span>
            </div>
            <p className="text-sm text-muted-foreground">
              유튜브 영상으로 완성하는 나만의 여행 계획
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-4">여행지</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/#destinations" className="hover:text-primary">
                  인기 여행지
                </Link>
              </li>
              <li>
                <Link href="/#destinations" className="hover:text-primary">
                  일본 여행
                </Link>
              </li>
              <li>
                <Link href="/#destinations" className="hover:text-primary">
                  유럽 여행
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">서비스</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/#how-it-works" className="hover:text-primary">
                  사용 방법
                </Link>
              </li>
              <li>
                <Link href="/#features" className="hover:text-primary">
                  기능 소개
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">정보</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/privacy" className="hover:text-primary">
                  개인정보처리방침
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t pt-8 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} Mojoday. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
