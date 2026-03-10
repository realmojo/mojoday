import type { Metadata } from "next";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description:
    "Mojoday's Privacy Policy. Learn how we collect, use, and protect your personal data when you visit our website.",
  openGraph: {
    title: "Privacy Policy | Mojoday",
    description:
      "Learn how Mojoday collects, uses, and protects your personal data.",
    url: "/privacy",
  },
  alternates: {
    canonical: "/privacy",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function PrivacyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />

      <main className="flex-1 py-12 md:py-24">
        <div className="container mx-auto px-4 md:px-6 max-w-4xl">
          <div className="space-y-6">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Privacy Policy
            </h1>
            <p className="text-muted-foreground">
              Last updated: {new Date().toLocaleDateString()}
            </p>

            <div className="prose prose-gray dark:prose-invert max-w-none space-y-8">
              <section>
                <h2 className="text-2xl font-semibold mb-4">1. Introduction</h2>
                <p className="text-muted-foreground leading-relaxed">
                  Welcome to Mojoday ("we," "our," or "us"). We respect your
                  privacy and are committed to protecting your personal data.
                  This Privacy Policy explains how we collect, use, disclose,
                  and safeguard your information when you visit our website
                  mojoday.app (the "Service"). Please read this privacy policy
                  carefully to understand our views and practices regarding your
                  personal data and how we will treat it.
                </p>
                <p className="text-muted-foreground leading-relaxed mt-4">
                  By using our Service, you agree to the collection and use of
                  information in accordance with this policy. If you do not
                  agree with our policies and practices, do not use our Service.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  2. Information We Collect
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We collect several types of information from and about users
                  of our Service:
                </p>

                <h3 className="text-xl font-semibold mb-3 mt-6">
                  2.1 Automatically Collected Information
                </h3>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  When you visit our Service, we automatically collect certain
                  information about your device and how you interact with our
                  Service, including:
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground mb-4">
                  <li>
                    <strong>Device Information:</strong> IP address, device
                    type, operating system, browser type and version, device
                    identifiers (including mobile advertising IDs such as Google
                    Advertising ID or Apple ID for Advertising), screen
                    resolution, language preferences
                  </li>
                  <li>
                    <strong>Usage Information:</strong> Pages visited, time
                    spent on pages, click patterns, referring website addresses,
                    search queries, date and time of visits
                  </li>
                  <li>
                    <strong>Location Information:</strong> General location data
                    (country, region, city) derived from your IP address
                  </li>
                  <li>
                    <strong>Technical Information:</strong> Browser plug-in
                    types and versions, time zone setting, platform information
                  </li>
                </ul>

                <h3 className="text-xl font-semibold mb-3 mt-6">
                  2.2 Information You Provide
                </h3>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We may collect information that you voluntarily provide to us,
                  including:
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>
                    Name, email address, and contact information when you
                    contact us
                  </li>
                  <li>
                    Information you provide when filling out forms on our
                    Service
                  </li>
                  <li>Any other information you choose to provide</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  3. How We Use Your Information
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We use the information we collect for the following purposes:
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>
                    <strong>To Provide and Maintain Our Service:</strong> To
                    operate, maintain, and improve our Service and user
                    experience
                  </li>
                  <li>
                    <strong>To Display Advertisements:</strong> To show you
                    relevant advertisements through Google AdSense and other
                    advertising partners. This includes personalized ads based
                    on your interests and browsing behavior
                  </li>
                  <li>
                    <strong>To Analyze Usage:</strong> To understand how users
                    interact with our Service, analyze trends, and gather
                    demographic information
                  </li>
                  <li>
                    <strong>To Communicate:</strong> To respond to your
                    inquiries, provide customer support, and send you important
                    updates about our Service
                  </li>
                  <li>
                    <strong>To Ensure Security:</strong> To detect, prevent, and
                    address technical issues, fraud, and security threats
                  </li>
                  <li>
                    <strong>To Comply with Legal Obligations:</strong> To comply
                    with applicable laws, regulations, and legal processes
                  </li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  4. Third-Party Services and Data Sharing
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We share your information with third-party service providers
                  who perform services on our behalf. These third parties are
                  contractually obligated to protect your information and use it
                  only for the purposes we specify:
                </p>

                <h3 className="text-xl font-semibold mb-3 mt-6">
                  4.1 Google AdSense
                </h3>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We use Google AdSense to display advertisements on our
                  Service. Google AdSense uses cookies and similar technologies
                  to serve ads based on your prior visits to our Service and
                  other websites. Google's use of advertising cookies enables it
                  and its partners to serve ads to you based on your visit to
                  our Service and/or other sites on the Internet.
                </p>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  <strong>Publisher IDs:</strong> pub-9130836798889522,
                  pub-1963334904140891
                </p>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  You may opt out of personalized advertising by visiting{" "}
                  <a
                    href="https://www.google.com/settings/ads"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary underline"
                  >
                    Google's Ads Settings
                  </a>
                  . You can also opt out of some third-party vendors' uses of
                  cookies for personalized advertising by visiting{" "}
                  <a
                    href="https://www.aboutads.info/choices/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary underline"
                  >
                    www.aboutads.info
                  </a>
                  .
                </p>

                <h3 className="text-xl font-semibold mb-3 mt-6">
                  4.2 Google Analytics
                </h3>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We use Google Analytics to analyze how users interact with our
                  Service. Google Analytics collects information such as how
                  often users visit our Service, what pages they visit, and what
                  other sites they used prior to coming to our Service. We use
                  the information we get from Google Analytics to improve our
                  Service.
                </p>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  <strong>Analytics ID:</strong> G-Z3NNQBGBSD
                </p>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  You can opt out of Google Analytics by installing the{" "}
                  <a
                    href="https://tools.google.com/dlpage/gaoptout"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary underline"
                  >
                    Google Analytics Opt-out Browser Add-on
                  </a>
                  .
                </p>

                <h3 className="text-xl font-semibold mb-3 mt-6">
                  4.3 Other Third Parties
                </h3>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We may also share your information:
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>
                    With service providers who assist us in operating our
                    Service
                  </li>
                  <li>When required by law or to respond to legal process</li>
                  <li>To protect our rights, privacy, safety, or property</li>
                  <li>
                    In connection with a merger, acquisition, or sale of assets
                  </li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  5. Cookies and Tracking Technologies
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  We use cookies, web beacons, and similar tracking technologies
                  to collect and store information about your preferences and
                  activity on our Service. Cookies are small data files stored
                  on your device that help us improve your experience.
                </p>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  <strong>Types of cookies we use:</strong>
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>
                    <strong>Essential Cookies:</strong> Required for the Service
                    to function properly
                  </li>
                  <li>
                    <strong>Analytics Cookies:</strong> Help us understand how
                    visitors use our Service
                  </li>
                  <li>
                    <strong>Advertising Cookies:</strong> Used to deliver
                    relevant advertisements and track ad performance
                  </li>
                  <li>
                    <strong>Functional Cookies:</strong> Remember your
                    preferences and settings
                  </li>
                </ul>
                <p className="text-muted-foreground leading-relaxed mt-4">
                  You can control cookies through your browser settings.
                  However, disabling cookies may limit your ability to use
                  certain features of our Service.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  6. Data Retention
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  We retain your personal information for as long as necessary
                  to fulfill the purposes outlined in this Privacy Policy,
                  unless a longer retention period is required or permitted by
                  law. When we no longer need your personal information, we will
                  securely delete or anonymize it.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  7. Your Privacy Rights
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  Depending on your location, you may have certain rights
                  regarding your personal information:
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>
                    <strong>Access:</strong> Request access to your personal
                    information
                  </li>
                  <li>
                    <strong>Correction:</strong> Request correction of
                    inaccurate information
                  </li>
                  <li>
                    <strong>Deletion:</strong> Request deletion of your personal
                    information
                  </li>
                  <li>
                    <strong>Opt-Out:</strong> Opt out of the sale or sharing of
                    your personal information (where applicable)
                  </li>
                  <li>
                    <strong>Data Portability:</strong> Request a copy of your
                    personal information in a portable format
                  </li>
                  <li>
                    <strong>Object to Processing:</strong> Object to certain
                    types of processing of your personal information
                  </li>
                </ul>
                <p className="text-muted-foreground leading-relaxed mt-4">
                  To exercise these rights, please contact us at
                  help@mojoday.app. We will respond to your request within a
                  reasonable timeframe and in accordance with applicable law.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  8. Children's Privacy
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  Our Service is not intended for children under the age of 13
                  (or 16 in the European Economic Area). We do not knowingly
                  collect personal information from children. If you are a
                  parent or guardian and believe your child has provided us with
                  personal information, please contact us immediately. If we
                  become aware that we have collected personal information from
                  a child without parental consent, we will take steps to delete
                  that information.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  9. International Data Transfers
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  Your information may be transferred to and processed in
                  countries other than your country of residence. These
                  countries may have data protection laws that differ from those
                  in your country. By using our Service, you consent to the
                  transfer of your information to these countries. We take
                  appropriate safeguards to ensure your information is protected
                  in accordance with this Privacy Policy.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  10. Data Security
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  We implement appropriate technical and organizational security
                  measures to protect your personal information against
                  unauthorized access, alteration, disclosure, or destruction.
                  However, no method of transmission over the Internet or
                  electronic storage is 100% secure. While we strive to use
                  commercially acceptable means to protect your information, we
                  cannot guarantee absolute security.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  11. Changes to This Privacy Policy
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  We may update this Privacy Policy from time to time. We will
                  notify you of any changes by posting the new Privacy Policy on
                  this page and updating the "Last updated" date. You are
                  advised to review this Privacy Policy periodically for any
                  changes. Changes to this Privacy Policy are effective when
                  they are posted on this page.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  12. California Privacy Rights
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  If you are a California resident, you have additional rights
                  under the California Consumer Privacy Act (CCPA):
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>
                    Right to know what personal information is collected, used,
                    and shared
                  </li>
                  <li>Right to delete personal information</li>
                  <li>Right to opt-out of the sale of personal information</li>
                  <li>
                    Right to non-discrimination for exercising your privacy
                    rights
                  </li>
                </ul>
                <p className="text-muted-foreground leading-relaxed mt-4">
                  We do not sell personal information. However, we may share
                  information with advertising partners as described in this
                  policy. You can opt out of personalized advertising as
                  described in Section 4.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">
                  13. European Privacy Rights (GDPR)
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  If you are located in the European Economic Area (EEA), you
                  have certain rights under the General Data Protection
                  Regulation (GDPR):
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>Right of access to your personal data</li>
                  <li>Right to rectification of inaccurate data</li>
                  <li>Right to erasure ("right to be forgotten")</li>
                  <li>Right to restrict processing</li>
                  <li>Right to data portability</li>
                  <li>Right to object to processing</li>
                  <li>Right to withdraw consent</li>
                </ul>
                <p className="text-muted-foreground leading-relaxed mt-4">
                  Our legal basis for processing your personal data includes:
                  (1) your consent, (2) performance of a contract, (3)
                  compliance with legal obligations, (4) protection of vital
                  interests, (5) public interest, and (6) legitimate interests.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-semibold mb-4">14. Contact Us</h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  If you have any questions, concerns, or requests regarding
                  this Privacy Policy or our privacy practices, please contact
                  us:
                </p>
                <div className="mt-4 p-4 bg-muted rounded-lg">
                  <p className="font-medium mb-2">Mojoday</p>
                  <p className="text-muted-foreground">
                    Email:{" "}
                    <a
                      href="mailto:help@mojoday.app"
                      className="text-primary underline"
                    >
                      help@mojoday.app
                    </a>
                  </p>
                  <p className="text-muted-foreground mt-2">
                    Website:{" "}
                    <a
                      href="https://mojoday.app"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary underline"
                    >
                      https://mojoday.app
                    </a>
                  </p>
                </div>
              </section>
            </div>
          </div>
        </div>
      </main>

      <SiteFooter />
    </div>
  );
}
