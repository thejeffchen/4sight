import "./tab-bar.css";

interface TabBarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const TABS = [
  { id: "chat", label: "Chat" },
  { id: "diffs", label: "Diffs" },
  { id: "settings", label: "Settings" },
];

export function TabBar({ activeTab, onTabChange }: TabBarProps) {
  return (
    <div className="tab-bar">
      {TABS.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`tab-bar__btn ${activeTab === tab.id ? "tab-bar__btn--active" : ""}`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
