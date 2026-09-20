'use strict';

// Listing pages keep the reference's three columns; reading pages use profile + TOC.
hexo.extend.filter.register('template_locals', locals => {
  if (['post', 'page'].includes(locals.page.layout)) {
    locals.config.widgets = locals.config.widgets.filter(widget =>
      ['profile', 'toc'].includes(widget.type));
  }
  return locals;
}, 20);
