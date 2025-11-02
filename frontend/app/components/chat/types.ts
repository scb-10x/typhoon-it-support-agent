/**
 * TypeScript interfaces for Chat component
 */

export interface Message {
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
  currentEvent?: string;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  iteration: number;
  next_action: string;
}

export interface WorkflowEvent {
  type: string;
  timestamp: string;
  node_name?: string;
  tool_name?: string;
  message?: string;
  data?: Record<string, unknown>;
  error?: string;
  iteration?: number;
}

export interface CodeBlockProps {
  language?: string;
  value: string;
}
