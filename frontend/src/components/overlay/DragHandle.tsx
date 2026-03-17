import { useEffect, useRef, useState } from "react";
import type { Window } from "@tauri-apps/api/window";
import "./drag-handle.css";

const isTauri = "__TAURI_INTERNALS__" in window;

export function DragHandle() {
  const dragRef = useRef<HTMLDivElement>(null);
  const [appWindow, setAppWindow] = useState<Window | null>(null);

  useEffect(() => {
    if (!isTauri) return;
    import("@tauri-apps/api/window").then((mod) => {
      setAppWindow(mod.getCurrentWindow());
    });
  }, []);

  useEffect(() => {
    const el = dragRef.current;
    if (!el || !appWindow) return;

    const onMouseDown = (e: MouseEvent) => {
      if ((e.target as HTMLElement).closest("button")) return;
      appWindow.startDragging();
    };

    el.addEventListener("mousedown", onMouseDown);
    return () => el.removeEventListener("mousedown", onMouseDown);
  }, [appWindow]);

  return (
    <div ref={dragRef} className="drag-handle">
      <div className="drag-handle__brand">
        <div className="drag-handle__dot" />
        <span className="drag-handle__title">4sight</span>
      </div>
      {isTauri && (
        <div className="drag-handle__controls">
          <button
            onClick={() => appWindow?.minimize()}
            className="drag-handle__btn drag-handle__btn--minimize"
            aria-label="Minimize"
          />
          <button
            onClick={() => appWindow?.close()}
            className="drag-handle__btn drag-handle__btn--close"
            aria-label="Close"
          />
        </div>
      )}
    </div>
  );
}
