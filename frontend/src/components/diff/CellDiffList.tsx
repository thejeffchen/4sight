import type { CellChange } from "../../lib/websocket";
import { DiffActions } from "./DiffActions";

interface CellDiffListProps {
  changes: CellChange[];
  onAcceptChange: (id: string) => void;
  onRejectChange: (id: string) => void;
}

function formatValue(value: unknown): string {
  if (value === null || value === undefined) return "(empty)";
  return String(value);
}

export function CellDiffList({ changes, onAcceptChange, onRejectChange }: CellDiffListProps) {
  return (
    <div className="space-y-1.5">
      {changes.map((change) => (
        <div
          key={change.id}
          className={`
            rounded-lg border px-3 py-2.5 text-xs
            ${change.status === "pending"
              ? "border-amber-500/15 bg-amber-500/[0.03]"
              : "border-white/[0.04] bg-white/[0.02]"}
          `}
        >
          <div className="flex items-center justify-between">
            <span className="font-mono font-medium text-white/70 text-[12px]">
              {change.sheet}!{change.cell_ref}
            </span>
            <DiffActions
              status={change.status}
              onAccept={() => onAcceptChange(change.id)}
              onReject={() => onRejectChange(change.id)}
            />
          </div>
          <div className="mt-2 flex items-center gap-2 text-[11px]">
            <span className="text-red-400/80 line-through">
              {change.old_formula || formatValue(change.old_value)}
            </span>
            <svg className="w-3 h-3 text-[#3b3b44] shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
            </svg>
            <span className="text-emerald-400 font-medium">
              {change.new_formula || formatValue(change.new_value)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
