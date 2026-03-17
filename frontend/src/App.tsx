import { useState, useEffect } from "react";
import { DragHandle } from "./components/overlay/DragHandle";
import { TabBar } from "./components/shared/TabBar";
import { ChatPanel } from "./components/chat/ChatPanel";
import { DiffPanel } from "./components/diff/DiffPanel";
import { SettingsPanel } from "./components/settings/SettingsPanel";
import { SetupScreen } from "./components/settings/SetupScreen";
import { useSettingsStore } from "./stores/settingsStore";

export default function App() {
  const [activeTab, setActiveTab] = useState("chat");
  const { apiKeyConfigured, checkApiKey } = useSettingsStore();

  useEffect(() => {
    checkApiKey();
  }, [checkApiKey]);

  if (apiKeyConfigured === null) {
    return (
      <div className="flex flex-col h-screen bg-[#0a0a0b] rounded-xl overflow-hidden border border-white/[0.06]">
        <DragHandle />
        <div className="flex items-center justify-center h-full">
          <div className="flex items-center gap-2.5 text-[#6b6b76] text-sm">
            <div className="w-4 h-4 border-2 border-emerald-500/40 border-t-emerald-400 rounded-full animate-spin" />
            Connecting...
          </div>
        </div>
      </div>
    );
  }

  if (!apiKeyConfigured) {
    return (
      <div className="flex flex-col h-screen bg-[#0a0a0b] rounded-xl overflow-hidden border border-white/[0.06]">
        <DragHandle />
        <SetupScreen />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-[#0a0a0b] rounded-xl overflow-hidden border border-white/[0.06]">
      <DragHandle />
      <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
      <div className="flex-1 overflow-hidden">
        {activeTab === "chat" && <ChatPanel />}
        {activeTab === "diffs" && <DiffPanel />}
        {activeTab === "settings" && <SettingsPanel />}
      </div>
    </div>
  );
}
