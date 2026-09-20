'use strict';

document.addEventListener('DOMContentLoaded', () => {
  // Reuse rendered equations so the TOC needs no system math fonts.
  document.querySelectorAll('#toc a[data-href^="#"], #toc a[href^="#"]').forEach(link => {
    const hash = link.hasAttribute('data-href') ? link.getAttribute('data-href') : link.hash;
    const heading = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!heading) throw new Error(`Missing TOC heading: ${hash}`);
    if (!heading.querySelector('mjx-container')) return;
    const label = heading.cloneNode(true);
    label.querySelectorAll('mjx-container').forEach(container => {
      const math = container.querySelector('math');
      const svg = container.querySelector('svg');
      if (!math || !svg) throw new Error('MathJax equation is missing SVG or accessible MathML');
      svg.removeAttribute('aria-hidden');
      svg.setAttribute('aria-label', math.textContent);
      container.querySelector('mjx-assistive-mml').remove();
    });
    label.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
    label.querySelectorAll('style, .headerlink').forEach(node => node.remove());
    const target = link.querySelector('.level-item:last-child');
    target.replaceChildren(...label.childNodes);
  });
  setTimeout(() => {
    document.querySelectorAll('[id^="busuanzi_value_"]').forEach(counter => {
      if (counter.textContent === 'Loading…') {
        counter.textContent = 'Unavailable';
        counter.title = 'The visitor-count service did not respond';
      }
    });
  }, 15000);
});
