/* Inject a small CSS override for the Icarus profile widget.
 *
 * Hexo runs any JS files under `scripts/` at build time.
 * This uses Hexo's injector API (same mechanism you see as
 * `<!-- hexo injector head_end start -->` in generated HTML).
 */

'use strict';

hexo.extend.injector.register(
  'head_end',
  '<link rel="stylesheet" href="/css/profile.css?v=20260402-1052">'
);

