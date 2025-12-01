import Link from "next/link";
import { Rocket } from "lucide-react";

export function SiteFooter() {
  return (
    <footer className="border-t bg-muted/50 py-12">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-4">
            <div className="flex items-center gap-2 font-bold text-xl">
              <Rocket className="h-6 w-6 text-primary" />
              <span>Mojoday</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Building the future of the web, one pixel at a time.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Services</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/#services" className="hover:text-primary">
                  Web Development
                </Link>
              </li>
              <li>
                <Link href="/#services" className="hover:text-primary">
                  UI/UX Design
                </Link>
              </li>
              <li>
                <Link href="/#services" className="hover:text-primary">
                  Marketing
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/#about" className="hover:text-primary">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/#contact" className="hover:text-primary">
                  Contact
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="hover:text-primary">
                  Privacy Policy
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
