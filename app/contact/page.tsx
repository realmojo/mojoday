"use client";

import { useState } from "react";
import Link from "next/link";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

const faqs = [
  {
    q: "어떤 유튜브 영상이든 분석할 수 있나요?",
    a: "자막이 있는 여행 관련 유튜브 영상이라면 대부분 분석 가능합니다. 자막이 없는 영상은 AI가 영상을 직접 분석합니다.",
  },
  {
    q: "분석하는 데 얼마나 걸리나요?",
    a: "영상 길이에 따라 다르지만 보통 30초~2분 내외로 완성됩니다.",
  },
  {
    q: "생성된 여행 계획을 수정할 수 있나요?",
    a: "네, 생성된 계획의 모든 항목(날짜, 장소, 활동 등)을 자유롭게 편집할 수 있습니다.",
  },
  {
    q: "무료로 사용할 수 있나요?",
    a: "현재 베타 서비스로 무료로 제공하고 있습니다.",
  },
];

export default function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [sent, setSent] = useState(false);

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    // 실제 전송은 이메일 서비스(Resend, EmailJS 등) 연동 필요
    setSent(true);
  }

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />
      <main className="flex-1">
        {/* Hero */}
        <section className="py-16 text-center border-b">
          <div className="container mx-auto px-4 md:px-6 max-w-2xl space-y-4">
            <h1 className="text-4xl font-bold tracking-tight">Contact</h1>
            <p className="text-muted-foreground text-lg">
              궁금한 점이나 건의사항이 있으시면 언제든지 연락주세요.
            </p>
          </div>
        </section>

        <section className="py-16">
          <div className="container mx-auto px-4 md:px-6 max-w-5xl">
            <div className="grid md:grid-cols-2 gap-12">
              {/* 문의 폼 */}
              <div className="space-y-6">
                <h2 className="text-xl font-bold">문의하기</h2>

                {sent ? (
                  <div className="rounded-2xl border bg-muted/30 p-8 text-center space-y-3">
                    <span className="text-4xl">✅</span>
                    <h3 className="font-bold text-lg">문의가 접수되었습니다</h3>
                    <p className="text-sm text-muted-foreground">
                      빠른 시일 내에 이메일로 답변드리겠습니다.
                    </p>
                    <button
                      onClick={() => { setSent(false); setForm({ name: "", email: "", message: "" }); }}
                      className="text-sm text-primary hover:underline"
                    >
                      다시 문의하기
                    </button>
                  </div>
                ) : (
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-1.5">
                      <label className="text-sm font-medium">이름</label>
                      <input
                        name="name"
                        value={form.name}
                        onChange={handleChange}
                        required
                        placeholder="홍길동"
                        className="w-full rounded-xl border bg-background px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-sm font-medium">이메일</label>
                      <input
                        name="email"
                        type="email"
                        value={form.email}
                        onChange={handleChange}
                        required
                        placeholder="hello@example.com"
                        className="w-full rounded-xl border bg-background px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-sm font-medium">문의 내용</label>
                      <textarea
                        name="message"
                        value={form.message}
                        onChange={handleChange}
                        required
                        rows={5}
                        placeholder="문의 내용을 자유롭게 작성해주세요."
                        className="w-full rounded-xl border bg-background px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                      />
                    </div>
                    <button
                      type="submit"
                      className="w-full bg-primary text-primary-foreground font-medium py-3 rounded-xl hover:bg-primary/90 transition-colors"
                    >
                      문의 보내기
                    </button>
                  </form>
                )}

                <p className="text-xs text-muted-foreground">
                  또는 직접 이메일로 연락주세요:{" "}
                  <a href="mailto:hello@mojoday.app" className="text-primary hover:underline">
                    hello@mojoday.app
                  </a>
                </p>
              </div>

              {/* FAQ */}
              <div className="space-y-6">
                <h2 className="text-xl font-bold">자주 묻는 질문</h2>
                <div className="space-y-4">
                  {faqs.map(({ q, a }) => (
                    <div key={q} className="rounded-xl border p-5 space-y-2">
                      <h3 className="font-medium text-sm">{q}</h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">{a}</p>
                    </div>
                  ))}
                </div>
                <div className="rounded-xl bg-muted/50 p-5 space-y-2">
                  <p className="text-sm font-medium">더 많은 도움이 필요하신가요?</p>
                  <Link href="/about" className="text-sm text-primary hover:underline">
                    Mojoday 소개 보기 →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
