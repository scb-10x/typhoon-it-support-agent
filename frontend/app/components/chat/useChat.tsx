/**
 * Custom hook for managing chat state and message sending
 */

import { useState } from "react";
import toast from "react-hot-toast";
import { Message, WorkflowEvent } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [workflowEvents, setWorkflowEvents] = useState<WorkflowEvent[]>([]);

  const sendMessage = async (userInput: string) => {
    if (!userInput.trim() || isLoading) return;

    const userMessage: Message = {
      role: "user",
      content: userInput,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setWorkflowEvents([]);

    // Add streaming message placeholder
    const streamingMessage: Message = {
      role: "assistant",
      content: "",
      isStreaming: true,
    };
    setMessages((prev) => [...prev, streamingMessage]);

    const requestBody = {
      message: userInput,
      session_id: sessionId,
    };

    try {
      const response = await fetch(`${API_URL}/chat/workflow`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok || !response.body) {
        throw new Error("Streaming not supported");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedContent = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));

              // Handle token streaming
              if (data.type === "token") {
                if (data.data?.message) {
                  accumulatedContent += data.data.message;
                  setMessages((prev) => {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = {
                      role: "assistant",
                      content: accumulatedContent,
                      isStreaming: true,
                    };
                    return newMessages;
                  });
                }
              } else {
                // Add non-token events to workflow events panel
                setWorkflowEvents((prev) => [...prev, data]);

                // Handle ticket created event - show toast
                if (data.type === "ticket_created") {
                  toast.success(`🎫 ${data.data?.message || "Ticket created successfully"}`, {
                    duration: 5000,
                    position: "top-right",
                    style: {
                      background: "#1a1d2e",
                      color: "#fff",
                      border: "1px solid #6366f1",
                    },
                  });
                }
              }

              if (data.type === "done") {
                // Finalize message
                if (data.data?.message && !accumulatedContent) {
                  accumulatedContent = data.data.message;
                }

                setMessages((prev) => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = {
                    role: "assistant",
                    content: accumulatedContent || "Processing complete",
                    isStreaming: false,
                  };
                  return newMessages;
                });

                if (data.data?.session_id) {
                  setSessionId(data.data.session_id);
                }
              } else if (data.type === "workflow_error" || data.type === "error") {
                setMessages((prev) => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = {
                    role: "assistant",
                    content:
                      "ขออภัยครับ เกิดข้อผิดพลาด: " + (data.data?.error || data.data?.message),
                    isStreaming: false,
                  };
                  return newMessages;
                });
              } else if (data.type !== "done") {
                // Update loading indicator with current event
                const eventMessage = data.data?.message || data.type.replace(/_/g, " ");
                setMessages((prev) => {
                  const newMessages = [...prev];
                  if (newMessages[newMessages.length - 1]?.isStreaming) {
                    newMessages[newMessages.length - 1] = {
                      ...newMessages[newMessages.length - 1],
                      currentEvent: eventMessage,
                    };
                  }
                  return newMessages;
                });
              }
            } catch (e) {
              console.error("Error parsing SSE data:", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Streaming error:", error);
      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          role: "assistant",
          content: "ขออภัยครับ เกิดข้อผิดพลาด กรุณาตรวจสอบว่า backend server ทำงานอยู่หรือไม่",
          isStreaming: false,
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
    setWorkflowEvents([]);
  };

  return {
    messages,
    isLoading,
    sessionId,
    workflowEvents,
    sendMessage,
    clearChat,
  };
};
