import Link from "next/link";
import Image from "next/image";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { company } from "@/lib/company";

const navItems = [
  { href: "/about", label: "회사 소개" },
  { href: "/services", label: "서비스" },
  { href: "/contact", label: "문의하기" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
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

        {/* Desktop Navigation */}
        <nav className="hidden items-center gap-8 text-sm font-medium md:flex">
          {navItems.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className="text-muted-foreground transition-colors hover:text-foreground"
            >
              {label}
            </Link>
          ))}
          <Button asChild size="sm">
            <a href={`mailto:${company.email}`}>프로젝트 문의</a>
          </Button>
        </nav>

        {/* Mobile Navigation */}
        <div className="md:hidden">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="h-5 w-5" />
                <span className="sr-only">메뉴 열기</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right">
              <SheetTitle className="sr-only">사이트 메뉴</SheetTitle>
              <nav className="mt-8 flex flex-col gap-4 px-4">
                {navItems.map(({ href, label }) => (
                  <Link
                    key={href}
                    href={href}
                    className="text-lg font-medium hover:text-primary"
                  >
                    {label}
                  </Link>
                ))}
                <Button asChild className="mt-4 w-full">
                  <a href={`mailto:${company.email}`}>프로젝트 문의</a>
                </Button>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
