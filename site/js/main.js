(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 1. Тень шапки при прокрутке
  var header = document.querySelector('.site-header');
  var toTop = document.getElementById('toTop');
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    header.classList.toggle('scrolled', y > 10);
    toTop.classList.toggle('show', y > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  toTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
  });

  // 2. Подсветка пункта меню по текущему разделу
  var navLinks = document.querySelectorAll('.navbar .nav-link[href^="#"]');
  var sections = Array.prototype.map.call(navLinks, function (a) {
    return document.querySelector(a.getAttribute('href'));
  });
  if ('IntersectionObserver' in window) {
    var secObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        navLinks.forEach(function (a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { if (s && s.id) secObs.observe(s); });
  }

  // 3. Появление блоков при прокрутке
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var revObs = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { revObs.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // 4. Счётчики в блоке цифр
  var counters = document.querySelectorAll('[data-count]');
  function animateCount(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (reduceMotion || isNaN(target)) return;
    var start = null, duration = 1400;
    el.textContent = '0';
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cntObs = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          animateCount(e.target);
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cntObs.observe(el); });
  }

  // 5. Вкладки каталога (таблицы по группам)
  var tabLinks = document.querySelectorAll('#catalogTabs [data-tab]');
  var panes = document.querySelectorAll('.tab-pane-x');

  function showTab(tabId, scroll) {
    tabLinks.forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('data-tab') === tabId);
    });
    panes.forEach(function (p) {
      var on = p.getAttribute('data-pane') === tabId;
      p.classList.toggle('d-none', !on);
      p.classList.toggle('active', on);
      if (on) p.classList.add('reveal', 'in');
    });
    if (scroll) {
      var el = document.getElementById('catalog-details');
      if (el) el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    }
  }

  tabLinks.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      showTab(a.getAttribute('data-tab'), false);
      history.replaceState(null, '', a.getAttribute('href'));
    });
  });

  // Ссылки «Подробнее» в карточках открывают нужную вкладку
  document.querySelectorAll('#catalog .more').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').replace('#', '');
      var pane = document.getElementById(id);
      if (!pane) return;
      e.preventDefault();
      showTab(pane.getAttribute('data-pane'), true);
      history.replaceState(null, '', '#' + id);
    });
  });

  // 6. Закрывать мобильное меню после выбора пункта
  var collapseEl = document.getElementById('mainMenu');
  document.querySelectorAll('#mainMenu .nav-link').forEach(function (a) {
    a.addEventListener('click', function () {
      if (collapseEl.classList.contains('show') && window.bootstrap) {
        bootstrap.Collapse.getOrCreateInstance(collapseEl).hide();
      }
    });
  });
})();

// 7. Переход по якорю на карточку характеристик (<details id="d-…">) — раскрыть её (каталоги ОСК и ОПН)
(function () {
  'use strict';
  function openTarget() {
    var id = decodeURIComponent((location.hash || '').slice(1));
    var el = id && document.getElementById(id);
    if (el && el.tagName === 'DETAILS') el.open = true;
  }
  window.addEventListener('hashchange', openTarget);
  openTarget();
})();

// 8. Меню-шторка (<992px), стрелки раскрытия, выбор языка, строки каталога как ссылки
(function () {
  'use strict';
  var root = document.documentElement;
  var menu = document.getElementById('mainMenu');
  var toggler = document.querySelector('.navbar-toggler');
  var L = { ru: { close: 'Закрыть меню', open: 'Раскрыть', fold: 'Свернуть' }, uk: { close: 'Закрити меню', open: 'Розгорнути', fold: 'Згорнути' }, en: { close: 'Close menu', open: 'Expand', fold: 'Collapse' } };
  function lang() { var l = root.lang; return L[l] ? l : 'ru'; }

  if (menu && toggler) {
    var overlay = document.createElement('div'); overlay.className = 'nav-overlay'; (document.querySelector('.site-header') || document.body).appendChild(overlay);
    var head = document.createElement('div'); head.className = 'drawer-head';
    head.innerHTML = '<i class="fa fa-bolt bolt" aria-hidden="true"></i><button type="button" class="drawer-close" aria-label="Close"><i class="fa fa-times"></i></button>';
    menu.insertBefore(head, menu.firstChild);
    var icon = toggler.querySelector('i');
    function setOpen(on) {
      menu.classList.toggle('menu-open', on); root.classList.toggle('nav-open', on);
      toggler.setAttribute('aria-expanded', on ? 'true' : 'false');
      if (icon) { icon.classList.toggle('fa-bars', !on); icon.classList.toggle('fa-times', on); }
      head.querySelector('.drawer-close').setAttribute('aria-label', L[lang()].close);
    }
    toggler.addEventListener('click', function () { setOpen(!menu.classList.contains('menu-open')); });
    overlay.addEventListener('click', function () { setOpen(false); });
    head.querySelector('.drawer-close').addEventListener('click', function () { setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    window.addEventListener('resize', function () { if (window.innerWidth >= 992) setOpen(false); });
    menu.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (a && !a.closest('.mega-toggle')) setOpen(false);
    });
  }

  // стрелки раскрытия пунктов меню (на мобильных)
  document.querySelectorAll('.mega-toggle').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      var li = b.parentElement, on = !li.classList.contains('open');
      li.classList.toggle('open', on); b.setAttribute('aria-expanded', on ? 'true' : 'false');
      b.setAttribute('aria-label', L[lang()][on ? 'fold' : 'open']);
    });
  });

  // выбор языка выпадающим списком
  document.querySelectorAll('.lang-dd').forEach(function (dd) {
    var btn = dd.querySelector('.lang-dd-btn'), list = dd.querySelector('.lang-dd-list');
    function close() { list.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); var open = list.hidden; list.hidden = !open; btn.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    list.addEventListener('click', close);
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  });

  // строки таблиц каталога на главной — целиком ссылки
  document.querySelectorAll('.row-link tbody tr').forEach(function (tr) {
    tr.addEventListener('click', function (e) {
      if (e.target.closest('a, button')) return;
      var a = tr.querySelector('a[href]'); if (a) window.location.href = a.getAttribute('href');
    });
  });
})();
