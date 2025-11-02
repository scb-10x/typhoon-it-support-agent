"use client";

/**
 * Main Chat component - orchestrates chat interface
 */

import { useState, useEffect } from "react";
import { Toaster } from "react-hot-toast";
import { useChat } from "./chat/useChat";
import { useChatScroll } from "./chat/useChatScroll";
import { ChatMessage } from "./chat/ChatMessage";
import { ChatInput } from "./chat/ChatInput";
import { WorkflowPanel } from "./chat/WorkflowPanel";

export default function Chat() {
  const [input, setInput] = useState("");
  const [showWorkflowPanel, setShowWorkflowPanel] = useState(false);

  const { messages, isLoading, workflowEvents, sendMessage, clearChat } = useChat();
  const { messagesEndRef, messagesContainerRef, showScrollButton, scrollToBottom } =
    useChatScroll();

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === "Escape" && messages.length > 0) {
        clearChat();
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [messages.length, clearChat]);

  const handleSubmit = async (message: string) => {
    await sendMessage(message);
  };

  return (
    <div className="flex h-full w-full bg-gradient-to-br from-typhoon-dark via-typhoon-darker to-black">
      {/* Toast Notifications */}
      <Toaster />

      {/* Main Chat Section */}
      <div className="flex flex-1 flex-col min-w-0">
        {/* Header */}
        <header className="flex-shrink-0 border-b border-rhythm bg-typhoon-darker/95 backdrop-blur-md shadow-sm">
          <div className="mx-auto flex max-w-5xl items-center justify-between px-4 sm:px-6 py-3 sm:py-4">
            <div className="flex items-center gap-2 sm:gap-3 min-w-0">
              <div className="flex h-10 w-10 sm:h-11 sm:w-11 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-typhoon-primary to-lavender text-white shadow-lg ring-2 ring-lavender/20">
                <svg
                  className="h-5 w-5 sm:h-6 sm:w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                  />
                </svg>
              </div>
              <div className="min-w-0">
                <h1 className="text-lg sm:text-xl font-bold text-white truncate font-[var(--font-noto-sans-thai)]">
                  ผู้ช่วย IT Support
                </h1>
                <p className="text-xs text-gray-400 flex items-center gap-1.5 font-[var(--font-pridi)]">
                  <span className="relative flex h-2 w-2 flex-shrink-0">
                    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex h-2 w-2 rounded-full bg-green-500"></span>
                  </span>
                  <span className="truncate">ขับเคลื่อนด้วย Typhoon AI</span>
                </p>
              </div>
            </div>
            <div className="flex items-center gap-1.5 sm:gap-2 flex-shrink-0">
              <button
                onClick={() => setShowWorkflowPanel(!showWorkflowPanel)}
                className="group flex items-center gap-1.5 sm:gap-2 rounded-xl border border-rhythm bg-typhoon-darker/80 px-2.5 sm:px-4 py-2 text-sm font-medium text-gray-200 shadow-sm transition-all hover:border-typhoon-primary hover:bg-typhoon-darker hover:shadow-md active:scale-95"
                aria-label="Toggle workflow panel"
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
                <span className="hidden lg:inline">Workflow</span>
                {workflowEvents.length > 0 && (
                  <span className="flex h-5 w-5 items-center justify-center rounded-full bg-typhoon-primary text-xs text-white">
                    {workflowEvents.length}
                  </span>
                )}
              </button>
              <button
                onClick={clearChat}
                title="กด ESC เพื่อล้างการสนทนา"
                className="group flex items-center gap-1.5 sm:gap-2 rounded-xl border border-rhythm bg-typhoon-darker/80 px-2.5 sm:px-4 py-2 text-sm font-medium text-gray-200 shadow-sm transition-all hover:border-typhoon-primary hover:bg-typhoon-darker hover:shadow-md active:scale-95"
                aria-label="Clear chat"
              >
                <svg
                  className="h-4 w-4 transition-transform group-hover:rotate-180"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                <span className="hidden lg:inline">ล้าง</span>
              </button>
            </div>
          </div>
        </header>

        {/* Messages Container */}
        <div ref={messagesContainerRef} className="relative flex-1 overflow-y-auto min-h-0">
          <div className="mx-auto max-w-5xl px-4 sm:px-6 py-6 sm:py-8">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center py-16 text-center animate-in fade-in duration-700">
                <div className="mb-8 flex h-24 w-24 items-center justify-center rounded-2xl bg-gradient-to-br from-typhoon-primary to-lavender text-white shadow-2xl ring-4 ring-lavender/30 animate-in zoom-in duration-700">
                  <svg className="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    />
                  </svg>
                </div>
                <h2 className="mb-3 bg-gradient-to-r from-typhoon-primary to-lavender bg-clip-text text-3xl font-bold text-transparent font-[var(--font-noto-sans-thai)]">
                  ยินดีต้อนรับสู่ IT Support
                </h2>
                <p className="mb-10 max-w-lg text-base leading-relaxed text-gray-300 font-[var(--font-pridi)]">
                  ฉันพร้อมช่วยเหลือคุณในเรื่องปัญหาไอทีต่างๆ สามารถถามเกี่ยวกับการรีเซ็ตรหัสผ่าน
                  ปัญหา WiFi หรือการแก้ไขปัญหาซอฟต์แวร์ได้เลยครับ
                </p>
                <div className="w-full max-w-2xl">
                  <p className="mb-4 text-sm font-medium text-gray-400 font-[var(--font-pridi)]">
                    ลองคำถามเหล่านี้ดูสิ
                  </p>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    {[
                      { text: "ฉันจะรีเซ็ตรหัสผ่านได้อย่างไร?", icon: "🔐" },
                      { text: "WiFi ของฉันเชื่อมต่อไม่ได้", icon: "📶" },
                      { text: "คอมพิวเตอร์ทำงานช้า", icon: "⚡" },
                      { text: "เข้าอีเมลไม่ได้", icon: "📧" },
                    ].map((suggestion, idx) => (
                      <button
                        key={suggestion.text}
                        onClick={() => setInput(suggestion.text)}
                        style={{ animationDelay: `${idx * 100}ms` }}
                        className="group flex items-start gap-3 rounded-xl border-2 border-rhythm bg-typhoon-darker/50 p-4 text-left text-sm text-gray-200 shadow-sm transition-all hover:border-typhoon-primary hover:shadow-lg hover:-translate-y-0.5 active:scale-95 animate-in fade-in slide-in-from-bottom-4 duration-500 font-[var(--font-pridi)]"
                      >
                        <span className="text-2xl transition-transform group-hover:scale-110">
                          {suggestion.icon}
                        </span>
                        <span className="flex-1 pt-1">{suggestion.text}</span>
                        <svg
                          className="h-5 w-5 text-gray-400 transition-transform group-hover:translate-x-1"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 5l7 7-7 7"
                          />
                        </svg>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4 sm:space-y-6">
                {messages.map((message, index) => (
                  <ChatMessage key={index} message={message} index={index} />
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Scroll to Bottom Button */}
          {showScrollButton && (
            <div className="absolute bottom-4 sm:bottom-6 right-4 sm:right-6 z-10 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <button
                onClick={scrollToBottom}
                className="group flex h-11 w-11 sm:h-12 sm:w-12 items-center justify-center rounded-full bg-gradient-to-br from-typhoon-primary to-lavender text-white shadow-xl ring-2 ring-lavender/30 transition-all hover:shadow-2xl hover:scale-110 active:scale-95"
                aria-label="Scroll to bottom"
              >
                <svg
                  className="h-5 w-5 sm:h-6 sm:w-6 transition-transform group-hover:translate-y-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 14l-7 7m0 0l-7-7m7 7V3"
                  />
                </svg>
              </button>
            </div>
          )}
        </div>

        {/* Input Form */}
        <ChatInput
          input={input}
          isLoading={isLoading}
          onInputChange={setInput}
          onSubmit={handleSubmit}
        />
      </div>

      {/* Workflow Events Panel */}
      <WorkflowPanel
        events={workflowEvents}
        isVisible={showWorkflowPanel}
        onClose={() => setShowWorkflowPanel(false)}
      />
    </div>
  );
}
