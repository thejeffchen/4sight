import { useState } from "react";
import { useSettingsStore } from "../../stores/settingsStore";

export function SetupScreen() {
  const { loading, error, saveApiKey } = useSettingsStore();
  const [key, setKey] = useState("");

  const handleSave = () => {
    const trimmed = key.trim();
    if (!trimmed) return;
    saveApiKey(trimmed);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSave();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full px-10 text-center">
      <div className="w-full max-w-sm space-y-6">
        <div className="space-y-2">
          <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center mx-auto mb-5">
            <div className="w-4 h-4 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.5)]" />
          </div>
          <h1 className="text-lg font-semibold text-white tracking-tight">Welcome to 4sight</h1>
          <p className="text-[13px] text-[#6b6b76] leading-relaxed">
            Enter your Anthropic API key to get started. You can get one from{" "}
            <a
              href="https://console.anthropic.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-400 hover:text-emerald-300 transition-colors"
            >
              console.anthropic.com
            </a>
          </p>
        </div>

        <input
          type="password"
          value={key}
          onChange={(e) => setKey(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="sk-ant-..."
          className="w-full rounded-xl border border-white/[0.08] bg-white/[0.04] px-4 py-3 text-[13px] text-white/90 placeholder-[#4b4b55]
                     focus:outline-none focus:border-emerald-500/30 transition-colors duration-200"
          autoFocus
        />

        <button
          onClick={handleSave}
          disabled={loading || !key.trim()}
          className="w-full px-4 py-3 bg-emerald-500 text-white text-[13px] font-semibold rounded-xl
                     hover:bg-emerald-400 disabled:opacity-30 disabled:cursor-not-allowed
                     transition-all duration-150 active:scale-[0.98]"
        >
          {loading ? "Saving..." : "Get Started"}
        </button>

        {error && (
          <p className="text-xs text-red-400">{error}</p>
        )}
      </div>
    </div>
  );
}
