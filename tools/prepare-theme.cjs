'use strict';

const { cpSync } = require('node:fs');
const { dirname, resolve } = require('node:path');
const root = resolve(__dirname, '..');
const upstream = dirname(require.resolve('hexo-theme-icarus/package.json'));
const theme = resolve(root, 'themes/icarus');
// The installed Icarus package supplies unchanged templates and assets.
cpSync(upstream, theme, { recursive: true });
cpSync(resolve(root, 'template'), theme, { recursive: true });
