/**
 * Chat input form component
 */

import { useRef, useCallback } from "react";

interface ChatInputProps {
  input: string;
  isLoading: boolean;
  onInputChange: (value: string) => void;
  onSubmit: (message: string) => void;
}

export const ChatInput = ({ input, isLoading, onInputChange, onSubmit }: ChatInputProps) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const adjustTextareaHeight = useCallback(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "auto";
    const newHeight = Math.min(textarea.scrollHeight, 200);
    textarea.style.height = `${newHeight}px`;
  }, []);

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    onInputChange(value);
    adjustTextareaHeight();
  }, [onInputChange, adjustTextareaHeight]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isLoading) {
        const form = e.currentTarget.form;
        if (form) {
          form.requestSubmit();
        }
      }
    }
  }, [input, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    onSubmit(input);
    onInputChange("");
    
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleClear = () => {
    onInputChange("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.focus();
    }
  };

  return (
    <div className="flex-shrink-0 border-t border-rhythm bg-gradient-to-b from-typhoon-darker/95 to-typhoon-dark/95 backdrop-blur-md shadow-[0_-8px_32px_rgba(0,0,0,0.4)]">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 py-5 sm:py-6">
        <form onSubmit={handleSubmit}>
          <div className="relative group">
            {/* Enhanced input container with gradient border effect */}
            <div className="absolute -inset-[2px] bg-gradient-to-r from-typhoon-primary via-lavender to-cerulean rounded-[28px] opacity-0 group-focus-within:opacity-100 blur-sm transition-opacity duration-500"></div>
            <div className="relative flex items-end gap-2 rounded-[26px] bg-gradient-to-br from-typhoon-dark to-typhoon-darker border-2 border-rhythm group-focus-within:border-transparent p-2 shadow-xl transition-all duration-300">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                placeholder="พิมพ์คำถามของคุณที่นี่..."
                disabled={isLoading}
                autoFocus
                rows={1}
                className="flex-1 resize-none overflow-hidden bg-transparent px-4 py-3 text-base text-white placeholder:text-gray-400 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
                style={{ minHeight: "48px", maxHeight: "200px" }}
              />

              {/* Action buttons container */}
              <div className="flex items-center gap-2 pb-1.5">
                {input && !isLoading && (
                  <button
                    type="button"
                    onClick={handleClear}
                    className="rounded-xl p-2 text-gray-400 transition-all hover:bg-rhythm/50 hover:text-white hover:scale-110 active:scale-95"
                    aria-label="Clear input"
                  >
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}

                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="relative group/btn flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-typhoon-primary via-lavender to-typhoon-primary bg-size-200 bg-pos-0 hover:bg-pos-100 px-5 py-3 font-semibold text-white shadow-lg shadow-typhoon-primary/30 transition-all duration-500 hover:shadow-xl hover:shadow-lavender/40 hover:scale-105 active:scale-95 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:scale-100 disabled:hover:shadow-lg min-w-[48px] h-[48px]"
                  aria-label={isLoading ? "กำลังส่ง..." : "ส่งข้อความ"}
                >
                  {isLoading ? (
                    <div className="relative">
                      <svg
                        className="h-6 w-6 animate-spin"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="3"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                    </div>
                  ) : (
                    <>
                      <svg
                        className="h-5 w-5 transition-transform duration-300 group-hover/btn:translate-x-0.5 group-hover/btn:-translate-y-0.5"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                      </svg>
                      <span className="hidden sm:inline font-[var(--font-noto-sans-thai)]">ส่ง</span>
                    </>
                  )}
                  {/* Pulse effect when ready to send */}
                  {!isLoading && input.trim() && (
                    <span className="absolute inset-0 rounded-2xl bg-white opacity-0 group-hover/btn:opacity-20 transition-opacity duration-300"></span>
                  )}
                </button>
              </div>
            </div>
          </div>
        </form>
        <div className="mt-3 flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-xs text-gray-400">
          <div className="flex items-center gap-1.5">
            <kbd className="rounded bg-typhoon-darker px-1.5 py-0.5 font-mono text-xs border border-rhythm">Enter</kbd>
            <span>ส่ง</span>
          </div>
          <span className="hidden sm:inline">•</span>
          <div className="flex items-center gap-1.5">
            <kbd className="rounded bg-typhoon-darker px-1.5 py-0.5 font-mono text-xs border border-rhythm">Shift+Enter</kbd>
            <span className="hidden sm:inline">บรรทัดใหม่</span>
          </div>
          <span className="hidden sm:inline">•</span>
          <div className="flex items-center gap-1.5">
            <kbd className="rounded bg-typhoon-darker px-1.5 py-0.5 font-mono text-xs border border-rhythm">ESC</kbd>
            <span>ล้าง</span>
          </div>
          <span className="hidden sm:inline">•</span>
          <span className="text-gray-500">Powered by Typhoon AI</span>
        </div>
      </div>
    </div>
  );
};

