import { create } from "zustand";
import type { Attachment } from "../lib/websocket";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  attachments?: Attachment[];
  toolCalls?: { name: string; input: Record<string, unknown> }[];
  isError?: boolean;
}

interface ChatState {
  messages: ChatMessage[];
  isStreaming: boolean;
  addUserMessage: (content: string, attachments?: Attachment[]) => void;
  startAssistantMessage: () => void;
  appendToAssistant: (text: string) => void;
  addToolCall: (name: string, input: Record<string, unknown>) => void;
  finishAssistantMessage: () => void;
  errorAssistantMessage: (error: string) => void;
  setStreaming: (streaming: boolean) => void;
}

let msgCounter = 0;

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isStreaming: false,

  addUserMessage: (content, attachments) =>
    set((state) => ({
      messages: [
        ...state.messages,
        { id: `msg-${++msgCounter}`, role: "user", content, attachments },
      ],
    })),

  startAssistantMessage: () =>
    set((state) => ({
      messages: [
        ...state.messages,
        { id: `msg-${++msgCounter}`, role: "assistant", content: "", toolCalls: [] },
      ],
      isStreaming: true,
    })),

  appendToAssistant: (text) =>
    set((state) => {
      const msgs = [...state.messages];
      const last = msgs[msgs.length - 1];
      if (last?.role === "assistant") {
        msgs[msgs.length - 1] = { ...last, content: last.content + text };
      }
      return { messages: msgs };
    }),

  addToolCall: (name, input) =>
    set((state) => {
      const msgs = [...state.messages];
      const last = msgs[msgs.length - 1];
      if (last?.role === "assistant") {
        const toolCalls = [...(last.toolCalls || []), { name, input }];
        msgs[msgs.length - 1] = { ...last, toolCalls };
      }
      return { messages: msgs };
    }),

  finishAssistantMessage: () =>
    set((state) => {
      // Remove empty assistant messages (no content, no tool calls)
      const msgs = [...state.messages];
      const last = msgs[msgs.length - 1];
      if (last?.role === "assistant" && !last.content && (!last.toolCalls || last.toolCalls.length === 0)) {
        msgs.pop();
      }
      return { messages: msgs, isStreaming: false };
    }),

  errorAssistantMessage: (error) =>
    set((state) => {
      const msgs = [...state.messages];
      const last = msgs[msgs.length - 1];
      if (last?.role === "assistant") {
        msgs[msgs.length - 1] = { ...last, content: error, isError: true };
      } else {
        msgs.push({ id: `msg-${++msgCounter}`, role: "assistant", content: error, isError: true });
      }
      return { messages: msgs, isStreaming: false };
    }),

  setStreaming: (streaming) => set({ isStreaming: streaming }),
}));
