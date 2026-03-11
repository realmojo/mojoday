"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { MapPin } from "lucide-react";
import { createAuthBrowserClient } from "@/lib/supabase-auth";

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState<"google" | "kakao" | null>(null);

  const supabase = createAuthBrowserClient();

  async function handleGoogle() {
    setLoading("google");
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
  }

  async function handleKakao() {
    setLoading("kakao");
    await supabase.auth.signInWithOAuth({
      provider: "kakao",
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background px-4">
      {/* 로고 */}
      <Link href="/" className="flex items-center gap-2 font-bold text-2xl tracking-tighter mb-10">
        <MapPin className="h-7 w-7 text-primary" />
        <span>Mojoday</span>
      </Link>

      {/* 카드 */}
      <div className="w-full max-w-sm rounded-2xl border bg-background shadow-lg p-8 space-y-6">
        <div className="text-center space-y-1">
          <h1 className="text-2xl font-bold">로그인</h1>
          <p className="text-sm text-muted-foreground">
            소셜 계정으로 간편하게 시작하세요
          </p>
        </div>

        <div className="space-y-3">
          {/* 구글 로그인 */}
          <button
            onClick={handleGoogle}
            disabled={loading !== null}
            className="w-full flex items-center justify-center gap-3 rounded-xl border bg-white text-gray-700 font-medium py-3 px-4 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading === "google" ? (
              <span className="h-5 w-5 border-2 border-gray-300 border-t-gray-600 rounded-full animate-spin" />
            ) : (
              <svg className="h-5 w-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
            )}
            Google로 계속하기
          </button>

          {/* 카카오 로그인 */}
          <button
            onClick={handleKakao}
            disabled={loading !== null}
            className="w-full flex items-center justify-center gap-3 rounded-xl font-medium py-3 px-4 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ backgroundColor: "#FEE500", color: "#191919" }}
          >
            {loading === "kakao" ? (
              <span className="h-5 w-5 border-2 border-yellow-600 border-t-yellow-900 rounded-full animate-spin" />
            ) : (
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="#191919">
                <path d="M12 3C6.477 3 2 6.477 2 10.909c0 2.758 1.677 5.19 4.227 6.698l-1.077 3.93c-.094.343.302.617.594.413l4.745-3.128C10.817 18.94 11.404 19 12 19c5.523 0 10-3.477 10-7.773S17.523 3 12 3z" />
              </svg>
            )}
            카카오로 계속하기
          </button>
        </div>

        <p className="text-xs text-center text-muted-foreground">
          로그인 시{" "}
          <span className="underline cursor-pointer">이용약관</span> 및{" "}
          <span className="underline cursor-pointer">개인정보처리방침</span>에
          동의하게 됩니다.
        </p>
      </div>

      <Link href="/" className="mt-6 text-sm text-muted-foreground hover:text-foreground transition-colors">
        ← 홈으로 돌아가기
      </Link>
    </div>
  );
}
