import { create } from "zustand";

const API_BASE = "http://127.0.0.1:8742";

interface SettingsState {
  apiKeyConfigured: boolean | null; // null = loading
  apiKeyHint: string;
  loading: boolean;
  error: string | null;
  checkApiKey: () => Promise<void>;
  saveApiKey: (key: string) => Promise<void>;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  apiKeyConfigured: null,
  apiKeyHint: "",
  loading: false,
  error: null,

  checkApiKey: async () => {
    try {
      const res = await fetch(`${API_BASE}/api/settings/api-key/status`);
      const data = await res.json();
      set({ apiKeyConfigured: data.configured, apiKeyHint: data.hint });
    } catch {
      set({ apiKeyConfigured: false });
    }
  },

  saveApiKey: async (key: string) => {
    set({ loading: true, error: null });
    try {
      const res = await fetch(`${API_BASE}/api/settings/api-key`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: key }),
      });
      const data = await res.json();
      if (data.status === "error") {
        set({ error: data.message, loading: false });
        return;
      }
      set({ apiKeyConfigured: true, apiKeyHint: `sk-ant-...${key.slice(-4)}`, loading: false });
    } catch (e) {
      set({ error: (e as Error).message, loading: false });
    }
  },
}));
