"""Check the built real blog: python check_blog.py BASE_URL GECKODRIVER SCREENSHOT_DIR."""
import json
import sys
import re
import urllib.request
import xml.etree.ElementTree as ET
from selenium.webdriver.common.by import By
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
    reference = json.loads((Path(__file__).parent / 'reference-layout.json').read_text())
    feed = ET.fromstring(urllib.request.urlopen(base.rstrip('/') + '/atom.xml', timeout=30).read())
    assert any(e.text == 'Solving exp(exp(z)) = 1 on the Complex Plane' for e in feed.iter('{http://www.w3.org/2005/Atom}title'))
    for route in ['/', '/2026/04/01/solutions-to-e-to-the-ez-equals-1/']:
        driver.get(base.rstrip('/') + route)
        driver.execute_async_script('document.fonts.ready.then(() => arguments[0]());')
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.fonts.check(\'16px "PT Serif"\') && document.fonts.check(\'700 16px "PT Sans Narrow"\')'))
        for width in [320, 375, 414, 768, 1088, 1280, 1440, 1600]:
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
                    dates: [...meta.querySelectorAll('time')].map(e => e.textContent),
                    metaIcons: meta.querySelectorAll('i').length,
                    domOrder: title.compareDocumentPosition(meta) & Node.DOCUMENT_POSITION_FOLLOWING,
                    followIcon: !!document.querySelector('[data-type=profile] a.button.is-primary .fa-github'),
                    navbarLogo: !!document.querySelector('.navbar-logo img'),
                    templateButton: !!document.querySelector('#night-nav'),
                    contentWidth: content.clientWidth,
                    contentScrollWidth: content.scrollWidth,
                    tocText: document.querySelector('#toc .menu')?.textContent ?? '',
                    metaFits: [...meta.querySelectorAll('.level-item')].every(e => e.getBoundingClientRect().right <= innerWidth),
                    brokenToc: [...document.querySelectorAll('#toc a[data-href^="#"], #toc a[href^="#"]')].some(a => !document.getElementById(decodeURIComponent((a.hasAttribute('data-href') ? a.getAttribute('data-href') : a.hash).slice(1))))
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
            assert result['domOrder'] and result['followIcon'] and result['navbarLogo'] and result['templateButton'], result
            assert all(re.fullmatch(r'\d{2}-\d{2}-\d{4}', date) for date in result['dates']), result
            assert result['metaIcons'] >= 4, result
            if route != '/' and str(width) in reference['widths']:
                for selector, expected in reference['widths'][str(width)].items():
                    actual = driver.execute_script("const e=document.querySelector(arguments[0]); const s=getComputedStyle(e); return {width:e.getBoundingClientRect().width,font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,line:s.lineHeight,margin:s.margin,padding:s.padding}", selector)
                    for key, value in expected.items():
                        if key == 'width':
                            assert abs(actual[key] - value) < 1, (width, selector, key, actual[key], value)
                        else:
                            assert actual[key] == value, (width, selector, key, actual[key], value)
            name = 'home' if route == '/' else 'post'
            driver.save_screenshot(str(output / f'{name}-{width}.png'))
            rows.append(result)
        driver.find_element(By.ID, 'night-nav').click()
        assert driver.execute_script("return document.documentElement.classList.contains('night')")
        driver.refresh()
        assert driver.execute_script("return document.documentElement.classList.contains('night')")
        assert driver.find_element(By.ID, 'night-nav').get_attribute('aria-pressed') == 'true'
        driver.save_screenshot(str(output / f'{name}-dark.png'))
        driver.find_element(By.ID, 'night-nav').click()
        driver.find_element(By.CSS_SELECTOR, '.navbar-end .search').click()
        field = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.CSS_SELECTOR, '.searchbox-input'))
        field.send_keys('Solving')
        WebDriverWait(driver, 20).until(lambda d: any('solutions-to-e-to-the-ez-equals-1' in a.get_attribute('href') for a in d.find_elements(By.CSS_SELECTOR, '.searchbox-result-item')))
        driver.find_element(By.CSS_SELECTOR, '.searchbox-close').click()
        if route != '/':
            assert len(driver.find_elements(By.CSS_SELECTOR, '#toc math msup')) == 2
            assert len(driver.find_elements(By.CSS_SELECTOR, '.a2a_kit > a')) == 9
    (output / 'checks.json').write_text(json.dumps(rows, indent=2))
finally:
    driver.quit()
