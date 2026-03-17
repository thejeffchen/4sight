import { useEffect, useRef, useCallback, useState } from "react";
import { BackendSocket } from "../lib/websocket";
import type { Attachment } from "../lib/websocket";
import { useChatStore } from "../stores/chatStore";
import { useDiffStore } from "../stores/diffStore";

export function useBackend() {
  const socketRef = useRef<BackendSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { addUserMessage, startAssistantMessage, appendToAssistant, addToolCall, finishAssistantMessage, errorAssistantMessage } =
    useChatStore();
  const { addChangeset } = useDiffStore();

  useEffect(() => {
    const socket = new BackendSocket();
    socketRef.current = socket;

    socket.connect().then(() => {
      setConnected(true);
      setError(null);
    }).catch((e) => {
      setError(e.message);
    });

    socket.onEvent((event) => {
      switch (event.type) {
        case "text_delta":
          appendToAssistant(event.text);
          break;
        case "tool_call":
          addToolCall(event.name, event.input);
          break;
        case "changeset":
          addChangeset(event.changeset);
          break;
        case "done":
          finishAssistantMessage();
          break;
        case "error":
          setError(event.message);
          errorAssistantMessage(event.message);
          break;
      }
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const sendMessage = useCallback(
    (message: string, attachments?: Attachment[]) => {
      if (!socketRef.current?.connected) return;
      addUserMessage(message, attachments);
      startAssistantMessage();
      socketRef.current.send(message, attachments);
    },
    [addUserMessage, startAssistantMessage]
  );

  return { connected, error, sendMessage };
}
