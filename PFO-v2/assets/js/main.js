/* ==========================================================================
   PFO_NewWeb — main.js（PHASE 5, PHASE 11）
   1) Mobile menu (< 1024px).  2) Card fade-in on scroll (PHASE 11, see below).
   - Toggle button updates aria-expanded / aria-label
   - Esc closes and returns focus to the toggle
   - Tab is kept inside header + menu while open
   - Closes on link click and when resizing to desktop
   The page works without JavaScript: the menu stays hidden and every page
   is still reachable from the footer links.
   ========================================================================== */
/* PHASE 11 — Cards fade in when scrolled into view.
   Runs only when motion is allowed and IntersectionObserver exists. Only cards
   that start below the fold are hidden (.pfo-reveal), so nothing that is
   already on screen blinks. The CSS lives inside
   @media (prefers-reduced-motion: no-preference). */
(() => {
  'use strict';
  const motionOK = window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
  if (!motionOK || !('IntersectionObserver' in window)) return;
  const cards = [...document.querySelectorAll('main .pfo-card')]
    .filter((el) => el.getBoundingClientRect().top > window.innerHeight);
  if (!cards.length) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      // reveal when it scrolls in — or if the user jumped past it (End key, anchor link)
      if (!entry.isIntersecting && entry.boundingClientRect.top > 0) return;
      entry.target.classList.add('is-visible');
      io.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -10% 0px' });
  cards.forEach((el) => { el.classList.add('pfo-reveal'); io.observe(el); });
})();

(() => {
  'use strict';

  const toggle = document.querySelector('[data-menu-toggle]');
  const menu = document.getElementById('mobile-menu');
  if (!toggle || !menu) return;

  const header = toggle.closest('.pfo-header');
  const background = [...document.querySelectorAll('body > .pfo-skip, body > main, body > footer, body > .pfo-review-banner')];
  const desktop = window.matchMedia('(min-width: 1024px)');
  const LABEL_OPEN = '開啟選單';
  const LABEL_CLOSE = '關閉選單';

  const focusables = () =>
    [...header.querySelectorAll('a[href], button:not([disabled])'),
     ...menu.querySelectorAll('a[href], button:not([disabled])')]
      .filter((el) => el.offsetParent !== null);

  // Pin the panel right under the header's current bottom edge
  // (the header can sit lower when the test banner is visible above it).
  const placeMenu = () => {
    menu.style.top = `${Math.max(0, header.getBoundingClientRect().bottom)}px`;
  };

  function setOpen(open, { returnFocus = false } = {}) {
    if (open) placeMenu();
    menu.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? LABEL_CLOSE : LABEL_OPEN);
    // SVG elements have no .hidden property — toggle the attribute instead
    toggle.querySelector('[data-icon="open"]').toggleAttribute('hidden', open);
    toggle.querySelector('[data-icon="close"]').toggleAttribute('hidden', !open);
    document.documentElement.classList.toggle('is-menu-open', open);
    // PHASE 9: while the menu covers the page, hide the rest of the page from
    // screen readers and keyboard (it is visually covered anyway).
    background.forEach((el) => { el.inert = open; });
    if (open) {
      menu.querySelector('a[href]')?.focus();
    } else if (returnFocus) {
      toggle.focus();
    }
  }

  toggle.addEventListener('click', () => {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  menu.addEventListener('click', (event) => {
    if (event.target.closest('a[href]')) setOpen(false);
  });

  document.addEventListener('keydown', (event) => {
    if (menu.hidden) return;
    if (event.key === 'Escape') {
      setOpen(false, { returnFocus: true });
      return;
    }
    if (event.key === 'Tab') {
      const items = focusables();
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });

  window.addEventListener('resize', () => { if (!menu.hidden) placeMenu(); });

  desktop.addEventListener('change', (event) => {
    if (event.matches) setOpen(false);
  });
})();
