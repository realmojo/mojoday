import { createBrowserClient } from "@supabase/ssr";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

// 브라우저(클라이언트 컴포넌트)에서 Auth 사용
export function createAuthBrowserClient() {
  return createBrowserClient(supabaseUrl, supabaseAnonKey);
}
