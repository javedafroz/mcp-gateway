import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import rehypeRaw from 'rehype-raw';
import 'highlight.js/styles/github.css';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content, className = '' }) => {
  return (
    <div className={`markdown-content ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight, rehypeRaw]}
        components={{
          // Customize rendering of different markdown elements
          h1: ({ children, ...props }: any) => (
            <h1 className="text-xl font-bold text-gray-900 mb-3 mt-4 first:mt-0" {...props}>
              {children}
            </h1>
          ),
          h2: ({ children, ...props }: any) => (
            <h2 className="text-lg font-semibold text-gray-800 mb-2 mt-3 first:mt-0" {...props}>
              {children}
            </h2>
          ),
          h3: ({ children, ...props }: any) => (
            <h3 className="text-md font-medium text-gray-700 mb-2 mt-2 first:mt-0" {...props}>
              {children}
            </h3>
          ),
          p: ({ children, ...props }: any) => (
            <p className="mb-2 last:mb-0 leading-relaxed" {...props}>
              {children}
            </p>
          ),
          ul: ({ children, ...props }: any) => (
            <ul className="list-disc list-inside mb-2 space-y-1 pl-2" {...props}>
              {children}
            </ul>
          ),
          ol: ({ children, ...props }: any) => (
            <ol className="list-decimal list-inside mb-2 space-y-1 pl-2" {...props}>
              {children}
            </ol>
          ),
          li: ({ children, ...props }: any) => (
            <li className="text-sm" {...props}>
              {children}
            </li>
          ),
          blockquote: ({ children, ...props }: any) => (
            <blockquote className="border-l-4 border-primary-200 pl-4 py-2 my-2 bg-primary-50 italic" {...props}>
              {children}
            </blockquote>
          ),
          code: ({ className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || '');
            const isInline = !className?.includes('language-');
            return !isInline ? (
              <pre className="bg-gray-100 rounded-md p-3 my-2 overflow-x-auto">
                <code className={className} {...props}>
                  {children}
                </code>
              </pre>
            ) : (
              <code 
                className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono" 
                {...props}
              >
                {children}
              </code>
            );
          },
          pre: ({ children, ...props }: any) => (
            <div className="bg-gray-100 rounded-md p-3 my-2 overflow-x-auto" {...props}>
              {children}
            </div>
          ),
          table: ({ children, ...props }: any) => (
            <div className="overflow-x-auto my-2">
              <table className="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-md" {...props}>
                {children}
              </table>
            </div>
          ),
          thead: ({ children, ...props }: any) => (
            <thead className="bg-gray-50" {...props}>
              {children}
            </thead>
          ),
          tbody: ({ children, ...props }: any) => (
            <tbody className="bg-white divide-y divide-gray-200" {...props}>
              {children}
            </tbody>
          ),
          tr: ({ children, ...props }: any) => (
            <tr className="hover:bg-gray-50" {...props}>
              {children}
            </tr>
          ),
          th: ({ children, ...props }: any) => (
            <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" {...props}>
              {children}
            </th>
          ),
          td: ({ children, ...props }: any) => (
            <td className="px-3 py-2 text-sm text-gray-900" {...props}>
              {children}
            </td>
          ),
          a: ({ children, href, ...props }: any) => (
            <a 
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-800 underline"
              {...props}
            >
              {children}
            </a>
          ),
          strong: ({ children, ...props }: any) => (
            <strong className="font-semibold text-gray-900" {...props}>
              {children}
            </strong>
          ),
          em: ({ children, ...props }: any) => (
            <em className="italic text-gray-700" {...props}>
              {children}
            </em>
          ),
          hr: ({ ...props }: any) => (
            <hr className="border-gray-300 my-4" {...props} />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
