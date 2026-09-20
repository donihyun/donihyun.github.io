# Blog template overrides

These files customize the installed MIT-licensed Icarus 6.1.1 theme. Layout and
styles follow the public reference https://leimao.github.io/ (2026-09-20), while
post content, identity, account links, and counters belong to this blog.

`npm run build` and `npm run server` copy the installed theme into the ignored
`themes/icarus/` directory and apply these overrides. Edit the tracked files here,
not the generated directory. Theme code retains its upstream license in LICENSE.

Fonts live in `source/fonts/`, styling in `source/css/profile.css`, and the theme
configuration in `_config.icarus.yml`. Donations and additional social links need
the owner's real account details. No third-party author's accounts or ads are used.

Browser check (requires Selenium and Firefox/geckodriver):

```
python tests/check_blog.py https://donihyun.github.io /path/to/geckodriver /tmp/blog-check
```
