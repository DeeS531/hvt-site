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
