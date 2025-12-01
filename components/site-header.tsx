import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Rocket, Menu } from "lucide-react";

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        <Link
          href="/"
          className="flex items-center gap-2 font-bold text-xl tracking-tighter"
        >
          <Rocket className="h-6 w-6 text-primary" />
          <span>Mojoday</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          <Link
            href="/#services"
            className="transition-colors hover:text-primary"
          >
            Services
          </Link>
          <Link href="/#about" className="transition-colors hover:text-primary">
            About
          </Link>
          <Link
            href="/#contact"
            className="transition-colors hover:text-primary"
          >
            Contact
          </Link>
          <Button asChild size="sm">
            <Link href="/#contact">Get Started</Link>
          </Button>
        </nav>

        {/* Mobile Navigation */}
        <Sheet>
          <SheetTrigger asChild className="md:hidden">
            <Button variant="ghost" size="icon">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="right">
            <nav className="flex flex-col gap-4 mt-8">
              <Link
                href="/#services"
                className="text-lg font-medium hover:text-primary"
              >
                Services
              </Link>
              <Link
                href="/#about"
                className="text-lg font-medium hover:text-primary"
              >
                About
              </Link>
              <Link
                href="/#contact"
                className="text-lg font-medium hover:text-primary"
              >
                Contact
              </Link>
              <Button className="w-full mt-4">Get Started</Button>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
