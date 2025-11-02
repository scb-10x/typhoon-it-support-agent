/**
 * Workflow events panel component
 */

import { WorkflowEvent } from "./types";

interface WorkflowPanelProps {
  events: WorkflowEvent[];
  isVisible: boolean;
  onClose: () => void;
}

const getEventIcon = (eventType: string): string => {
  switch (eventType) {
    case "workflow_start":
      return "🚀";
    case "workflow_end":
      return "✅";
    case "node_start":
      return "▶️";
    case "node_end":
      return "✓";
    case "tool_start":
      return "🔧";
    case "tool_end":
      return "🔨";
    case "agent_thinking":
      return "🤔";
    case "agent_response":
      return "💬";
    case "router_decision":
      return "🔀";
    case "status":
      return "ℹ️";
    case "done":
      return "🎉";
    case "ticket_created":
      return "🎫";
    case "error":
    case "workflow_error":
    case "node_error":
    case "tool_error":
      return "❌";
    default:
      return "•";
  }
};

const getEventColor = (eventType: string): string => {
  if (eventType.includes("error")) return "text-desert";
  if (eventType.includes("start")) return "text-cerulean";
  if (eventType.includes("end") || eventType === "done") return "text-green-400";
  if (eventType === "ticket_created") return "text-green-400";
  if (eventType.includes("tool")) return "text-lavender";
  if (eventType.includes("agent")) return "text-typhoon-primary";
  if (eventType.includes("router")) return "text-kobi";
  return "text-gray-400";
};

export const WorkflowPanel = ({ events, isVisible, onClose }: WorkflowPanelProps) => {
  if (!isVisible) return null;

  return (
    <div className="w-80 sm:w-96 border-l border-rhythm bg-typhoon-darker flex flex-col h-full">
      <div className="flex-shrink-0 border-b border-rhythm bg-typhoon-dark px-4 py-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-white font-[var(--font-noto-sans-thai)]">
            Workflow Events
          </h2>
          <button
            onClick={onClose}
            className="rounded-lg p-1 text-gray-400 transition-colors hover:bg-rhythm hover:text-gray-200"
            aria-label="Close workflow panel"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-4 min-h-0">
        {events.length === 0 ? (
          <div className="flex h-full items-center justify-center text-center">
            <div className="text-gray-400">
              <svg
                className="mx-auto mb-2 h-12 w-12 opacity-50"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              <p className="text-sm">ส่งข้อความเพื่อดู workflow events</p>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            {events.map((event, index) => (
              <div
                key={index}
                className="animate-in fade-in slide-in-from-right-4 rounded-lg border border-rhythm bg-typhoon-dark/50 p-3 text-xs"
              >
                <div className="flex items-start gap-2">
                  <span className="text-lg">{getEventIcon(event.type)}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={`font-semibold ${getEventColor(event.type)}`}>
                        {event.type.replace(/_/g, " ").toUpperCase()}
                      </span>
                      {event.data?.iteration !== undefined && (
                        <span className="rounded bg-rhythm px-1.5 py-0.5 text-xs">
                          Iter {event.data.iteration}
                        </span>
                      )}
                    </div>
                    {event.data?.node_name && (
                      <p className="mt-1 text-gray-300">
                        Node: <span className="font-mono">{event.data.node_name}</span>
                      </p>
                    )}
                    {event.data?.tool_name && (
                      <p className="mt-1 text-gray-300">
                        Tool: <span className="font-mono">{event.data.tool_name}</span>
                      </p>
                    )}
                    {event.data?.message && (
                      <p className="mt-1 text-gray-200">{event.data.message}</p>
                    )}
                    {event.data?.error && (
                      <p className="mt-1 text-desert">Error: {event.data.error}</p>
                    )}
                    <p className="mt-1 text-xs text-gray-400">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
