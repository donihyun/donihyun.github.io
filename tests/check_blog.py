"""Check the built real blog: python check_blog.py BASE_URL GECKODRIVER SCREENSHOT_DIR."""
import json
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

base, geckodriver, output = sys.argv[1:]
output = Path(output)
output.mkdir(parents=True, exist_ok=True)
options = Options()
options.add_argument('-headless')
options.enable_bidi = True
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(service=Service(geckodriver, log_output=str(output / 'geckodriver.log')), options=options)
try:
    rows = []
    for route in ['/', '/2026/04/01/solutions-to-e-to-the-ez-equals-1/']:
        driver.get(base.rstrip('/') + route)
        driver.execute_async_script('document.fonts.ready.then(() => arguments[0]());')
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.fonts.check(\'16px "PT Serif"\') && document.fonts.check(\'700 16px "PT Sans Narrow"\')'))
        for width in [320, 375, 414, 768, 1440]:
            driver.browsing_context.set_viewport(context=driver.current_window_handle, viewport={'width': width, 'height': 1000})
            result = driver.execute_script('''
                const title = document.querySelector('article.article > .title');
                const content = document.querySelector('article.article > .content');
                const meta = document.querySelector('.article-meta');
                const style = getComputedStyle(content);
                return {
                    width: innerWidth,
                    scrollWidth: document.documentElement.scrollWidth,
                    titleBeforeContent: title.getBoundingClientRect().bottom <= meta.getBoundingClientRect().top && meta.getBoundingClientRect().bottom <= content.getBoundingClientRect().top,
                    bodyFont: style.fontFamily,
                    headingFont: getComputedStyle(title).fontFamily,
                    lineHeight: parseFloat(style.lineHeight) / parseFloat(style.fontSize),
                    equations: content.querySelectorAll('mjx-container').length,
                    mathErrors: content.querySelectorAll('[data-mml-node="merror"],merror').length,
                    rawMath: content.textContent.includes('$$'),
                    warnings: document.querySelectorAll('.notification.is-danger').length,
                    title: title.textContent,
                    contentWidth: content.clientWidth,
                    contentScrollWidth: content.scrollWidth,
                    tocText: document.querySelector('#toc')?.textContent ?? '',
                    metaFits: [...meta.querySelectorAll('.level-item')].every(e => e.getBoundingClientRect().right <= innerWidth),
                    brokenToc: [...document.querySelectorAll('#toc a[href^="#"]')].some(a => !document.getElementById(decodeURIComponent(a.hash.slice(1))))
                };
            ''')
            result['route'] = route
            print(json.dumps(result), flush=True)
            assert result['width'] == width, result
            assert result['scrollWidth'] <= width, result
            assert result['contentScrollWidth'] <= result['contentWidth'] + 1, result
            assert result['titleBeforeContent'], result
            assert 'PT Serif' in result['bodyFont'], result
            assert 'PT Sans Narrow' in result['headingFont'], result
            assert abs(result['lineHeight'] - 1.5) < 0.01, result
            assert result['equations'] > 20, result
            assert result['mathErrors'] == 0 and not result['rawMath'], result
            assert result['warnings'] == 0 and not result['brokenToc'], result
            assert 'display:' not in result['tocText'] and 'mjx-' not in result['tocText'], result
            assert result['metaFits'], result
            assert result['title'] == 'Solving exp(exp(z)) = 1 on the Complex Plane', result
            name = 'home' if route == '/' else 'post'
            driver.save_screenshot(str(output / f'{name}-{width}.png'))
            rows.append(result)
    (output / 'checks.json').write_text(json.dumps(rows, indent=2))
finally:
    driver.quit()
