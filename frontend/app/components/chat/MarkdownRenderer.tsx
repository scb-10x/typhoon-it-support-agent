/**
 * Markdown renderer component with custom styling
 */

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { CodeBlock } from "./CodeBlock";

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer = ({ content }: MarkdownRendererProps) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ children }) => (
          <h1 className="mb-4 mt-6 text-3xl font-bold text-white first:mt-0 border-b-2 border-rhythm pb-2">
            {children}
          </h1>
        ),
        h2: ({ children }) => (
          <h2 className="mb-3 mt-6 text-2xl font-bold text-white first:mt-0 border-b border-rhythm pb-2">
            {children}
          </h2>
        ),
        h3: ({ children }) => (
          <h3 className="mb-3 mt-5 text-xl font-semibold text-white first:mt-0">
            {children}
          </h3>
        ),
        h4: ({ children }) => (
          <h4 className="mb-2 mt-4 text-lg font-semibold text-white first:mt-0">
            {children}
          </h4>
        ),
        h5: ({ children }) => (
          <h5 className="mb-2 mt-3 text-base font-semibold text-white first:mt-0">
            {children}
          </h5>
        ),
        h6: ({ children }) => (
          <h6 className="mb-2 mt-3 text-sm font-semibold text-white first:mt-0">
            {children}
          </h6>
        ),
        p: ({ children }) => (
          <p className="mb-4 leading-relaxed text-gray-200 last:mb-0">
            {children}
          </p>
        ),
        ul: ({ children }) => (
          <ul className="mb-4 ml-6 list-disc space-y-2 text-gray-200">
            {children}
          </ul>
        ),
        ol: ({ children }) => (
          <ol className="mb-4 ml-6 list-decimal space-y-2 text-gray-200">
            {children}
          </ol>
        ),
        li: ({ children }) => (
          <li className="leading-relaxed">{children}</li>
        ),
        blockquote: ({ children }) => (
          <blockquote className="my-4 border-l-4 border-typhoon-primary pl-4 italic text-cerulean">
            {children}
          </blockquote>
        ),
        table: ({ children }) => (
          <div className="my-4 overflow-x-auto">
            <table className="min-w-full divide-y divide-rhythm">
              {children}
            </table>
          </div>
        ),
        thead: ({ children }) => (
          <thead className="bg-typhoon-darker">
            {children}
          </thead>
        ),
        tbody: ({ children }) => (
          <tbody className="divide-y divide-rhythm bg-typhoon-dark">
            {children}
          </tbody>
        ),
        tr: ({ children }) => (
          <tr className="even:bg-rhythm/10">
            {children}
          </tr>
        ),
        th: ({ children }) => (
          <th className="px-4 py-3 text-left text-sm font-semibold text-white">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="px-4 py-3 text-sm text-gray-200">
            {children}
          </td>
        ),
        hr: () => (
          <hr className="my-6 border-t-2 border-rhythm" />
        ),
        code: ({ children, className }) => {
          const match = /language-(\w+)/.exec(className || "");
          const language = match ? match[1] : "";

          return !className ? (
            <code className="rounded-md bg-typhoon-darker px-2 py-0.5 text-sm font-mono text-kobi">
              {children}
            </code>
          ) : (
            <CodeBlock language={language} value={String(children).replace(/\n$/, "")} />
          );
        },
        strong: ({ children }) => (
          <strong className="font-semibold text-white">
            {children}
          </strong>
        ),
        em: ({ children }) => (
          <em className="italic text-gray-200">
            {children}
          </em>
        ),
        a: ({ children, href }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-cerulean underline decoration-cerulean decoration-2 underline-offset-2 transition-colors hover:text-cerulean-light"
          >
            {children}
          </a>
        ),
      }}
    >
      {content || " "}
    </ReactMarkdown>
  );
};

