'use strict';

const { createHash } = require('node:crypto');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const version = createHash('sha256')
  .update(readFileSync(join(hexo.source_dir, 'css/profile.css')))
  .digest('hex').slice(0, 12);

hexo.extend.injector.register('head_end',
  `<link rel="stylesheet" href="/css/profile.css?v=${version}">`);
