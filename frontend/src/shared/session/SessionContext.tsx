import { createContext, useContext } from "react";
import type { ReactNode } from "react";

import { useQuery, useQueryClient } from "@tanstack/react-query";

import { authApi } from "@/shared/api";
import type { UserOut } from "@/shared/api";

export const SESSION_QUERY_KEY = ["session"];

interface SessionContextValue {
  user: UserOut | null;
  isLoading: boolean;
  setUser: (user: UserOut | null) => void;
}

const SessionContext = createContext<SessionContextValue | null>(null);

export function SessionProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: SESSION_QUERY_KEY,
    queryFn: authApi.session,
    staleTime: 5 * 60 * 1000,
    retry: false,
  });

  const value: SessionContextValue = {
    user: data?.user ?? null,
    isLoading,
    setUser: (user) => queryClient.setQueryData(SESSION_QUERY_KEY, { user }),
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
