'use strict';

// Icarus reads heading text for its TOC. Keep MathJax's embedded CSS outside headings.
hexo.extend.filter.register('after_post_render', data => {
  const styles = new Set();
  data.content = data.content.replace(/<style\b[^>]*>[\s\S]*?<\/style>/g, style => {
    styles.add(style);
    return '';
  });
  data.content = [...styles].join('') + data.content;
  return data;
});
