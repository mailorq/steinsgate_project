import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";

export interface SessionUser {
  username: string;
  nickname: string;
  email: string;
  avatarUrl: string | null;
}

interface SessionContextValue {
  user: SessionUser | null;
  isDemo: boolean;
  updateUser: (patch: Partial<SessionUser>) => void;
  logout: () => void;
}

/**
 * TODO(api): заменить демо-пользователя на запрос сессии к django-ninja
 * (GET /api/auth/session) и убрать isDemo
 */
const DEMO_USER: SessionUser = {
  username: "okabe",
  nickname: "Hououin Kyouma",
  email: "okabe@futuregadget.lab",
  avatarUrl: null,
};

const SessionContext = createContext<SessionContextValue | null>(null);

export function SessionProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<SessionUser | null>(DEMO_USER);

  const value: SessionContextValue = {
    user,
    isDemo: true,
    updateUser: (patch) => setUser((current) => (current ? { ...current, ...patch } : current)),
    logout: () => setUser(null),
  };

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function useSession(): SessionContextValue {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error("useSession must be used within SessionProvider");
  }
  return context;
}
