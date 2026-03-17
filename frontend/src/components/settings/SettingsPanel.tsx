import { useState } from "react";
import { useSettingsStore } from "../../stores/settingsStore";

export function SettingsPanel() {
  const { apiKeyHint, loading, error, saveApiKey } = useSettingsStore();
  const [key, setKey] = useState("");
  const [editing, setEditing] = useState(!apiKeyHint);

  const handleSave = () => {
    const trimmed = key.trim();
    if (!trimmed) return;
    saveApiKey(trimmed).then(() => {
      setKey("");
      setEditing(false);
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSave();
    }
  };

  return (
    <div className="flex flex-col h-full px-6 py-6">
      <h2 className="text-sm font-semibold text-white/90 mb-6">Settings</h2>

      <div className="space-y-6">
        <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5">
          <label className="block text-[13px] font-medium text-white/70 mb-2">
            Anthropic API Key
          </label>
          <p className="text-[12px] text-[#4b4b55] mb-4">
            Get your key from{" "}
            <a
              href="https://console.anthropic.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-400 hover:text-emerald-300 transition-colors"
            >
              console.anthropic.com
            </a>
          </p>

          {editing ? (
            <div className="space-y-4">
              <input
                type="password"
                value={key}
                onChange={(e) => setKey(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="sk-ant-..."
                className="w-full rounded-lg border border-white/[0.08] bg-white/[0.04] px-3.5 py-2.5 text-[13px] text-white/90 placeholder-[#4b4b55]
                           focus:outline-none focus:border-emerald-500/30 transition-colors duration-200"
                autoFocus
              />
              <div className="flex gap-2">
                <button
                  onClick={handleSave}
                  disabled={loading || !key.trim()}
                  className="px-4 py-2 bg-emerald-500 text-white text-[13px] font-medium rounded-lg
                             hover:bg-emerald-400 disabled:opacity-30 disabled:cursor-not-allowed
                             transition-all duration-150"
                >
                  {loading ? "Saving..." : "Save"}
                </button>
                {apiKeyHint && (
                  <button
                    onClick={() => { setEditing(false); setKey(""); }}
                    className="px-4 py-2 text-white/50 text-[13px] rounded-lg border border-white/[0.08]
                               hover:bg-white/[0.04] transition-colors duration-150"
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <span className="text-[13px] font-mono text-white/60 bg-white/[0.04] px-3 py-1.5 rounded-lg border border-white/[0.06]">
                {apiKeyHint}
              </span>
              <button
                onClick={() => setEditing(true)}
                className="text-[12px] text-emerald-400 hover:text-emerald-300 transition-colors"
              >
                Change
              </button>
            </div>
          )}

          {error && (
            <p className="text-xs text-red-400 mt-2">{error}</p>
          )}
        </div>
      </div>
    </div>
  );
}
