import { useChatStore } from "../../stores/chatStore";
import { useBackend } from "../../hooks/useBackend";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";
import type { Attachment } from "../../lib/websocket";
import "./chat.css";

export function ChatPanel() {
  const { messages, isStreaming } = useChatStore();
  const { connected, error, sendMessage } = useBackend();

  const handleSend = (message: string, attachments?: Attachment[]) => {
    sendMessage(message, attachments);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="chat-container flex flex-col flex-1 overflow-hidden">
        {error && (
          <div className="mx-4 mt-3 px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
            {error}
          </div>
        )}
        <MessageList messages={messages} />
        <MessageInput onSend={handleSend} disabled={!connected || isStreaming} />
      </div>
    </div>
  );
}
