'use strict';

(() => {
  const saved = localStorage.getItem('blog-color-scheme');
  if (saved !== null && saved !== 'light' && saved !== 'dark') {
    throw new Error('Invalid blog-color-scheme preference');
  }
  const root = document.documentElement;
  root.classList.toggle('night', saved === 'dark');
  document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('night-nav');
    const icon = document.getElementById('night-icon');
    const sync = () => {
      const dark = root.classList.contains('night');
      button.setAttribute('aria-pressed', String(dark));
      button.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      icon.className = dark ? 'fas fa-sun' : 'fas fa-moon';
    };
    sync();
    button.addEventListener('click', () => {
      const dark = !root.classList.contains('night');
      localStorage.setItem('blog-color-scheme', dark ? 'dark' : 'light');
      root.classList.toggle('night', dark);
      sync();
    });
  });
})();
