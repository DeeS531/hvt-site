(function () {
  'use strict';

  var T = {
    ru: {
      title: 'ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ — изоляторы, ОПН, вводы, шинные опоры',
      brand_name: 'ТЕХНОЛОГИИ ВЫСОКОГО НАПРЯЖЕНИЯ',
      brand_sub: 'High Voltage Technologies',
      top_city: 'Украина, г. Киев',
      nav_home: 'Главная', nav_products: 'Продукция', nav_quality: 'Качество',
      nav_contacts: 'Контакты', nav_request: 'Оставить заявку', btn_request: 'Оставить заявку',
      btn_telegram: 'Telegram',
      hero_eyebrow: 'Продажа высоковольтного оборудования',
      hero_title: 'Высоковольтное оборудование для энергетики',
      hero_lead: 'Полимерные изоляторы, ограничители перенапряжения (разрядники), шинные опоры и вводы высоковольтные. Продукция с сертификатами соответствия и более чем 25-летним опытом эксплуатации.',
      hero_btn_products: 'Перейти к продукции', hero_btn_request: 'Оставить заявку',
      badge_iso1: 'ISO 9001', badge_iso2: 'ISO 14001', badge_cert: 'Сертификаты УкрСЕПРО', badge_ship: 'Поставки в Украину и за рубеж',
      stat1: 'лет опыта эксплуатации', stat2: 'основных групп изделий', stat3: 'диапазон напряжений', stat4: 'стандарта ISO',
      cat_eyebrow: 'Продукция', cat_title: 'Высоковольтное оборудование',
      cat_lead: 'Основные группы изделий для линий электропередачи, подстанций, железных дорог и выключателей.',
      card_line_t: 'Линейные изоляторы', card_line_d: 'Подвесные полимерные изоляторы для высоковольтных линий электропередач.',
      card_sup_t: 'Опорные изоляторы', card_sup_d: 'Опорно-стержневые полимерные изоляторы на напряжение от 10 до 220 кВ.',
      card_opn_t: 'Ограничители перенапряжения', card_opn_d: 'ОПН-П (разрядники) на напряжение от 0,22 до 330 кВ.',
      card_pass_t: 'Проходные изоляторы', card_pass_d: 'Полимерные проходные изоляторы ППЦ.',
      card_bush_t: 'Вводы высоковольтные', card_bush_d: 'Вводы для масляных выключателей 35 кВ.',
      card_bus_t: 'Шинные опоры и распорки', card_bus_d: 'Шинные опоры полимерные от 10 до 220 кВ и межфазные распорки от 35 до 330 кВ.',
      more: 'Подробнее',
      cat2_eyebrow: 'Каталог', cat2_title: 'Модели и обозначения',
      cat2_lead: 'Полный перечень с вариантами обозначений. Для подбора и расчёта — свяжитесь с нами.',
      tab_line: 'Линейные', tab_sup: 'Опорные', tab_opn: 'Ограничители', tab_pass: 'Проходные', tab_bus: 'Шинные опоры и распорки',
      th_group: 'Группа', th_model: 'Модель / обозначение', th_variants: 'Варианты обозначения',
      th_voltage: 'Напряжение', th_model_s: 'Модель', th_variants_s: 'Варианты обозначения',
      row_line70: 'Линейные изоляторы, 70 кН', row_line120: 'Линейные изоляторы, 120 кН', row_line160: 'Линейные изоляторы, 160 кН',
      val_on_request: 'по запросу', note_line: 'Взаимозаменяемость: гирлянда изоляторов ПС-70Е, ПСД-70Е, ПС-120Б, ПСВ-120Б.',
      note_sup: 'Варианты обозначения опорных изоляторов: ИОС, ИОСК, ОНШ, ОНШП, КОСК, ОТК, СК. Для контактной сети: ПСПКР, ФСПКР, НСПКР, КСПКР.',
      row_contact_net: 'Контактная сеть ж/д',
      note_opn: 'Разрядники и ограничители перенапряжения от 0,22 до 330 кВ.',
      row_bus_dist: 'Распорка межфазная',
      why_eyebrow: 'Почему выбирают нас', why_title: 'Надёжность, проверенная временем',
      why_lead: 'Поставляем оборудование для энергетических объектов Украины, ближнего и дальнего зарубежья.',
      f1_t: '25+ лет опыта', f1_d: 'Продукция проверена длительной эксплуатацией на энергообъектах.',
      f2_t: 'Сертификация', f2_d: 'Соответствие системе УкрСЕПРО, ISO 9001 и ISO 14001.',
      f3_t: 'Положительные отзывы', f3_d: 'Многочисленные отзывы потребителей подтверждают качество.',
      f4_t: 'Поставки', f4_d: 'Работаем с Украиной и зарубежными партнёрами.',
      q_eyebrow: 'Качество', q_title: 'Сертификаты и стандарты',
      q_lead: 'Всё оборудование имеет сертификаты соответствия. Копии документов предоставляем по запросу.',
      c1_t: 'УкрСЕПРО', c1_d: 'Сертификат соответствия', c2_t: 'ISO 9001', c2_d: 'Система управления качеством',
      c3_t: 'ISO 14001', c3_d: 'Экологический менеджмент', c4_t: 'СОУ, МПЕ, МЭК', c4_d: 'Применяемые стандарты',
      ct_eyebrow: 'Контакты', ct_title: 'Свяжитесь с нами',
      ct_lead: 'Подберём оборудование под ваши задачи и подготовим коммерческое предложение.',
      ct_phone: 'Телефон / Viber / WhatsApp', ct_email: 'Email', ct_telegram: 'Telegram', ct_address: 'Адрес',
      ct_city: 'г. Киев, Украина', ct_form: 'Оставить заявку на сайте', ct_form_btn: 'Открыть форму',
      footer_rights: 'Все права защищены.', footer_top: 'Наверх',
      form_title: 'Оставить заявку', form_lead: 'Опишите задачу — мы свяжемся с вами и подготовим предложение.', f_name: 'Имя', f_email: 'Почта', f_phone: 'Телефон', f_subject: 'Тема', f_message: 'Текст заявки', f_required: 'обязательное поле', f_optional: 'необязательно', f_submit: 'Отправить заявку', f_sent: 'Спасибо! Заявка отправлена. Мы свяжемся с вами.', f_back: 'На главную', f_note: 'Заявка отправляется на почту highvoltagetechnologies.ua@gmail.com',
    },
    uk: {
      title: 'ТЕХНОЛОГІЇ ВИСОКОЇ НАПРУГИ — ізолятори, ОПН, вводи, шинні опори',
      brand_name: 'ТЕХНОЛОГІЇ ВИСОКОЇ НАПРУГИ',
      brand_sub: 'High Voltage Technologies',
      top_city: 'Україна, м. Київ',
      nav_home: 'Головна', nav_products: 'Продукція', nav_quality: 'Якість',
      nav_contacts: 'Контакти', nav_request: 'Залишити заявку', btn_request: 'Залишити заявку',
      btn_telegram: 'Telegram',
      hero_eyebrow: 'Продаж високовольтного обладнання',
      hero_title: 'Високовольтне обладнання для енергетики',
      hero_lead: 'Полімерні ізолятори, обмежувачі перенапруги (розрядники), шинні опори та високовольтні вводи. Продукція з сертифікатами відповідності та понад 25-річним досвідом експлуатації.',
      hero_btn_products: 'Перейти до продукції', hero_btn_request: 'Залишити заявку',
      badge_iso1: 'ISO 9001', badge_iso2: 'ISO 14001', badge_cert: 'Сертифікати УкрСЕПРО', badge_ship: 'Поставки в Україну та за кордон',
      stat1: 'років досвіду експлуатації', stat2: 'основних груп виробів', stat3: 'діапазон напруг', stat4: 'стандарту ISO',
      cat_eyebrow: 'Продукція', cat_title: 'Високовольтне обладнання',
      cat_lead: 'Основні групи виробів для ліній електропередачі, підстанцій, залізниць і вимикачів.',
      card_line_t: 'Лінійні ізолятори', card_line_d: 'Підвісні полімерні ізолятори для високовольтних ліній електропередачі.',
      card_sup_t: 'Опорні ізолятори', card_sup_d: 'Опорно-стрижневі полімерні ізолятори на напругу від 10 до 220 кВ.',
      card_opn_t: 'Обмежувачі перенапруги', card_opn_d: 'ОПН-П (розрядники) на напругу від 0,22 до 330 кВ.',
      card_pass_t: 'Прохідні ізолятори', card_pass_d: 'Полімерні прохідні ізолятори ППЦ.',
      card_bush_t: 'Високовольтні вводи', card_bush_d: 'Вводи для масляних вимикачів 35 кВ.',
      card_bus_t: 'Шинні опори та розпірки', card_bus_d: 'Полімерні шинні опори від 10 до 220 кВ і міжфазні розпірки від 35 до 330 кВ.',
      more: 'Детальніше',
      cat2_eyebrow: 'Каталог', cat2_title: 'Моделі та позначення',
      cat2_lead: 'Повний перелік із варіантами позначень. Для підбору та розрахунку — зв’яжіться з нами.',
      tab_line: 'Лінійні', tab_sup: 'Опорні', tab_opn: 'Обмежувачі', tab_pass: 'Прохідні', tab_bus: 'Шинні опори та розпірки',
      th_group: 'Група', th_model: 'Модель / позначення', th_variants: 'Варіанти позначення',
      th_voltage: 'Напруга', th_model_s: 'Модель', th_variants_s: 'Варіанти позначення',
      row_line70: 'Лінійні ізолятори, 70 кН', row_line120: 'Лінійні ізолятори, 120 кН', row_line160: 'Лінійні ізолятори, 160 кН',
      val_on_request: 'за запитом', note_line: 'Взаємозамінність: гірлянда ізоляторів ПС-70Е, ПСД-70Е, ПС-120Б, ПСВ-120Б.',
      note_sup: 'Варіанти позначень опорних ізоляторів: ІОС, ІОСК, ОНШ, ОНШП, КОСК, ОТК, СК. Для контактної мережі: ПСПКР, ФСПКР, НСПКР, КСПКР.',
      row_contact_net: 'Контактна мережа залізниць',
      note_opn: 'Розрядники та обмежувачі перенапруги від 0,22 до 330 кВ.',
      row_bus_dist: 'Розпірка міжфазна',
      why_eyebrow: 'Чому обирають нас', why_title: 'Надійність, перевірена часом',
      why_lead: 'Постачаємо обладнання для енергооб’єктів України, ближнього та дальнього зарубіжжя.',
      f1_t: '25+ років досвіду', f1_d: 'Продукція перевірена тривалою експлуатацією на енергооб’єктах.',
      f2_t: 'Сертифікація', f2_d: 'Відповідність системі УкрСЕПРО, ISO 9001 та ISO 14001.',
      f3_t: 'Позитивні відгуки', f3_d: 'Численні відгуки споживачів підтверджують якість.',
      f4_t: 'Постачання', f4_d: 'Працюємо з Україною та зарубіжними партнерами.',
      q_eyebrow: 'Якість', q_title: 'Сертифікати та стандарти',
      q_lead: 'Усе обладнання має сертифікати відповідності. Копії документів надаємо на запит.',
      c1_t: 'УкрСЕПРО', c1_d: 'Сертифікат відповідності', c2_t: 'ISO 9001', c2_d: 'Система управління якістю',
      c3_t: 'ISO 14001', c3_d: 'Екологічний менеджмент', c4_t: 'СОУ, МПЕ, МЕК', c4_d: 'Застосовувані стандарти',
      ct_eyebrow: 'Контакти', ct_title: 'Зв’яжіться з нами',
      ct_lead: 'Підберемо обладнання під ваші завдання та підготуємо комерційну пропозицію.',
      ct_phone: 'Телефон / Viber / WhatsApp', ct_email: 'Email', ct_telegram: 'Telegram', ct_address: 'Адреса',
      ct_city: 'м. Київ, Україна', ct_form: 'Залишити заявку на сайті', ct_form_btn: 'Відкрити форму',
      footer_rights: 'Усі права захищено.', footer_top: 'Нагору',
      form_title: 'Залишити заявку', form_lead: 'Опишіть завдання — ми зв’яжемося з вами та підготуємо пропозицію.', f_name: 'Ім’я', f_email: 'Пошта', f_phone: 'Телефон', f_subject: 'Тема', f_message: 'Текст заявки', f_required: 'обов’язкове поле', f_optional: 'необов’язково', f_submit: 'Надіслати заявку', f_sent: 'Дякуємо! Заявку надіслано. Ми зв’яжемося з вами.', f_back: 'На головну', f_note: 'Заявка надсилається на пошту highvoltagetechnologies.ua@gmail.com',
    },
    en: {
      title: 'High Voltage Technologies — insulators, surge arresters, bushings, busbar supports',
      brand_name: 'HIGH VOLTAGE TECHNOLOGIES',
      brand_sub: 'High Voltage Technologies',
      top_city: 'Ukraine, Kyiv',
      nav_home: 'Home', nav_products: 'Products', nav_quality: 'Quality',
      nav_contacts: 'Contacts', nav_request: 'Request a quote', btn_request: 'Send a request',
      btn_telegram: 'Telegram',
      hero_eyebrow: 'High-voltage equipment supplier',
      hero_title: 'High-voltage equipment for power utilities',
      hero_lead: 'Polymer insulators, surge arresters (lightning arresters), busbar supports and high-voltage bushings. Certified products with more than 25 years of field experience.',
      hero_btn_products: 'View products', hero_btn_request: 'Send a request',
      badge_iso1: 'ISO 9001', badge_iso2: 'ISO 14001', badge_cert: 'UkrSEPRO certificates', badge_ship: 'Shipping in Ukraine and abroad',
      stat1: 'years of field experience', stat2: 'main product groups', stat3: 'voltage range', stat4: 'ISO standards',
      cat_eyebrow: 'Products', cat_title: 'High-voltage equipment',
      cat_lead: 'Main product groups for power lines, substations, railways and circuit breakers.',
      card_line_t: 'Line insulators', card_line_d: 'Polymer suspension insulators for high-voltage power lines.',
      card_sup_t: 'Post insulators', card_sup_d: 'Polymer post insulators for voltages from 10 to 220 kV.',
      card_opn_t: 'Surge arresters', card_opn_d: 'OPN-P (lightning arresters) for voltages from 0.22 to 330 kV.',
      card_pass_t: 'Bushing insulators', card_pass_d: 'Polymer bushing insulators PPTs.',
      card_bush_t: 'High-voltage bushings', card_bush_d: 'Bushings for oil circuit breakers, 35 kV.',
      card_bus_t: 'Busbar supports and spacers', card_bus_d: 'Polymer busbar supports from 10 to 220 kV and phase spacers from 35 to 330 kV.',
      more: 'Details',
      cat2_eyebrow: 'Catalog', cat2_title: 'Models and designations',
      cat2_lead: 'Full list with alternative designations. For selection and calculation, contact us.',
      tab_line: 'Line', tab_sup: 'Post', tab_opn: 'Arresters', tab_pass: 'Bushing', tab_bus: 'Busbar & spacers',
      th_group: 'Group', th_model: 'Model / designation', th_variants: 'Alternative designations',
      th_voltage: 'Voltage', th_model_s: 'Model', th_variants_s: 'Alternative designations',
      row_line70: 'Line insulators, 70 kN', row_line120: 'Line insulators, 120 kN', row_line160: 'Line insulators, 160 kN',
      val_on_request: 'on request', note_line: 'Interchangeable with insulator strings PS-70E, PSD-70E, PS-120B, PSV-120B.',
      note_sup: 'Alternative designations of post insulators: IOS, IOSK, ONSh, ONShP, KOSK, OTK, SK. For catenary: PSPKR, FSPKR, NSPKR, KSPKR.',
      row_contact_net: 'Railway catenary',
      note_opn: 'Surge arresters and limiters from 0.22 to 330 kV.',
      row_bus_dist: 'Phase spacer',
      why_eyebrow: 'Why choose us', why_title: 'Reliability proven over time',
      why_lead: 'We supply equipment to power facilities in Ukraine, nearby and distant foreign countries.',
      f1_t: '25+ years of experience', f1_d: 'Products proven by long-term operation at power facilities.',
      f2_t: 'Certification', f2_d: 'Compliant with UkrSEPRO, ISO 9001 and ISO 14001.',
      f3_t: 'Positive reviews', f3_d: 'Numerous customer reviews confirm quality.',
      f4_t: 'Supply', f4_d: 'We work with Ukraine and foreign partners.',
      q_eyebrow: 'Quality', q_title: 'Certificates and standards',
      q_lead: 'All equipment has conformity certificates. Copies of documents are available on request.',
      c1_t: 'UkrSEPRO', c1_d: 'Conformity certificate', c2_t: 'ISO 9001', c2_d: 'Quality management system',
      c3_t: 'ISO 14001', c3_d: 'Environmental management', c4_t: 'SOU, MPE, IEC', c4_d: 'Applied standards',
      ct_eyebrow: 'Contacts', ct_title: 'Get in touch',
      ct_lead: 'We will select equipment for your needs and prepare a commercial offer.',
      ct_phone: 'Phone / Viber / WhatsApp', ct_email: 'Email', ct_telegram: 'Telegram', ct_address: 'Address',
      ct_city: 'Kyiv, Ukraine', ct_form: 'Send a request on the website', ct_form_btn: 'Open form',
      footer_rights: 'All rights reserved.', footer_top: 'Back to top',
      form_title: 'Send a request', form_lead: 'Describe your task — we will contact you and prepare an offer.', f_name: 'Name', f_email: 'Email', f_phone: 'Phone', f_subject: 'Subject', f_message: 'Message', f_required: 'required', f_optional: 'optional', f_submit: 'Send request', f_sent: 'Thank you! Your request has been sent. We will contact you.', f_back: 'Back to home', f_note: 'The request is sent to highvoltagetechnologies.ua@gmail.com',
    }
  };

  var LANGS = ['ru', 'uk', 'en'];
  var LOCALE = { ru: 'ru', uk: 'uk', en: 'en' };

  function getLang() {
    var l = null;
    try { l = localStorage.getItem('hvt_lang'); } catch (e) {}
    return LANGS.indexOf(l) > -1 ? l : 'ru';
  }

  // --- контекст страницы: главная/форма (переводятся на месте), страницы продукции (отдельные файлы в ua/ и en/) ---
  var DOC = document.documentElement;
  var PAGE_LANG = DOC.getAttribute('data-page-lang');            // 'uk' | 'en' на переведённых страницах
  var FOLDER = { ru: '', uk: 'ua/', en: 'en/' };
  var path = location.pathname.split('/');
  var FILE = path[path.length - 1] || 'index.html';
  var IN_SUB = PAGE_LANG === 'uk' || PAGE_LANG === 'en';          // мы в папке ua/ или en/
  var IS_HOME = DOC.hasAttribute('data-home') || FILE === 'form.html' || FILE === 'index.html';
  var PRODUCT = /^[A-Za-z0-9_\-.]+\.html$/;

  function targetUrl(lang) {
    var root = IN_SUB ? '../' : '';
    return root + FOLDER[lang] + FILE + location.search + location.hash;
  }

  function apply(lang) {
    var dict = T[lang];
    DOC.lang = LOCALE[lang];
    if (dict.title && DOC.hasAttribute('data-home')) document.title = dict.title;
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (dict[key] !== undefined) el.textContent = dict[key];
    });
    document.querySelectorAll('[data-i18n-attr]').forEach(function (el) {
      // формат: "placeholder:key;title:key2"
      el.getAttribute('data-i18n-attr').split(';').forEach(function (pair) {
        var p = pair.split(':');
        if (dict[p[1]] !== undefined) el.setAttribute(p[0], dict[p[1]]);
      });
    });
    document.querySelectorAll('[data-lang-btn]').forEach(function (b) {
      var on = b.getAttribute('data-lang-btn') === lang;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    if (IS_HOME) relinkProducts(lang);
  }

  // на главной и в форме ссылки на страницы продукции ведут на версию выбранного языка
  function relinkProducts(lang) {
    document.querySelectorAll('a[href]').forEach(function (a) {
      var orig = a.getAttribute('data-orig-href');
      if (orig === null) { orig = a.getAttribute('href'); a.setAttribute('data-orig-href', orig); }
      var base = orig.split('#')[0];
      if (PRODUCT.test(base) && base !== 'index.html' && base !== 'form.html') a.setAttribute('href', FOLDER[lang] + orig);
      else a.setAttribute('href', orig);
    });
  }

  function setLang(lang) {
    if (LANGS.indexOf(lang) === -1) return;
    try { localStorage.setItem('hvt_lang', lang); } catch (e) {}
    if (IS_HOME) { apply(lang); return; }
    if (lang === (IN_SUB ? PAGE_LANG : 'ru')) { apply(lang); return; }
    location.href = targetUrl(lang);
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-lang-btn]').forEach(function (b) {
      b.addEventListener('click', function (e) { e.preventDefault(); setLang(b.getAttribute('data-lang-btn')); });
    });
    var lang = getLang();
    if (IN_SUB) {                                   // страница уже на своём языке: он главный
      try { localStorage.setItem('hvt_lang', PAGE_LANG); } catch (e) {}
      apply(PAGE_LANG);
    } else if (!IS_HOME && lang !== 'ru') {         // русская страница продукции, а выбран другой язык
      location.replace(targetUrl(lang));
    } else {
      apply(lang);
    }
  });
})();
