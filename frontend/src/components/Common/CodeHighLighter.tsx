import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus as github } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodeHighlighterProps {
  language: string;
  code: string;
}

const CodeHighlighter: React.FC<CodeHighlighterProps> = ({ language, code }) => {
  return (
	<SyntaxHighlighter language={language} style={github}>
	  {code}
	</SyntaxHighlighter>
  );
};

export default CodeHighlighter;