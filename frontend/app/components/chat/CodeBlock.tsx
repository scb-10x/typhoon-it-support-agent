/**
 * Code block component with syntax highlighting and copy functionality
 */

import { useState, useCallback } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { CodeBlockProps } from "./types";

export const CodeBlock = ({ language, value }: CodeBlockProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [value]);

  return (
    <div className="group relative my-4">
      <div className="absolute right-2 top-2 z-10">
        <button
          onClick={handleCopy}
          className="rounded-lg bg-gray-700 px-3 py-1 text-xs text-white opacity-0 transition-opacity hover:bg-gray-600 group-hover:opacity-100"
          aria-label="Copy code"
        >
          {copied ? "✓ คัดลอกแล้ว" : "คัดลอก"}
        </button>
      </div>
      <SyntaxHighlighter
        language={language || "text"}
        style={oneDark}
        customStyle={{
          borderRadius: "0.75rem",
          padding: "1rem",
          fontSize: "0.875rem",
          margin: 0,
        }}
        showLineNumbers
      >
        {value}
      </SyntaxHighlighter>
    </div>
  );
};
