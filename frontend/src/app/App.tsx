import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { Layout } from "@/app/Layout";
import { AnimePage } from "@/pages/AnimePage";
import { AuthStubPage } from "@/pages/AuthStubPage";
import { LabPage } from "@/pages/LabPage";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/steins-gate" replace />} />
          <Route path="/future-gadget-laboratory" element={<LabPage />} />
          <Route path="/register" element={<AuthStubPage />} />
          <Route path="/profile" element={<AuthStubPage />} />
          <Route path="/:slug" element={<AnimePage />} />
          <Route path="*" element={<Navigate to="/steins-gate" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
