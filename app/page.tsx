import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Code,
  Megaphone,
  Palette,
  Rocket,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative py-20 md:py-32 overflow-hidden">
          <div className="absolute inset-0 -z-10 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]"></div>
          <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary/20 opacity-20 blur-[100px]"></div>

          <div className="container mx-auto px-4 md:px-6 flex flex-col items-center text-center space-y-8">
            <Badge
              variant="secondary"
              className="px-4 py-1.5 text-sm rounded-full"
            >
              Innovation in Every Pixel
            </Badge>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight max-w-4xl bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">
              We Build, Create, and Market{" "}
              <span className="text-primary">Digital Experiences</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl leading-relaxed">
              Mojoday is your all-in-one partner for web application
              development, creative design, and strategic marketing. We turn
              ideas into reality.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
              <Button size="lg" className="h-12 px-8 text-base">
                Start Your Project <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="h-12 px-8 text-base"
              >
                View Our Work
              </Button>
            </div>

            {/* Tech Stack Preview */}
            <div className="pt-12 flex items-center justify-center gap-8 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
              {/* Simple text representation for logos for now */}
              <span className="font-bold text-xl">Next.js</span>
              <span className="font-bold text-xl">React</span>
              <span className="font-bold text-xl">Tailwind</span>
              <span className="font-bold text-xl">TypeScript</span>
            </div>
          </div>
        </section>

        {/* Services Section */}
        <section id="services" className="py-20 bg-muted/30">
          <div className="container mx-auto px-4 md:px-6">
            <div className="text-center mb-16 space-y-4">
              <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
                Our Expertise
              </h2>
              <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
                Comprehensive solutions tailored to elevate your business in the
                digital landscape.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              <Card className="bg-background border-none shadow-lg hover:shadow-xl transition-all duration-300">
                <CardHeader>
                  <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                    <Code className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-xl">Web Development</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    Custom web applications built with modern technologies like
                    Next.js and React. Fast, secure, and scalable.
                  </CardDescription>
                  <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" />{" "}
                      Full-Stack Development
                    </li>
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" />{" "}
                      E-commerce Solutions
                    </li>
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" /> API
                      Integration
                    </li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-background border-none shadow-lg hover:shadow-xl transition-all duration-300">
                <CardHeader>
                  <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                    <Palette className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-xl">UI/UX Design</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    Beautiful, intuitive designs that engage users. We focus on
                    user experience to drive conversion and retention.
                  </CardDescription>
                  <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" />{" "}
                      User Interface Design
                    </li>
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" />{" "}
                      User Experience Research
                    </li>
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" />{" "}
                      Brand Identity
                    </li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="bg-background border-none shadow-lg hover:shadow-xl transition-all duration-300">
                <CardHeader>
                  <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                    <Megaphone className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-xl">Digital Marketing</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    Data-driven marketing strategies to grow your audience. We
                    help you reach the right people at the right time.
                  </CardDescription>
                  <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" /> SEO
                      Optimization
                    </li>
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" />{" "}
                      Social Media Marketing
                    </li>
                    <li className="flex items-center">
                      <CheckCircle2 className="h-4 w-4 mr-2 text-primary" />{" "}
                      Content Strategy
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section id="about" className="py-20">
          <div className="container mx-auto px-4 md:px-6">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="space-y-6">
                <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
                  Why Choose Mojoday?
                </h2>
                <p className="text-muted-foreground text-lg leading-relaxed">
                  At Mojoday, we believe in the power of technology to transform
                  businesses. We are not just developers and designers; we are
                  your strategic partners.
                </p>
                <div className="grid grid-cols-2 gap-6">
                  <div className="p-4 rounded-lg bg-muted/50">
                    <h3 className="font-bold text-2xl text-primary mb-2">
                      50+
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Projects Delivered
                    </p>
                  </div>
                  <div className="p-4 rounded-lg bg-muted/50">
                    <h3 className="font-bold text-2xl text-primary mb-2">
                      98%
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Client Satisfaction
                    </p>
                  </div>
                  <div className="p-4 rounded-lg bg-muted/50">
                    <h3 className="font-bold text-2xl text-primary mb-2">
                      24/7
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Support & Maintenance
                    </p>
                  </div>
                  <div className="p-4 rounded-lg bg-muted/50">
                    <h3 className="font-bold text-2xl text-primary mb-2">5+</h3>
                    <p className="text-sm text-muted-foreground">
                      Years Experience
                    </p>
                  </div>
                </div>
              </div>
              <div className="relative h-[400px] rounded-2xl overflow-hidden bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center border">
                <div className="absolute inset-0 bg-grid-white/10 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]"></div>
                <Rocket className="h-32 w-32 text-primary animate-pulse" />
              </div>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="py-20">
          <div className="container mx-auto px-4 md:px-6">
            <div className="max-w-2xl mx-auto text-center mb-12">
              <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">
                Let's Work Together
              </h2>
              <p className="text-muted-foreground text-lg">
                Ready to start your next project? Send us a message and we'll
                get back to you within 24 hours.
              </p>
            </div>

            <Card className="max-w-xl mx-auto shadow-lg">
              <CardContent className="p-6 md:p-8 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label htmlFor="name" className="text-sm font-medium">
                      Name
                    </label>
                    <Input id="name" placeholder="John Doe" />
                  </div>
                  <div className="space-y-2">
                    <label htmlFor="email" className="text-sm font-medium">
                      Email
                    </label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="john@example.com"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <label htmlFor="subject" className="text-sm font-medium">
                    Subject
                  </label>
                  <Input id="subject" placeholder="Project Inquiry" />
                </div>
                <div className="space-y-2">
                  <label htmlFor="message" className="text-sm font-medium">
                    Message
                  </label>
                  <Textarea
                    id="message"
                    placeholder="Tell us about your project..."
                    className="min-h-[120px]"
                  />
                </div>
                <Button className="w-full size-lg text-base">
                  Send Message
                </Button>
              </CardContent>
            </Card>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}
