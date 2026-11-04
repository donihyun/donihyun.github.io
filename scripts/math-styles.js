'use strict';

const MarkdownIt = require('markdown-it');
const mathjax = require('markdown-it-mathjax3');

// Icarus reads heading text for its TOC. Keep MathJax's embedded CSS outside headings.
const titleMarkdown = new MarkdownIt({
  html: false,
  breaks: false,
  linkify: true,
  typographer: false
}).use(mathjax);

hexo.extend.filter.register('after_post_render', data => {
  const styles = new Set();
  const extractStyles = html => html.replace(/<style\b[^>]*>[\s\S]*?<\/style>/g, style => {
    // MathJax's selectable, transparent MathML must not widen the visual line.
    if (style.includes('mjx-assistive-mml')) {
      style = style.replace('width: auto !important;', 'width: 1px !important;')
        .replace('clip: auto !important;', 'clip: rect(1px, 1px, 1px, 1px) !important;');
    }
    styles.add(style);
    return '';
  });
  data.title_html = extractStyles(titleMarkdown.renderInline(data.title || ''));
  data.content = extractStyles(data.content);
  data.content = [...styles].join('') + data.content;
  return data;
});
