import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { MapPin, Menu } from "lucide-react";
import { AuthButton } from "@/components/auth-button";

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        <Link
          href="/"
          className="flex items-center gap-2 font-bold text-xl tracking-tighter"
        >
          <MapPin className="h-6 w-6 text-primary" />
          <span>Mojoday</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          <Link
            href="/#destinations"
            className="transition-colors hover:text-primary"
          >
            인기 여행지
          </Link>
          <Link
            href="/#how-it-works"
            className="transition-colors hover:text-primary"
          >
            사용 방법
          </Link>
          <Link
            href="/#features"
            className="transition-colors hover:text-primary"
          >
            기능
          </Link>
          <AuthButton />
        </nav>

        {/* Mobile Navigation */}
        <div className="flex items-center gap-2 md:hidden">
          <AuthButton />
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="h-5 w-5" />
                <span className="sr-only">메뉴 열기</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right">
              <nav className="flex flex-col gap-4 mt-8">
                <Link
                  href="/#destinations"
                  className="text-lg font-medium hover:text-primary"
                >
                  인기 여행지
                </Link>
                <Link
                  href="/#how-it-works"
                  className="text-lg font-medium hover:text-primary"
                >
                  사용 방법
                </Link>
                <Link
                  href="/#features"
                  className="text-lg font-medium hover:text-primary"
                >
                  기능
                </Link>
                <Button asChild className="w-full mt-4">
                  <Link href="/login">로그인</Link>
                </Button>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
