import { create } from "zustand";
import type { Changeset } from "../lib/websocket";
import * as api from "../lib/api";

interface DiffState {
  changesets: Changeset[];
  addChangeset: (cs: Changeset) => void;
  loadChangesets: () => Promise<void>;
  acceptChange: (changeId: string) => Promise<void>;
  rejectChange: (changeId: string) => Promise<void>;
  acceptChangeset: (changesetId: string) => Promise<void>;
  rejectChangeset: (changesetId: string) => Promise<void>;
  updateChangeStatus: (changeId: string, status: "accepted" | "denied") => void;
  updateChangesetStatus: (changesetId: string, status: "accepted" | "denied") => void;
}

export const useDiffStore = create<DiffState>((set, get) => ({
  changesets: [],

  addChangeset: (cs) =>
    set((state) => ({ changesets: [cs, ...state.changesets] })),

  loadChangesets: async () => {
    const data = await api.fetchChangesets();
    set({ changesets: data });
  },

  acceptChange: async (changeId) => {
    await api.acceptChange(changeId);
    get().updateChangeStatus(changeId, "accepted");
  },

  rejectChange: async (changeId) => {
    await api.rejectChange(changeId);
    get().updateChangeStatus(changeId, "denied");
  },

  acceptChangeset: async (changesetId) => {
    await api.acceptChangeset(changesetId);
    get().updateChangesetStatus(changesetId, "accepted");
  },

  rejectChangeset: async (changesetId) => {
    await api.rejectChangeset(changesetId);
    get().updateChangesetStatus(changesetId, "denied");
  },

  updateChangeStatus: (changeId, status) =>
    set((state) => ({
      changesets: state.changesets.map((cs) => ({
        ...cs,
        changes: cs.changes.map((c) =>
          c.id === changeId ? { ...c, status } : c
        ),
      })),
    })),

  updateChangesetStatus: (changesetId, status) =>
    set((state) => ({
      changesets: state.changesets.map((cs) =>
        cs.id === changesetId
          ? {
              ...cs,
              status,
              changes: cs.changes.map((c) => ({
                ...c,
                status: c.status === "pending" ? status : c.status,
              })),
            }
          : cs
      ),
    })),
}));
