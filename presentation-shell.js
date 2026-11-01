(() => {
  'use strict';
  const menu = document.querySelector('.deck-sidebar');
  const toggle = document.querySelector('.deck-nav-toggle');
  const localMenu = document.querySelector('.deck-local-menu');
  const expand = document.querySelector('.deck-expand');
  const progress = document.querySelector('.deck-progress > span');
  const disclosure = [...document.querySelectorAll('.research-archive, .page-content details, .page-intro .deck-context')];
  document.querySelectorAll('table.deck-responsive-table').forEach(table => {
    const labels = [...table.querySelectorAll('thead th')].map(cell => cell.textContent.trim());
    table.querySelectorAll('tbody tr').forEach(row => {
      [...row.cells].forEach((cell,index) => {
        if (!cell.hasAttribute('colspan') && labels[index]) cell.dataset.label = labels[index];
      });
    });
  });

  const closeMenu = () => {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    if (open && localMenu) localMenu.open = false;
  });
  menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (menu.classList.contains('is-open')) { closeMenu(); toggle.focus(); }
    if (localMenu?.open) { localMenu.open = false; localMenu.querySelector('summary').focus(); }
  });
  document.addEventListener('click', event => {
    if (localMenu && !localMenu.contains(event.target)) localMenu.open = false;
    if (!menu.contains(event.target) && !toggle.contains(event.target)) closeMenu();
  });
  localMenu?.addEventListener('click', event => {
    if (event.target.closest('a')) localMenu.open = false;
  });
  expand?.addEventListener('click', () => {
    const open = expand.getAttribute('aria-expanded') !== 'true';
    disclosure.forEach(detail => { detail.open = open; });
    expand.setAttribute('aria-expanded', String(open));
    expand.textContent = open ? 'Свернуть подробности' : 'Раскрыть подробности';
  });

  // Direct links to evidence also open every native disclosure above the target.
  function revealTarget() {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    let parent = target.parentElement;
    while (parent) {
      if (parent.tagName === 'DETAILS') parent.open = true;
      parent = parent.parentElement;
    }
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'instant' }));
  }
  window.addEventListener('hashchange', revealTarget);
  window.addEventListener('load', revealTarget, { once: true });
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (link && link.hash === location.hash) revealTarget();
  });

  let scheduled = false;
  const sections = [...document.querySelectorAll('.plain-showcase>section, .page-content>.deck-section')];
  const localLinks = [...(localMenu?.querySelectorAll('a') || [])];
  function updateProgress() {
    scheduled = false;
    const range = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${range > 0 ? Math.min(1,scrollY/range) : 1})`;
    let current = null;
    for (const section of sections) {
      if (section.getBoundingClientRect().top < 180) current = section.id;
    }
    localLinks.forEach(link => {
      if (link.hash === `#${current}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  function requestProgress() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updateProgress); }
  }
  addEventListener('scroll', requestProgress, { passive: true });
  addEventListener('resize', requestProgress, { passive: true });
  disclosure.forEach(detail => detail.addEventListener('toggle', requestProgress));
  updateProgress();
  window.addEventListener('beforeprint', () => disclosure.forEach(detail => { detail.dataset.printOpen = detail.open; detail.open = true; }));
  window.addEventListener('afterprint', () => disclosure.forEach(detail => { detail.open = detail.dataset.printOpen === 'true'; delete detail.dataset.printOpen; }));
})();
