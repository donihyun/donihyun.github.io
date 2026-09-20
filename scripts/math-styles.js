'use strict';

// Icarus reads heading text for its TOC. Keep MathJax's embedded CSS outside headings.
hexo.extend.filter.register('after_post_render', data => {
  const styles = new Set();
  data.content = data.content.replace(/<style\b[^>]*>[\s\S]*?<\/style>/g, style => {
    // MathJax's selectable, transparent MathML must not widen the visual line.
    if (style.includes('mjx-assistive-mml')) {
      style = style.replace('width: auto !important;', 'width: 1px !important;')
        .replace('clip: auto !important;', 'clip: rect(1px, 1px, 1px, 1px) !important;');
    }
    styles.add(style);
    return '';
  });
  data.content = [...styles].join('') + data.content;
  return data;
});
