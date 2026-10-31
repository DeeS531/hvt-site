// Убирает водяные знаки старого сайта (www.sep.ho.ua / slavsep@gmail.com) с фото ОПН.
// Метод: тонкие бледные штрихи текста убираются медианным фильтром; пиксель заменяется медианой, только если отличается от неё
// не сильнее порога (резкие контуры изделия не трогаются). На светлом фоне порог выше. Два прохода.
// Нужен модуль sharp (в проекте не установлен): SHARP_PATH=/путь/к/node_modules/sharp node tools/unwatermark.js
// Вход по умолчанию: data/photos_orig/*, выход: site/images/opn/photo/*.png (длинная сторона ≤ 1000 px). Для чертежей ППЦ: data/ppc_wm_orig -> site/images/ppc.
const path = require('path'), fs = require('fs');
const sharp = require(process.env.SHARP_PATH || '/Users/dees531/Documents/repot_aff/node_modules/sharp');
const ROOT = path.join(__dirname, '..');
// по умолчанию: фото ОПН; можно задать папки: node tools/unwatermark.js <вход> <выход>
const IN = process.argv[2] || path.join(ROOT, 'data', 'photos_orig'), OUT = process.argv[3] || path.join(ROOT, 'site', 'images', 'opn', 'photo');
// [медиана 1-го прохода, 2-го, порог на изделии, порог на светлом фоне, яркость «светлого фона»]
const DEF = [15, 11, 45, 110, 222];
const P = {
  'OPN10schem.PNG': [31, 21, 45, 75, 200], 'OPN10version4.PNG': [31, 21, 45, 75, 200],
  'OPN10version2.PNG': [21, 15, 45, 75, 200], 'OPN10version3.PNG': [21, 15, 45, 75, 200],
};
async function pass(buf, info, M, T0, TB, BL) {
  const m = await sharp(buf, { raw: info }).median(M).raw().toBuffer();
  const c = info.channels, o = Buffer.from(buf);
  for (let i = 0; i < buf.length; i += c) {
    let d = 0, lum = 0;
    for (let k = 0; k < c; k++) { d = Math.max(d, Math.abs(buf[i+k] - m[i+k])); lum += m[i+k]; }
    if (d <= (lum / c >= BL ? TB : T0)) for (let k = 0; k < c; k++) o[i+k] = m[i+k];
  }
  return o;
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  for (const f of fs.readdirSync(IN)) {
    const [m1, m2, T0, TB, BL] = P[f] || (process.env.SHOP_PHOTO && /^SHOP\d+-\d(-p)?\.png$/.test(f) ? [21, 15, 75, 85, 185] : DEF);   // SHOP_PHOTO=1: рендеры шинных опор — усиленная обработка
    const { data, info } = await sharp(path.join(IN, f)).removeAlpha().raw().toBuffer({ resolveWithObject: true });
    const raw = { width: info.width, height: info.height, channels: info.channels };
    let o = await pass(data, raw, m1, T0, TB, BL);
    o = await pass(o, raw, m2, T0, TB, BL);
    const W = parseInt(process.env.WHITE || '0');   // для чертежей: светлые остатки знака -> чисто белый (WHITE=205)
    if (W) for (let i = 0; i < o.length; i += raw.channels) { let mn = 255; for (let k = 0; k < raw.channels; k++) mn = Math.min(mn, o[i+k]); if (mn >= W) for (let k = 0; k < raw.channels; k++) o[i+k] = 255; }
    const out = path.join(OUT, f.replace(/\.[^.]+$/, '') + '.png');
    await sharp(o, { raw }).resize({ width: 1000, height: 1000, fit: 'inside', withoutEnlargement: true }).png({ compressionLevel: 9 }).toFile(out);
    console.log(path.basename(out), fs.statSync(out).size);
  }
})();
