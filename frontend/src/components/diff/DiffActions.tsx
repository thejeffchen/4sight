interface DiffActionsProps {
  onAccept: () => void;
  onReject: () => void;
  onRethink?: () => void;
  status: string;
}

export function DiffActions({ onAccept, onReject, onRethink, status }: DiffActionsProps) {
  if (status !== "pending") {
    return (
      <span
        className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${
          status === "accepted"
            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
            : "bg-red-500/10 text-red-400 border border-red-500/20"
        }`}
      >
        {status}
      </span>
    );
  }

  return (
    <div className="flex gap-1.5">
      <button
        onClick={onAccept}
        className="text-[11px] font-medium px-2.5 py-1 rounded-lg bg-emerald-500/15 text-emerald-400 border border-emerald-500/20
                   hover:bg-emerald-500/25 transition-colors duration-150"
      >
        Accept
      </button>
      <button
        onClick={onReject}
        className="text-[11px] font-medium px-2.5 py-1 rounded-lg bg-red-500/10 text-red-400 border border-red-500/20
                   hover:bg-red-500/20 transition-colors duration-150"
      >
        Reject
      </button>
      {onRethink && (
        <button
          onClick={onRethink}
          className="text-[11px] font-medium px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20
                     hover:bg-amber-500/20 transition-colors duration-150"
        >
          Rethink
        </button>
      )}
    </div>
  );
}
