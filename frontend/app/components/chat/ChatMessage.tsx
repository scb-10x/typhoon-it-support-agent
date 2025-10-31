/**
 * Individual chat message component
 */

import { Message } from "./types";
import { MarkdownRenderer } from "./MarkdownRenderer";

interface ChatMessageProps {
  message: Message;
  index: number;
}

export const ChatMessage = ({ message, index }: ChatMessageProps) => {
  return (
    <div
      className={`flex animate-in fade-in slide-in-from-bottom-4 duration-500 ${
        message.role === "user" ? "justify-end" : "justify-start"
      }`}
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <div
        className={`flex max-w-[90%] sm:max-w-[85%] gap-2 sm:gap-3 ${
          message.role === "user" ? "flex-row-reverse" : "flex-row"
        }`}
      >
        <div
          className={`flex h-8 w-8 sm:h-9 sm:w-9 shrink-0 items-center justify-center rounded-xl ${
            message.role === "user"
              ? "bg-gradient-to-br from-cerulean to-cerulean-dark ring-2 ring-cerulean/20"
              : "bg-gradient-to-br from-typhoon-primary to-lavender ring-2 ring-lavender/20"
          } text-white shadow-lg`}
        >
          {message.role === "user" ? (
            <svg
              className="h-4 w-4 sm:h-5 sm:w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          ) : (
            <svg
              className="h-4 w-4 sm:h-5 sm:w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          )}
        </div>
        <div
          className={`rounded-2xl px-4 py-3 sm:px-5 sm:py-3.5 shadow-md ${
            message.role === "user"
              ? "bg-gradient-to-br from-cerulean to-cerulean-dark text-white ring-1 ring-white/20"
              : "bg-typhoon-darker/80 text-white ring-1 ring-rhythm"
          }`}
        >
          {message.role === "user" ? (
            <p className="whitespace-pre-wrap text-sm leading-relaxed font-[var(--font-pridi)]">
              {message.content}
            </p>
          ) : (
            <div className="markdown-content max-w-none">
              {!message.content && message.isStreaming ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="relative flex h-5 w-5">
                      <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-lavender opacity-75"></span>
                      <span className="relative inline-flex h-5 w-5 rounded-full bg-typhoon-primary"></span>
                    </div>
                    <span className="text-sm text-gray-300">
                      {message.currentEvent || "กำลังประมวลผล..."}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <div className="h-2 w-2 animate-bounce rounded-full bg-typhoon-primary" style={{ animationDelay: "0ms" }}></div>
                    <div className="h-2 w-2 animate-bounce rounded-full bg-lavender" style={{ animationDelay: "150ms" }}></div>
                    <div className="h-2 w-2 animate-bounce rounded-full bg-kobi" style={{ animationDelay: "300ms" }}></div>
                  </div>
                </div>
              ) : (
                <>
                  <MarkdownRenderer content={message.content} />
                  {message.isStreaming && message.content && (
                    <div className="mt-4 flex items-center gap-2 border-t border-rhythm pt-3">
                      <div className="relative flex h-4 w-4">
                        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-lavender opacity-75"></span>
                        <span className="relative inline-flex h-4 w-4 rounded-full bg-typhoon-primary"></span>
                      </div>
                      <span className="text-xs text-gray-300">
                        {message.currentEvent || "กำลังประมวลผล..."}
                      </span>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

