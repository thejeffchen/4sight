import { useEffect } from "react";
import { useDiffStore } from "../../stores/diffStore";
import { CellDiffList } from "./CellDiffList";
import { DiffActions } from "./DiffActions";

export function DiffPanel() {
  const { changesets, loadChangesets, acceptChange, rejectChange, acceptChangeset, rejectChangeset } =
    useDiffStore();

  useEffect(() => {
    loadChangesets();
  }, []);

  const pendingChangesets = changesets.filter(
    (cs) => cs.changes.some((c) => c.status === "pending")
  );
  const resolvedChangesets = changesets.filter(
    (cs) => !cs.changes.some((c) => c.status === "pending")
  );

  return (
    <div className="flex flex-col h-full overflow-y-auto px-4 py-5 space-y-5">
      {changesets.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center px-6">
          <div className="w-10 h-10 rounded-full bg-white/[0.04] flex items-center justify-center mb-4 border border-white/[0.06]">
            <svg className="w-4 h-4 text-[#4b4b55]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            </svg>
          </div>
          <p className="text-white/60 text-sm font-medium">No changes yet</p>
          <p className="text-[#4b4b55] text-[13px] mt-1">
            AI changes will appear here for review.
          </p>
        </div>
      )}

      {pendingChangesets.length > 0 && (
        <div>
          <h3 className="text-[11px] font-semibold text-[#6b6b76] uppercase tracking-widest mb-3">
            Pending Review
          </h3>
          <div className="space-y-3">
            {pendingChangesets.map((cs) => (
              <div key={cs.id} className="rounded-xl border border-amber-500/20 bg-amber-500/[0.04] p-3.5">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[13px] text-white/70">
                    {cs.description || `${cs.changes.length} change(s)`}
                  </span>
                  <DiffActions
                    status="pending"
                    onAccept={() => acceptChangeset(cs.id)}
                    onReject={() => rejectChangeset(cs.id)}
                  />
                </div>
                <CellDiffList
                  changes={cs.changes}
                  onAcceptChange={acceptChange}
                  onRejectChange={rejectChange}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {resolvedChangesets.length > 0 && (
        <div>
          <h3 className="text-[11px] font-semibold text-[#6b6b76] uppercase tracking-widest mb-3">
            Resolved
          </h3>
          <div className="space-y-2">
            {resolvedChangesets.map((cs) => (
              <div key={cs.id} className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-3.5 opacity-50">
                <span className="text-[13px] text-white/50">
                  {cs.description || `${cs.changes.length} change(s)`}
                </span>
                <CellDiffList
                  changes={cs.changes}
                  onAcceptChange={acceptChange}
                  onRejectChange={rejectChange}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
