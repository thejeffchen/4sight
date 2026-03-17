import { useEffect, useRef } from "react";
import type { ChatMessage } from "../../stores/chatStore";
import "./chat.css";

interface MessageListProps {
  messages: ChatMessage[];
}

export function MessageList({ messages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const bubbleClass = (msg: ChatMessage) => {
    if (msg.isError) return "message-bubble message-bubble--error";
    if (msg.role === "user") return "message-bubble message-bubble--user";
    return "message-bubble message-bubble--assistant";
  };

  return (
    <div className="message-list">
      {messages.length === 0 && (
        <div className="empty-state">
          <div className="empty-state__icon">
            <div className="empty-state__dot" />
          </div>
          <p className="empty-state__title">Welcome to 4sight</p>
          <p className="empty-state__subtitle">
            Ask me to read or modify your spreadsheet.
          </p>
        </div>
      )}
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`message-row ${msg.role === "user" ? "message-row--user" : "message-row--assistant"}`}
        >
          <div className={bubbleClass(msg)}>
            {msg.attachments && msg.attachments.length > 0 && (
              <div className="attachment-list">
                {msg.attachments.map((att, i) =>
                  att.preview_url ? (
                    <img
                      key={i}
                      src={att.preview_url}
                      alt={att.name}
                      className="attachment-image"
                    />
                  ) : (
                    <div key={i} className="attachment-file">
                      <svg className="w-3.5 h-3.5 opacity-60" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                      </svg>
                      {att.name}
                    </div>
                  )
                )}
              </div>
            )}

            {msg.content && (
              <span className="message-text">{msg.content}</span>
            )}

            {msg.toolCalls && msg.toolCalls.length > 0 && (
              <div className="tool-call-list">
                {msg.toolCalls.map((tc, i) => (
                  <div key={i} className="tool-call">
                    {tc.name}({Object.values(tc.input).join(", ")})
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
